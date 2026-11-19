import re

with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Find pump markers or rendering in ScadaSchematicSimulation.tsx
lines = code.split('\n')
for i, line in enumerate(lines):
    if any(k in line for k in ['handleTogglePump', 'M1', 'M2', 'M3', 'M4', 'M10', 'M11', 'M12', 'M13']):
        if '<g' in line or '<circle' in line:
            print(f"Line {i+1}: {line.strip()[:100]}")
