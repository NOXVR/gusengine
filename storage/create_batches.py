import os, base64, json

pdf_dir = r'j:\GusEngine\storage\pdfs'
pdfs = [(f, os.path.getsize(os.path.join(pdf_dir, f)))
        for f in os.listdir(pdf_dir)
        if f.endswith('.pdf') and (f.startswith('00.') or f.startswith('03.') or f.startswith('05.') or f.startswith('07.'))]
pdfs.sort(key=lambda x: x[1])
selected = pdfs[:20]

# Split into 4 batches of 5
for batch_idx in range(4):
    batch = selected[batch_idx*5:(batch_idx+1)*5]
    out_path = os.path.join(r'j:\GusEngine\storage', f'pdf_batch_{batch_idx+1}.py')
    
    with open(out_path, 'w') as out:
        out.write('import base64, os\n')
        out.write('os.makedirs("/workspace/GusEngine/storage/pdfs", exist_ok=True)\n')
        out.write('files = {\n')
        for name, size in batch:
            filepath = os.path.join(pdf_dir, name)
            with open(filepath, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode()
            out.write(f'  {json.dumps(name)}: "{b64}",\n')
        out.write('}\n')
        out.write('for name, data in files.items():\n')
        out.write('    path = f"/workspace/GusEngine/storage/pdfs/{name}"\n')
        out.write('    with open(path, "wb") as f:\n')
        out.write('        f.write(base64.b64decode(data))\n')
        out.write('    sz = os.path.getsize(path)\n')
        out.write('    print(f"  wrote {name} ({sz} bytes)")\n')
        out.write(f'print("Batch {batch_idx+1} done! {len(batch)} PDFs.")\n')
    
    batch_size = os.path.getsize(out_path)
    batch_total = sum(s for _, s in batch)
    print(f"Batch {batch_idx+1}: {len(batch)} files, {batch_total//1024}KB data, {batch_size//1024}KB script")
    for name, size in batch:
        print(f"  - {name} ({size//1024}KB)")

total = sum(s for _, s in selected)
print(f"\nTotal: {len(selected)} files, {total//1024}KB")
