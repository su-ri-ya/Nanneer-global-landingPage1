import re

with open('scripts/extracted_schematic_pipelines.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all <path ... d="..." ... /> or stroke
paths = re.findall(r'<path[\s\S]*?/>', text)
print(f"Total <path ... /> elements in pipeline section: {len(paths)}")

route_definitions = []
for p in paths:
    d_match = re.search(r'd=["`{]([^"`}]+)["`}]', p)
    stroke_match = re.search(r'stroke=["`{]([^"`}]+)["`}]', p)
    stroke_w = re.search(r'strokeWidth=["`{]([^"`}]+)["`}]', p)
    if d_match:
        d = d_match.group(1).strip()
        s = stroke_match.group(1).strip() if stroke_match else "none"
        sw = stroke_w.group(1).strip() if stroke_w else "none"
        if any(cmd in d for cmd in ['M', 'L', 'C', 'Q', 'Z']):
            route_definitions.append((d, s, sw))

print(f"Total path routes extracted: {len(route_definitions)}")

# De-duplicate paths (since many are layered: casing + fluid + anim)
unique_paths = {}
for d, s, sw in route_definitions:
    # normalize whitespace
    d_clean = re.sub(r'\s+', ' ', d).strip()
    if d_clean not in unique_paths:
        unique_paths[d_clean] = []
    unique_paths[d_clean].append((s, sw))

print(f"Unique geometric routes in schematic: {len(unique_paths)}")
for i, (path_str, layers) in enumerate(unique_paths.items(), 1):
    strokes = [l[0] for l in layers]
    print(f"\n[{i:2}] Route: {path_str}")
    print(f"     Layers ({len(layers)}): {strokes}")
