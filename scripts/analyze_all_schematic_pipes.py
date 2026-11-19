import re

with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Look for pipeline blocks
# In ScadaSchematicSimulation, pipelines start around line 512
lines = code.split('\n')
pipe_sections = []
recording = False
current_section = "General"

for i, line in enumerate(lines):
    if '{/* PIPELINE NETWORK' in line:
        recording = True
    if '{/* EQUIPMENT & TANKS' in line or '{/* 1. COLLECTION TANK' in line:
        recording = False
    
    if recording:
        if '{/*' in line and '*/}' in line:
            current_section = line.strip()
        if '<path' in line and ' d=' in line:
            d_match = re.search(r'd=["`{]([^"`}]+)["`}]', line)
            stroke_match = re.search(r'stroke=["`{]([^"`}]+)["`}]', line)
            stroke_w = re.search(r'strokeWidth=["`{]([^"`}]+)["`}]', line)
            if d_match:
                pipe_sections.append((i+1, current_section, d_match.group(1), stroke_match.group(1) if stroke_match else 'none', stroke_w.group(1) if stroke_w else 'none'))

print(f"Total pipeline paths found in PIPELINE NETWORK section: {len(pipe_sections)}")
for ln, sec, d, s, sw in pipe_sections:
    print(f"L{ln:4} | {sec[:35]:35} | stroke={s:15} | w={sw:4} | d={d}")
