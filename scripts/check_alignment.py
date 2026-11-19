import os
import glob
import re
import xml.etree.ElementTree as ET

BASE_DIR = 'public/schematic-assets'

def check_alignment():
    print("=== CHECKING CONNECTION ALIGNMENT & SNAPPING ===")
    
    # 1. Pipes alignment
    pipes = glob.glob(os.path.join(BASE_DIR, 'pipes', '*.svg'))
    for p in sorted(pipes):
        fname = os.path.basename(p)
        content = open(p).read()
        # Find paths with M/L coordinates
        coords = re.findall(r'[ML]\s*([\d\.]+)\s+([\d\.]+)', content)
        # Check boundary intersections (0 or 200)
        boundary_pts = [(float(x), float(y)) for x, y in coords if float(x) in (0, 200) or float(y) in (0, 200)]
        # print first 3 as sample
        if 'horizontal' in fname and 'fluid-animated' in fname:
            print(f"Horizontal pipe: boundary pts = {boundary_pts}")
        elif 'elbow-down-to-right' in fname and 'fluid-animated' in fname:
            print(f"Elbow down-to-right: boundary pts = {boundary_pts}")
        elif 'tee-branch-up' in fname and 'fluid-animated' in fname:
            print(f"Tee branch-up: boundary pts = {boundary_pts}")

    # 2. Centrifugal Pumps
    pumps = glob.glob(os.path.join(BASE_DIR, 'pumps', 'centrifugal*dn25*l2r*running-animated.svg'))
    for p in pumps:
        content = open(p).read()
        # check suction at x=0
        has_suction_0 = 'M 0 132' in content or 'M 0,132' in content or 'x="0"' in content
        # check discharge at top
        has_discharge = 'y="0"' in content or 'M 132 0' in content or 'M 132,0' in content
        print(f"Centrifugal L2R Pump: suction at x=0: {has_suction_0}, discharge at y=0: {has_discharge}")

    # 3. Check valves
    valves = glob.glob(os.path.join(BASE_DIR, 'valves', '*.svg'))
    print(f"Total Valves: {len(valves)}")

    # 4. Check instruments & utilities
    instruments = glob.glob(os.path.join(BASE_DIR, 'instruments-utilities', '*.svg'))
    print(f"Total Instruments & Utilities: {len(instruments)}")

check_alignment()
