import re

with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Look for orange lines (#D97706) in ScadaSchematicSimulation.tsx
lines = code.split('\n')
for i, line in enumerate(lines):
    if '#D97706' in line:
        print(f"L{i+1}: {line.strip()[:100]}")
