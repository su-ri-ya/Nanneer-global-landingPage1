import re

with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

defs_match = re.search(r'<defs>([\s\S]*?)</defs>', code)
if defs_match:
    defs_text = defs_match.group(1)
    ids = re.findall(r'id=["\']([^"\']+)["\']', defs_text)
    print("Found Defs IDs in ScadaSchematicSimulation.tsx:")
    for i in ids:
        print(f"  - {i}")

print("\n--- Pipeline rendering paths in ScadaSchematicSimulation.tsx ---")
pipes = re.findall(r'<path[^>]*stroke=[^>]*>', code)
pipe_strokes = set()
for p in pipes:
    stroke_match = re.search(r'stroke=["\']([^"\']+)["\']', p)
    width_match = re.search(r'strokeWidth=["\']?([\d\.]+)["\']?', p)
    filter_match = re.search(r'filter=["\']([^"\']+)["\']', p)
    if stroke_match and width_match:
        pipe_strokes.add((stroke_match.group(1), width_match.group(1), filter_match.group(1) if filter_match else None))

for s, w, flt in sorted(pipe_strokes):
    print(f"Stroke: {s:25} Width: {w:4} Filter: {flt}")
