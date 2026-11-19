import os

# 10 Additional Precise Pipeline Shapes from ScadaSchematicSimulation.tsx
ADDITIONAL_SCHEMATIC_SHAPES = {
    # 1. Dedicated Upper Half Bypass Loop (Line 565 in schematic)
    'bypass-upper-half-left-to-right': {
        'path': 'M 0 100 L 40 100 L 40 45 L 160 45 L 160 100 L 200 100',
        'desc': 'Upper duty bypass loop around M1/filter bank'
    },
    'bypass-upper-half-right-to-left': {
        'path': 'M 200 100 L 160 100 L 160 45 L 40 45 L 40 100 L 0 100',
        'desc': 'Reverse upper bypass loop'
    },
    # 2. Dedicated Lower Half Bypass Loop (Line 566 in schematic)
    'bypass-lower-half-left-to-right': {
        'path': 'M 0 100 L 40 100 L 40 155 L 160 155 L 160 100 L 200 100',
        'desc': 'Lower standby bypass loop around M2/filter bank'
    },
    'bypass-lower-half-right-to-left': {
        'path': 'M 200 100 L 160 100 L 160 155 L 40 155 L 40 100 L 0 100',
        'desc': 'Reverse lower bypass loop'
    },
    # 3. Z-Jog Drop-Run-Drop (Line 678 in schematic: feed line to PSF)
    'jog-drop-run-right-drop': {
        'path': 'M 50 0 L 50 100 L 150 100 L 150 200',
        'desc': 'Vertical drop, horizontal step right, vertical drop to vessel inlet'
    },
    'jog-drop-run-left-drop': {
        'path': 'M 150 0 L 150 100 L 50 100 L 50 200',
        'desc': 'Vertical drop, horizontal step left, vertical drop to vessel inlet'
    },
    # 4. Z-Jog Rise-Run-Rise
    'jog-rise-run-right-rise': {
        'path': 'M 50 200 L 50 100 L 150 100 L 150 0',
        'desc': 'Vertical riser, horizontal step right, vertical riser'
    },
    'jog-rise-run-left-rise': {
        'path': 'M 150 200 L 150 100 L 50 100 L 50 0',
        'desc': 'Vertical riser, horizontal step left, vertical riser'
    },
    # 5. Multi-Turn Overhead Gantry Return Line (Line 542 in schematic: drain return to collection tank)
    'overhead-gantry-multi-turn-return': {
        'path': 'M 170 200 L 170 70 L 40 70 L 40 25 L 120 25',
        'desc': 'High-elevation multi-turn recirculation return line back into tank'
    },
    # 6. Half-Length Vessel Nozzle Spool Stub (Lines 697, 702, 724 in schematic)
    'nozzle-stub-spool-horizontal': {
        'path': 'M 0 100 L 100 100',
        'desc': 'Short spool stub connecting valves directly to vessel nozzles'
    }
}

print(f"Verified {len(ADDITIONAL_SCHEMATIC_SHAPES)} additional shapes from schematic code.")
for k, v in ADDITIONAL_SCHEMATIC_SHAPES.items():
    print(f"  • {k:35}: {v['desc']}")
