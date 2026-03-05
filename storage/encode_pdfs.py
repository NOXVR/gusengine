import os, base64, json

pdf_dir = r'j:\GusEngine\storage\pdfs'
pdfs = [(f, os.path.getsize(os.path.join(pdf_dir, f)))
        for f in os.listdir(pdf_dir)
        if f.endswith('.pdf') and (f.startswith('00.') or f.startswith('03.') or f.startswith('05.') or f.startswith('07.'))]
pdfs.sort(key=lambda x: x[1])
selected = pdfs[:20]

out_path = r'j:\GusEngine\storage\pdf_transfer.py'
with open(out_path, 'w') as out:
    out.write('import base64, os\n')
    out.write('os.makedirs("/workspace/GusEngine/storage/pdfs", exist_ok=True)\n')
    out.write('files = {\n')
    for name, size in selected:
        filepath = os.path.join(pdf_dir, name)
        with open(filepath, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        out.write('  ' + json.dumps(name) + ': "' + b64 + '",\n')
    out.write('}\n')
    out.write('for name, data in files.items():\n')
    out.write('    path = f"/workspace/GusEngine/storage/pdfs/{name}"\n')
    out.write('    with open(path, "wb") as f:\n')
    out.write('        f.write(base64.b64decode(data))\n')
    out.write('    size = os.path.getsize(path)\n')
    out.write('    print(f"  wrote {name} ({size} bytes)")\n')
    out.write('print(f"Done! {len(files)} PDFs transferred.")\n')

total = sum(s for _, s in selected)
script_size = os.path.getsize(out_path)
print(f'Transfer script created at {out_path}')
print(f'Total PDF data: {total // 1024}KB')
print(f'Script file size: {script_size // 1024}KB')
print(f'Files included: {len(selected)}')
