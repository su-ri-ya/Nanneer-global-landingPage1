import os

paths = [
    'public/schematic-assets/tanks/collection-tank-fluid-animated.svg',
    'public/schematic-assets/tanks/collection-tank-dry-static.svg',
    'public/schematic-assets/tanks/treated-water-tank-fluid-animated.svg',
    'public/schematic-assets/pipes/blue/pipe-straight-horizontal-center-left-to-right-fluid-animated.svg',
    'public/schematic-assets/pipes/blue/pipe-elbow-center-left-to-down-fluid-animated.svg',
    'public/schematic-assets/pipes/blue/pipe-straight-vertical-center-top-to-bottom-fluid-animated.svg',
    'public/schematic-assets/pipes/blue/pipe-elbow-center-down-to-left-fluid-animated.svg',
    'public/schematic-assets/pipes/blue/pipe-straight-horizontal-center-right-to-left-fluid-animated.svg',
    'public/schematic-assets/pumps/centrifugal-pump-dn100-flow-left-to-right-running-animated.svg',
    'public/schematic-assets/pumps/centrifugal-pump-dn100-flow-left-to-right-standby-static.svg',
    'public/schematic-assets/pumps/centrifugal-pump-dn100-flow-left-to-right-stopped-static.svg',
    'public/schematic-assets/pumps/centrifugal-pump-dn100-flow-left-to-right-fault-animated.svg',
    'public/schematic-assets/valves/solenoid-valve-active-animated.svg',
    'public/schematic-assets/valves/solenoid-valve-closed-static.svg',
    'public/schematic-assets/filters/sand-filter-vessel-fluid-animated.svg',
    'public/schematic-assets/instruments-utilities/flow-meter-active-animated.svg',
]

for p in paths:
    status = "EXISTS" if os.path.exists(p) else "MISSING"
    print(f"{p}: {status}")
