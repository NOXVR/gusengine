#!/usr/bin/env python3
"""V8 Thermodynamic Ingestion Daemon.
Extracts PDFs from VMDK/OVA files, chunks them with absolute page
watermarks, and maintains an atomic manifest for deduplication.
"""

import os, sys, time, subprocess, shutil, tempfile, hashlib, json, glob
import fitz  # PyMuPDF

ENGINE_DIR = os.path.expanduser("~/diagnostic_engine")
DOWNLOAD_DIR = os.path.join(ENGINE_DIR, "downloads")
OUTPUT_DIR = os.path.join(ENGINE_DIR, "extracted_manuals")
QUARANTINE_DIR = os.path.join(ENGINE_DIR, "quarantine")
OVA_STAGING = os.path.join(ENGINE_DIR, "staging", "ova")
MOUNTS_DIR = os.path.join(ENGINE_DIR, "staging", "mounts")
MANIFEST_FILE = os.path.join(OUTPUT_DIR, "manifest.json")

def get_hash(filepath):
    """1MB Buffer for high-speed I/O on 20GB files."""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()

def validate_file_header(path):
    """Validate VMDK/OVA magic bytes to detect corruption."""
    try:
        with open(path, 'rb') as f:
            magic = f.read(4)
        if path.lower().endswith('.vmdk'):
            return magic in [b'KDMV', b'# Di']
        if path.lower().endswith('.ova'):
            with open(path, 'rb') as f:
                f.seek(257)
                return f.read(5) == b'ustar'
    except Exception:
        pass
    return True  # Proceed if unknown format (caught by extraction fail anyway)

def wait_for_stable(path):
    """Multi-stage TOCTOU-immune OS lock verification with double-check.
    Includes OSError guards for file deletion during check and zero-byte
    file detection to prevent processing empty/incomplete downloads.

    V2 FIX: All code paths that execute `continue` now increment `elapsed`
    to prevent infinite loops on zero-byte files or size-changing files.
    """
    print(f"Verifying absolute OS file lock release: {path}")
    elapsed = 0
    while elapsed < 7200:  # 2-hour timeout
        try:
            subprocess.check_output(['lsof', path], stderr=subprocess.DEVNULL)
            time.sleep(10)
            elapsed += 10
        except subprocess.CalledProcessError:
            # File unlocked by lsof. Double-verify TOCTOU buffer.
            time.sleep(5)
            elapsed += 5  # V2 FIX: count this sleep toward timeout
            try:
                subprocess.check_output(['lsof', path], stderr=subprocess.DEVNULL)
                continue  # Re-locked during buffer — keep waiting
            except subprocess.CalledProcessError:
                # Confirm size stability with OSError guards
                try:
                    prev_size = os.path.getsize(path)
                except OSError:
                    return False  # File was deleted during check
                time.sleep(5)
                elapsed += 5  # V2 FIX: count this sleep toward timeout
                try:
                    curr_size = os.path.getsize(path)
                except OSError:
                    return False  # File was deleted during check
                if curr_size != prev_size:
                    continue  # Still writing
                if curr_size == 0:
                    # V2 FIX: elapsed is already incremented above.
                    # Without this, a zero-byte file caused an infinite loop
                    # because elapsed was only incremented in the try branch.
                    continue  # Empty file — still arriving
                if validate_file_header(path):
                    return True
                print(f"ABORT: {path} has invalid VMDK/OVA header. Corrupt download.")
                return False
    return False

def write_manifest_atomic(manifest):
    """Atomically write manifest.json using tmp+rename pattern."""
    dir_name = os.path.dirname(MANIFEST_FILE)
    with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False, suffix='.tmp') as tmp:
        json.dump(manifest, tmp, indent=2)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path = tmp.name
    os.replace(tmp_path, MANIFEST_FILE)

def chunk_pdf(input_path, output_dir, file_hash, base_name, chunk_size=5):
    """Chunk PDF into 5-page segments with absolute page watermarks.

    chunk_size=5 ensures semantic token limits (400 tokens) align with
    physical PDF page boundaries. Each chunk produces a narrow page range
    (e.g., pages_101-105.pdf) so citation accuracy is ±4 pages max.

    Absolute page watermarks [[ABSOLUTE_PAGE: N]] are burned into the
    text layer of each page BEFORE Mistral OCR processes them. This
    eliminates all LLM arithmetic for citations.
    """
    with fitz.open(input_path) as doc:
        total = len(doc)
        for i in range(0, total, chunk_size):
            start_page = i + 1
            end_page = min(i + chunk_size, total)
            with fitz.open() as chunk_doc:
                chunk_doc.insert_pdf(doc, from_page=i, to_page=end_page - 1)

                # Burn absolute provenance into the text layer.
                # Mistral OCR will read this marker and embed it in the
                # vectorized text. The LLM cites the integer directly.
                for page_idx in range(len(chunk_doc)):
                    abs_page = start_page + page_idx
                    page = chunk_doc[page_idx]
                    page.insert_text(
                        (72, 36),
                        f"[[ABSOLUTE_PAGE: {abs_page}]]",
                        fontsize=10,
                        color=(0.6, 0.6, 0.6)
                    )

                out_name = f"{base_name}_pages_{start_page}-{end_page}_{file_hash[:8]}.pdf"
                chunk_doc.save(os.path.join(output_dir, out_name))
                print(f"  Created chunk: {out_name}")

def load_manifest():
    """Load manifest with corrupt-backup safety."""
    if os.path.exists(MANIFEST_FILE):
        try:
            with open(MANIFEST_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            backup = MANIFEST_FILE + ".corrupt." + str(int(time.time()))
            shutil.copy2(MANIFEST_FILE, backup)
            print(f"WARNING: Corrupt manifest backed up to {backup}")
    return {}

def process_file(file_path):
    """Process a single VMDK/OVA/PDF file."""
    # V8 FIX (Phase 10 DT R3): mount_point initialized to None so the
    # finally block can safely check before cleanup. mkdtemp moved INSIDE
    # the try block — if disk is full or inodes exhausted, OSError is caught
    # by the quarantine handler instead of crashing the daemon.
    mount_point = None
    extract_dir = None
    target_vmdk = file_path
    success = False

    try:
        # V8 FIX (Phase 10 DT R3): mkdtemp inside try — OSError from disk
        # full / permission denied now triggers quarantine, not daemon crash.
        mount_point = tempfile.mkdtemp(prefix="vmdk_mount_", dir=MOUNTS_DIR)

        # V8 FIX (Phase 10 DT): get_hash(), load_manifest(), and dedup
        # check moved INSIDE the try block. Previously, a PermissionError
        # or OSError here would crash the daemon unhandled, bypassing the
        # quarantine logic and causing an infinite systemd restart loop.
        file_hash = get_hash(file_path)
        manifest = load_manifest()

        if file_hash in manifest:
            print(f"Skipping duplicate: {file_path}")
            os.remove(file_path)
            return

        if file_path.lower().endswith('.ova'):
            extract_dir = tempfile.mkdtemp(prefix="ova_extract_", dir=OVA_STAGING)
            subprocess.run(["tar", "-xf", file_path, "-C", extract_dir], check=True)
            largest_size = -1
            for root, _, files in os.walk(extract_dir):
                for f in files:
                    if f.lower().endswith('.vmdk'):
                        fp = os.path.join(root, f)
                        size = os.path.getsize(fp)
                        if size > largest_size:
                            largest_size = size
                            target_vmdk = fp

        if target_vmdk.lower().endswith(('.vmdk', '.ova')):
            subprocess.run(
                ["guestmount", "-a", target_vmdk, "-i", "--ro", mount_point],
                check=True
            )
            for root, _, files in os.walk(mount_point):
                for name in files:
                    if name.lower().endswith('.pdf'):
                        src = os.path.join(root, name)
                        pdf_hash = get_hash(src)
                        if pdf_hash not in manifest:
                            chunk_pdf(
                                src, OUTPUT_DIR, pdf_hash,
                                name.replace('.pdf', '').replace(' ', '_')
                            )
                            # V2 FIX: Unified manifest value type to dict
                            manifest[pdf_hash] = {
                                "timestamp": time.time(),
                                "file": name
                            }
        elif target_vmdk.lower().endswith('.pdf'):
            chunk_pdf(
                target_vmdk, OUTPUT_DIR, file_hash,
                os.path.basename(target_vmdk).replace('.pdf', '').replace(' ', '_')
            )
            # V2 FIX: Removed dead code — line 465 in V1 wrote a string
            # that was immediately overwritten by the dict on line 467.

        manifest[file_hash] = {
            "timestamp": time.time(),
            "file": os.path.basename(file_path)
        }
        write_manifest_atomic(manifest)
        success = True

    except Exception as e:
        print(f"Extraction Error: {e}")
        # V8 FIX (Phase 10 DT R5): Guard against file vanishing during extraction.
        # If file was deleted mid-process (cancelled upload), skip quarantine
        # to avoid false CRITICAL cascade identical to the main loop fix (Row 33).
        if not os.path.exists(file_path):
            print(f"File vanished during extraction (normal): {file_path}")
        else:
            try:
                os.makedirs(QUARANTINE_DIR, exist_ok=True)
                shutil.move(
                    file_path,
                    os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
                )
                print(f"QUARANTINED (extraction failure): {file_path}")
            except Exception:
                # V8 FIX (Phase 10): If shutil.move fails, forcibly delete.
                # Without this, the file persists in DOWNLOAD_DIR and triggers
                # an infinite 10-second extraction retry loop.
                try:
                    os.remove(file_path)
                    print(f"FORCE-DELETED (quarantine failed): {file_path}")
                except OSError as e2:
                    # V8 FIX (Phase 10 DT R6): TOCTOU guard — if file vanished
                    # between os.path.exists check and here, suppress false CRITICAL.
                    if isinstance(e2, FileNotFoundError):
                        print(f"File vanished during quarantine (normal): {file_path}")
                    else:
                        print(f"CRITICAL: Cannot quarantine or delete {file_path}: {e2}. Manual intervention required.")
    finally:
        # V8 FIX (Phase 10 DT R3): mount_point may be None if mkdtemp failed.
        # Guard with truthiness check before os.path.ismount.
        if mount_point and os.path.ismount(mount_point):
            subprocess.run(["guestunmount", mount_point], check=False)
            time.sleep(2)
        # V8 FIX (Phase 10 DT R7): Only rmtree if the mount was successfully
        # detached. If guestunmount failed (busy mount), rmtree would traverse
        # the entire FUSE filesystem — ignore_errors swallows EROFS but wastes
        # minutes of I/O. ExecStopPost handles stuck mounts at service level.
        if mount_point and not os.path.ismount(mount_point):
            shutil.rmtree(mount_point, ignore_errors=True)
        if extract_dir:
            shutil.rmtree(extract_dir, ignore_errors=True)

    if success:
        try:
            os.remove(file_path)  # ONLY DELETE ON SUCCESS
        except OSError:
            pass

if __name__ == "__main__":
    for d in [DOWNLOAD_DIR, OUTPUT_DIR, OVA_STAGING, MOUNTS_DIR, QUARANTINE_DIR]:
        os.makedirs(d, exist_ok=True)
    print("V8 Ingestion Daemon Active.")
    while True:
        for f in os.listdir(DOWNLOAD_DIR):
            path = os.path.join(DOWNLOAD_DIR, f)
            if f.lower().endswith(('.vmdk', '.ova', '.pdf')):
                try:
                    # 30-second thermal age limit prevents racing active downloads
                    if time.time() - os.stat(path).st_mtime < 30:
                        continue
                except OSError:
                    continue

                if wait_for_stable(path):
                    process_file(path)
                else:
                    # V8 FIX: Quarantine files that fail stabilization.
                    # Without this, the file remains in DOWNLOAD_DIR and is
                    # re-discovered every 10 seconds. Since wait_for_stable()
                    # blocks for 2 hours per attempt, a single zero-byte file
                    # causes a permanent rolling livelock that halts ALL
                    # ingestion. Moving to quarantine breaks the cycle.

                    # V8 FIX (Phase 10 DT R4): If the file was deleted during
                    # wait_for_stable() (user cancelled SCP, network tool cleanup),
                    # skip quarantine entirely. Without this guard, os.rename throws
                    # FileNotFoundError, cascading through os.remove to a false
                    # CRITICAL log demanding "manual intervention" for a normal event.
                    if not os.path.exists(path):
                        print(f"File vanished during stabilization (normal): {path}")
                        continue

                    quarantine_dest = os.path.join(QUARANTINE_DIR, os.path.basename(path))
                    try:
                        # V8 FIX (Phase 10 DT R6): Ensure quarantine dir exists at
                        # runtime for parity with process_file's quarantine block.
                        os.makedirs(QUARANTINE_DIR, exist_ok=True)
                        # V8 FIX (Phase 10 DT R7): shutil.move handles cross-device
                        # moves (EXDEV) by falling back to copy+delete. os.rename
                        # raises OSError on cross-device, bypassing quarantine.
                        shutil.move(path, quarantine_dest)
                        print(f"QUARANTINED (failed stabilization after 2h): {path} -> {quarantine_dest}")
                    except OSError:
                        # LAST RESORT: If quarantine fails (permissions, cross-device,
                        # etc.), forcibly delete the file. A deleted file is recoverable
                        # from backups; a livelocked daemon is not.
                        try:
                            os.remove(path)
                            print(f"FORCE-DELETED (quarantine failed): {path}")
                        except OSError as e2:
                            # V8 FIX (Phase 10 DT R6): If the file vanished between
                            # os.path.exists check and here (TOCTOU), suppress the
                            # false CRITICAL instead of alarming the operator.
                            if isinstance(e2, FileNotFoundError):
                                print(f"File vanished during quarantine (normal): {path}")
                            else:
                                print(f"CRITICAL: Cannot quarantine or delete {path}: {e2}. Manual intervention required.")
        time.sleep(10)
