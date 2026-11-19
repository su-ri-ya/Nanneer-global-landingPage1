import os
import shutil

ASSET_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets"

# Read all current files
files = os.listdir(ASSET_DIR)

rename_map = {}
copies_to_create = {}

for f in files:
    if not f.endswith(".svg"):
        continue

    new_name = f

    # 1. Pipes
    new_name = new_name.replace("pipe-straight-horizontal-flow-r2l-", "pipe-horizontal-flow-right-to-left-")
    new_name = new_name.replace("pipe-straight-horizontal-", "pipe-horizontal-flow-left-to-right-")
    new_name = new_name.replace("pipe-horizontal-flow-left-to-right-dry-static.svg", "pipe-horizontal-dry-static.svg")

    new_name = new_name.replace("pipe-straight-vertical-flow-b2t-", "pipe-vertical-flow-bottom-to-top-")
    new_name = new_name.replace("pipe-straight-vertical-", "pipe-vertical-flow-top-to-bottom-")
    new_name = new_name.replace("pipe-vertical-flow-top-to-bottom-dry-static.svg", "pipe-vertical-dry-static.svg")

    new_name = new_name.replace("pipe-elbow-left-up-", "pipe-elbow-left-to-up-")
    new_name = new_name.replace("pipe-elbow-up-left-", "pipe-elbow-up-to-left-")
    new_name = new_name.replace("pipe-elbow-left-down-", "pipe-elbow-left-to-down-")
    new_name = new_name.replace("pipe-elbow-down-left-", "pipe-elbow-down-to-left-")
    new_name = new_name.replace("pipe-elbow-right-up-", "pipe-elbow-right-to-up-")
    new_name = new_name.replace("pipe-elbow-up-right-", "pipe-elbow-up-to-right-")
    new_name = new_name.replace("pipe-elbow-right-down-", "pipe-elbow-right-to-down-")
    new_name = new_name.replace("pipe-elbow-down-right-", "pipe-elbow-down-to-right-")

    new_name = new_name.replace("pipe-tee-up-", "pipe-tee-branch-up-")
    new_name = new_name.replace("pipe-tee-down-", "pipe-tee-branch-down-")
    new_name = new_name.replace("pipe-tee-left-", "pipe-tee-branch-left-")
    new_name = new_name.replace("pipe-tee-right-", "pipe-tee-branch-right-")

    # 2. Pumps
    new_name = new_name.replace("pump-centrifugal-", "centrifugal-pump-")
    new_name = new_name.replace("pump-ro-high-pressure-", "ro-high-pressure-pump-")
    new_name = new_name.replace("pump-chemical-dosing-", "chemical-dosing-pump-")
    new_name = new_name.replace("pump-submersible-sump-", "submersible-sump-pump-")
    new_name = new_name.replace("flow-l2r-", "flow-left-to-right-")
    new_name = new_name.replace("flow-r2l-", "flow-right-to-left-")

    # 3. Blowers
    new_name = new_name.replace("blower-rotary-", "aeration-blower-")

    # 4. Filters & Vessels
    new_name = new_name.replace("filter-pressure-sand-psf-", "pressure-sand-filter-psf-")
    new_name = new_name.replace("filter-activated-carbon-acf-", "activated-carbon-filter-acf-")
    new_name = new_name.replace("filter-water-softener-resin-", "water-softener-resin-")
    new_name = new_name.replace("filter-cartridge-micron-", "micron-cartridge-filter-")
    new_name = new_name.replace("vessel-pressure-filter-frp-", "multi-grade-filter-mgf-")
    new_name = new_name.replace("skid-membrane-ro-", "ro-membrane-system-")
    new_name = new_name.replace("skid-membrane-uf-", "uf-ultrafiltration-system-")
    new_name = new_name.replace("press-sludge-filter-", "sludge-filter-press-")
    new_name = new_name.replace("settler-lamella-clarifier-", "lamella-tube-settler-")
    new_name = new_name.replace("tank-flotation-daf-", "daf-flotation-tank-")

    # 5. Utilities & Sensors
    new_name = new_name.replace("cooling-tower-induced-draft-", "cooling-tower-")
    new_name = new_name.replace("reactor-uv-disinfection-", "uv-disinfection-system-")
    new_name = new_name.replace("sensor-flow-meter-electromagnetic-", "flow-meter-")
    new_name = new_name.replace("sensor-level-transmitter-ultrasonic-", "level-sensor-")
    new_name = new_name.replace("gauge-analog-pressure-", "pressure-gauge-")
    new_name = new_name.replace("facility-commercial-building-static.svg", "commercial-building-consumer-static.svg")
    new_name = new_name.replace("supply-water-tanker-", "water-tanker-supply-")

    # 6. Valves
    new_name = new_name.replace("valve-solenoid-inline-", "solenoid-valve-")
    new_name = new_name.replace("valve-multiport-block-", "multiport-valve-block-")
    new_name = new_name.replace("valve-check-non-return-", "check-valve-nrv-")
    new_name = new_name.replace("valve-manual-isolation-", "manual-isolation-valve-")

    # 7. Tanks
    new_name = new_name.replace("tank-aeration-diffuser-", "aeration-tank-")
    new_name = new_name.replace("tank-cylindrical-horizontal-", "horizontal-storage-tank-")
    new_name = new_name.replace("basin-open-reservoir-", "rainwater-pond-")

    if f.startswith("tank-cylindrical-vertical-"):
        new_name = f.replace("tank-cylindrical-vertical-", "collection-tank-")
        # Also create copies for filter-feed-tank, treated-water-tank, soft-water-tank
        state = f.replace("tank-cylindrical-vertical-", "")
        copies_to_create[f] = [
            f"filter-feed-tank-{state}",
            f"treated-water-tank-{state}",
            f"soft-water-tank-{state}"
        ]

    if f.startswith("tank-conical-hopper-"):
        new_name = f.replace("tank-conical-hopper-", "clarifier-tank-")
        state = f.replace("tank-conical-hopper-", "")
        copies_to_create[f] = [
            f"sludge-holding-tank-{state}"
        ]

    if f.startswith("tank-agitator-mixer-"):
        new_name = f.replace("tank-agitator-mixer-", "flash-mixer-tank-")
        state = f.replace("tank-agitator-mixer-", "")
        copies_to_create[f] = [
            f"flocculator-tank-{state}"
        ]

    if new_name != f:
        rename_map[f] = new_name

print(f"Renaming {len(rename_map)} files to clear, natural plant names...")
for old_name, new_name in rename_map.items():
    old_path = os.path.join(ASSET_DIR, old_name)
    new_path = os.path.join(ASSET_DIR, new_name)
    if os.path.exists(old_path):
        # If target exists and differs only by case or target is same
        if old_path != new_path:
            shutil.move(old_path, new_path)

print(f"Creating {sum(len(v) for v in copies_to_create.values())} natural plant-specific tank aliases...")
for src_name, dest_names in copies_to_create.items():
    # If the source was renamed, find its new name
    real_src = rename_map.get(src_name, src_name)
    src_path = os.path.join(ASSET_DIR, real_src)
    if os.path.exists(src_path):
        for d in dest_names:
            dest_path = os.path.join(ASSET_DIR, d)
            shutil.copyfile(src_path, dest_path)
            print(f"  + Created {d}")

print("All assets successfully renamed to understandable plant names!")
