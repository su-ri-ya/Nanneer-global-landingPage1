import os
import shutil

BASE_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets"

FOLDERS = {
    "tanks": [
        "collection-tank", "aeration-tank", "clarifier-tank", "sludge-holding-tank",
        "filter-feed-tank", "treated-water-tank", "soft-water-tank", "flash-mixer-tank",
        "flocculator-tank", "horizontal-storage-tank", "rainwater-pond"
    ],
    "filters": [
        "pressure-sand-filter", "activated-carbon-filter", "water-softener",
        "multi-grade-filter", "micron-cartridge", "ro-membrane", "uf-ultrafiltration",
        "sludge-filter-press", "lamella-tube-settler", "daf-flotation"
    ],
    "pumps": [
        "centrifugal-pump", "ro-high-pressure-pump", "chemical-dosing-pump", "submersible-sump-pump"
    ],
    "pipes": [
        "pipe-"
    ],
    "valves": [
        "solenoid-valve", "multiport-valve", "check-valve", "manual-isolation-valve"
    ],
    "instruments-utilities": [
        "aeration-blower", "cooling-tower", "uv-disinfection", "flow-meter",
        "level-sensor", "pressure-gauge", "water-tanker", "commercial-building"
    ]
}

# Create subdirectories
for folder in FOLDERS.keys():
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

files = [f for f in os.listdir(BASE_DIR) if f.endswith(".svg")]
moved_counts = {k: 0 for k in FOLDERS.keys()}

for f in files:
    src_path = os.path.join(BASE_DIR, f)
    if not os.path.isfile(src_path):
        continue

    assigned_folder = None
    # Check matching folder
    for folder, patterns in FOLDERS.items():
        if any(p in f for p in patterns):
            assigned_folder = folder
            break

    if assigned_folder:
        dest_path = os.path.join(BASE_DIR, assigned_folder, f)
        shutil.move(src_path, dest_path)
        moved_counts[assigned_folder] += 1
    else:
        print(f"Warning: unclassified file {f}")

print("Folder organization complete:")
for folder, count in moved_counts.items():
    print(f"  + {folder}/: {count} SVGs")
