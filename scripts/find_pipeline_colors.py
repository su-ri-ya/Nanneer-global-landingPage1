import re

with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Find lines with pipelines and comments describing them
lines = code.split('\n')
for i, line in enumerate(lines):
    if any(k in line for k in ['Pipeline', 'pipeline', 'Line', 'line', 'stroke="#', 'stroke={', 'url(#ssPipe']):
        if any(c in line for c in ['#0284C7', '#16A34A', '#8D6E63', '#D97706', '#DC2626', 'ssPipe']):
            print(f"Line {i+1}: {line.strip()[:100]}")
