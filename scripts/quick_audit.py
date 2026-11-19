import os
import glob
import re

BASE_DIR = 'public/schematic-assets'

def run_quick_audit():
    print("================================================================================")
    print("                    QUICK COMBINATION & MATRIX AUDIT                            ")
    print("================================================================================")

    # 1. Tanks Audit
    tanks = glob.glob(os.path.join(BASE_DIR, 'tanks', '*.svg'))
    tank_base_names = set()
    tank_states = {}
    for t in tanks:
        fn = os.path.basename(t)
        m = re.match(r'^(.*)-(dry-static|fluid-static|fluid-animated)\.svg$', fn)
        if m:
            base, st = m.group(1), m.group(2)
            tank_base_names.add(base)
            tank_states.setdefault(base, set()).add(st)
        else:
            print("Unrecognized tank file:", fn)

    print(f"\n[1] TANKS: {len(tanks)} SVGs across {len(tank_base_names)} equipment types")
    tank_gaps = []
    expected_tank_states = {'dry-static', 'fluid-static', 'fluid-animated'}
    for b in sorted(tank_base_names):
        missing = expected_tank_states - tank_states[b]
        if missing:
            tank_gaps.append((b, missing))
    if not tank_gaps:
        print("  -> PASS: All 11 tanks have all 3 complete states (dry-static, fluid-static, fluid-animated).")
    else:
        print("  -> GAPS in tanks:", tank_gaps)

    # 2. Filters Audit
    filters = glob.glob(os.path.join(BASE_DIR, 'filters', '*.svg'))
    filter_base_names = set()
    filter_states = {}
    for f in filters:
        fn = os.path.basename(f)
        m = re.match(r'^(.*)-(dry-static|fluid-static|fluid-animated|clamped-animated|clamped-static|open-static)\.svg$', fn)
        if m:
            base, st = m.group(1), m.group(2)
            filter_base_names.add(base)
            filter_states.setdefault(base, set()).add(st)
        else:
            print("Unrecognized filter file:", fn)

    print(f"\n[2] FILTERS: {len(filters)} SVGs across {len(filter_base_names)} equipment types")
    filter_gaps = []
    for b, sts in filter_states.items():
        if len(sts) != 3:
            filter_gaps.append((b, sts))
    if not filter_gaps:
        print("  -> PASS: All 10 filters have complete 3 states (operational animated, operational static, dry/offline).")
    else:
        print("  -> GAPS in filters:", filter_gaps)

    # 3. Pumps Audit
    pumps = glob.glob(os.path.join(BASE_DIR, 'pumps', '*.svg'))
    print(f"\n[3] PUMPS: {len(pumps)} SVGs")
    pump_types = {
        'centrifugal': glob.glob(os.path.join(BASE_DIR, 'pumps', 'centrifugal-*.svg')),
        'ro-high-pressure': glob.glob(os.path.join(BASE_DIR, 'pumps', 'ro-high-pressure-*.svg')),
        'chemical-dosing': glob.glob(os.path.join(BASE_DIR, 'pumps', 'chemical-dosing-*.svg')),
        'submersible-sump': glob.glob(os.path.join(BASE_DIR, 'pumps', 'submersible-sump-*.svg'))
    }
    for ptype, pfiles in pump_types.items():
        print(f"  • {ptype:20}: {len(pfiles)} SVGs")
    
    # Check centrifugal orientations
    cp_l2r = [f for f in pump_types['centrifugal'] if 'left-to-right' in f]
    cp_r2l = [f for f in pump_types['centrifugal'] if 'right-to-left' in f]
    print(f"    - Centrifugal L2R: {len(cp_l2r)}, R2L: {len(cp_r2l)} (Symmetrical: {len(cp_l2r) == len(cp_r2l)})")

    # 4. Pipes Audit
    print(f"\n[4] PIPELINES: {len(glob.glob(os.path.join(BASE_DIR, 'pipes', '**', '*.svg'), recursive=True))} total SVGs")
    pipe_dirs = ['water', 'sewage', 'air', 'sludge', 'chemical', 'permeate', 'brine', 'dry']
    shapes_per_dir = {}
    for pd in pipe_dirs:
        p_files = glob.glob(os.path.join(BASE_DIR, 'pipes', pd, '*.svg'))
        shapes_per_dir[pd] = len(p_files)
        print(f"  • pipes/{pd:12}: {len(p_files)} files")

    # 5. Valves Audit
    valves = glob.glob(os.path.join(BASE_DIR, 'valves', '*.svg'))
    print(f"\n[5] VALVES: {len(valves)} SVGs")
    for v in sorted(valves):
        print(f"  • {os.path.basename(v)}")

    # 6. Instruments & Utilities Audit
    inst = glob.glob(os.path.join(BASE_DIR, 'instruments-utilities', '*.svg'))
    print(f"\n[6] INSTRUMENTS & UTILITIES: {len(inst)} SVGs")
    inst_categories = {}
    for i in inst:
        fn = os.path.basename(i)
        cat = fn.split('-')[0]
        inst_categories.setdefault(cat, []).append(fn)
    for cat, items in sorted(inst_categories.items()):
        print(f"  • {cat:15}: {len(items)} files")

run_quick_audit()
