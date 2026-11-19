import re

with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Find tank definitions in ScadaSchematicSimulation.tsx
tank_blocks = re.findall(r'(<g id="tank-[^"]*"[\s\S]*?</g>)', code)
print(f"Found tank blocks: {len(tank_blocks)}")
for tb in tank_blocks:
    id_match = re.search(r'id="(tank-[^"]*)"', tb)
    print("Tank ID:", id_match.group(1) if id_match else "unknown")
    print(tb[:400])
    print("--------------------------------------------------")
