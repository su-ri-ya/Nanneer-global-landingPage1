with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in ScadaSchematicSimulation.tsx: {len(lines)}")

# Find where pipelines start and end
recording = False
pipe_lines = []
for i, line in enumerate(lines):
    if 'PIPELINE NETWORK' in line:
        recording = True
    if 'EQUIPMENT & TANKS' in line or '1. COLLECTION TANK' in line:
        recording = False
    if recording:
        pipe_lines.append((i + 1, line))

print(f"Pipeline network section spans {len(pipe_lines)} lines")
with open('scripts/extracted_schematic_pipelines.txt', 'w', encoding='utf-8') as out:
    for num, l in pipe_lines:
        out.write(f"{num:4}: {l}")

print("Saved to scripts/extracted_schematic_pipelines.txt")
