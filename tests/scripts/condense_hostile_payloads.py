"""
condense_hostile_payloads.py — Strip redundant fields from GusEngine test runs.

Keeps ALL data needed for hostile auditing:
  - query_id, technical_issue, query_text (identification)
  - response_parsed (Gus's full diagnostic: reasoning, instructions, answer paths, citations)
  - current_state (phase)
  - branch_id, branch_path, turn (BFS tree position)

Drops:
  - response_raw (redundant — it's just response_parsed as a string)
  - rag_sources (internal RAG chunks — 48% of file size)
  - validated_fix (redundant — already in the XLSX answer key)
  - diagnostic_reasoning, mechanic_instructions, answer_paths, citations,
    intersecting_subsystems, components_mentioned (all extracted duplicates of response_parsed)
  - Infrastructure metrics: latency, http_status, response_bytes, etc.
  - Keyword grades: grade, grade_detail, keyword_hits, keyword_misses
  - Test harness metadata: run_id, conversation_id, scenario_id, repeat_num, etc.

Output: split into files of ~25 queries each, named xxx_part1.txt, xxx_part2.txt
"""

import json
import os
import glob

BASE = r'J:\GusEngine\tests\hostile_analysis'
QUERIES_PER_FILE = 25

# Fields to KEEP — everything the hostile auditor needs
KEEP_FIELDS = {
    'query_id',
    'technical_issue',
    'query_text',
    'query_category',
    'response_parsed',
    'current_state',
    'branch_id',
    'branch_path',
    'turn',
}


def condense_records(records):
    """Strip records to only audit-relevant fields."""
    condensed = []
    for rec in records:
        slim = {k: v for k, v in rec.items() if k in KEEP_FIELDS}
        condensed.append(slim)
    return condensed


def group_by_query(records):
    """Group records by query_id, preserving order."""
    groups = {}
    order = []
    for rec in records:
        qid = rec.get('query_id', 'unknown')
        if qid not in groups:
            groups[qid] = []
            order.append(qid)
        groups[qid].append(rec)
    return groups, order


def process_vehicle(vehicle_dir):
    """Process all JSON files in a vehicle directory."""
    # Find the source JSON (the full unsplit version or reassemble from splits)
    json_files = sorted(glob.glob(os.path.join(vehicle_dir, '*.json')))
    if not json_files:
        print(f'  No JSON files found, skipping')
        return

    # Load all records
    all_records = []
    for jf in json_files:
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            if isinstance(data, list):
                all_records.extend(data)
            else:
                all_records.append(data)

    original_size = sum(os.path.getsize(jf) for jf in json_files)
    print(f'  Loaded {len(all_records)} records from {len(json_files)} file(s) ({original_size:,} bytes)')

    # Condense
    condensed = condense_records(all_records)

    # Group by query_id
    groups, order = group_by_query(condensed)
    print(f'  {len(order)} unique queries, {len(condensed)} total records after condensing')

    # Split into chunks of QUERIES_PER_FILE queries
    chunks = []
    current_chunk_qids = []
    for qid in order:
        current_chunk_qids.append(qid)
        if len(current_chunk_qids) >= QUERIES_PER_FILE:
            chunks.append(current_chunk_qids[:])
            current_chunk_qids = []
    if current_chunk_qids:
        chunks.append(current_chunk_qids)

    # Remove old txt files (the oversized ones)
    for old in glob.glob(os.path.join(vehicle_dir, '*.txt')):
        os.remove(old)

    # Write chunks
    total_new_size = 0
    for i, chunk_qids in enumerate(chunks, 1):
        chunk_records = []
        for qid in chunk_qids:
            chunk_records.extend(groups[qid])

        filename = f'gus_diagnostic_output_part{i}.txt'
        filepath = os.path.join(vehicle_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chunk_records, f, indent=2, ensure_ascii=False)

        fsize = os.path.getsize(filepath)
        total_new_size += fsize
        print(f'    {filename}: {fsize:,} bytes ({len(chunk_qids)} queries, {len(chunk_records)} records)')

    reduction = (1 - total_new_size / original_size) * 100
    print(f'  Total: {total_new_size:,} bytes ({reduction:.0f}% reduction)')
    print()


def main():
    for vehicle in ['mustang', 'mercedes', 'mercruiser', 'cessna']:
        vehicle_dir = os.path.join(BASE, vehicle)
        if not os.path.isdir(vehicle_dir):
            continue
        print(f'=== {vehicle.upper()} ===')
        process_vehicle(vehicle_dir)

    print('Done!')


if __name__ == '__main__':
    main()
