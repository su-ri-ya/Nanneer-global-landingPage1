import re

with open('components/ScadaSchematicSimulation.tsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Extract lines between each tank definition
tank_ids = ['tank-collection', 'tank-mbbr', 'tank-clarifier', 'tank-sludge', 'tank-filter-feed', 'tank-treated', 'tank-soft-water']

for tid in tank_ids:
    pattern = r'(<g id="' + tid + r'"[\s\S]*?)(?=<g id="tank-|<g id="blower|<g id="pump|<g id="filter|\n\s*\{/\*|\Z)'
    match = re.search(pattern, code)
    if match:
        print(f"==================== {tid} ====================")
        # Print without telemetry labels/text
        text = match.group(1)
        # Clean out React variables and telemetry
        print(text[:1200])
