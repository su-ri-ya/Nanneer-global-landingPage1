import re

with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Find how shadows are applied
shadow_uses = re.findall(r'<[^>]*filter=["\']url\(#[^)]+\)["\'][^>]*>', code)
print(f"Elements using filter: {len(shadow_uses)}")
for u in shadow_uses[:10]:
    print("  ", u[:120])

# Find bottom shadows (like ellipse, rect under tanks/vessels)
ground_shadows = []
lines = code.split('\n')
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['shadow', 'bottom', 'pedestal', 'footing', 'ground', 'base']):
        ground_shadows.append((i+1, line.strip()))

print(f"\nGround / bottom shadow references: {len(ground_shadows)}")
for ln, text in ground_shadows[:15]:
    print(f"  Line {ln}: {text[:100]}")
