import re

with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

lines = code.split('\n')
for i, line in enumerate(lines):
    if 'handleTogglePump' in line:
        # print 5 lines around it
        start = max(0, i-2)
        end = min(len(lines), i+8)
        print(f"=== Match at line {i+1} ===")
        for j in range(start, end):
            print(f"  L{j+1}: {lines[j]}")
