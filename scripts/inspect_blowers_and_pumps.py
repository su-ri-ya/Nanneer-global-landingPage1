import re

with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Find blower definitions
blowers = re.findall(r'(<g id="blower[^"]*"[\s\S]*?</g>)', code)
print(f"Blower blocks found: {len(blowers)}")
for b in blowers:
    print(b[:600])
    print("---------------------------------------------")

# Find pump definitions
pumps = re.findall(r'(<g id="pump[^"]*"[\s\S]*?</g>)', code)
print(f"Pump blocks found: {len(pumps)}")
for p in pumps[:3]:
    print(p[:600])
    print("---------------------------------------------")
