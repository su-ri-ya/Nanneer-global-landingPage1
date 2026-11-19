import os
import shutil

BASE_DIR = 'public/schematic-assets'
PIPES_DIR = os.path.join(BASE_DIR, 'pipes')

# 3 Specified Colors
COLORS = [
    {
        'id': 'blue',
        'alias': 'water',
        'desc': 'Blue - Clean / Process / Treated Water',
        'fluid': '#0284c7',
        'pulse': '#bae6fd'
    },
    {
        'id': 'brown',
        'alias': 'sewage',
        'desc': 'Brown - Raw Influent / Sewage / Sludge',
        'fluid': '#8d6e63',
        'pulse': '#d7ccc8'
    },
    {
        'id': 'green',
        'alias': 'chemical',
        'desc': 'Green - Chemical Dosing / Treated Effluent',
        'fluid': '#16a34a',
        'pulse': '#bbf7d0'
    }
]

# Master Shapes Covering All Directions From Any Tank (Top, Center, Bottom, Above, Below, Left, Right)
ALL_SHAPES = {
    # =========================================================================
    # 1. CORE CARDINAL RUNS & ELBOWS (From Reference Photo)
    # =========================================================================
    'horizontal-straight-left-to-right': {
        'path': 'M 0 100 L 200 100',
        'arrow': '<polygon points="108,97 116,100 108,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'horizontal-straight-right-to-left': {
        'path': 'M 200 100 L 0 100',
        'arrow': '<polygon points="92,103 84,100 92,97" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'vertical-straight-top-to-bottom': {
        'path': 'M 100 0 L 100 200',
        'arrow': '<polygon points="97,108 100,116 103,108" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'vertical-straight-bottom-to-top': {
        'path': 'M 100 200 L 100 0',
        'arrow': '<polygon points="97,92 100,84 103,92" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-left-to-up': {
        'path': 'M 0 100 L 100 100 L 100 0',
        'arrow': '<polygon points="97,55 100,47 103,55" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-left-to-down': {
        'path': 'M 0 100 L 100 100 L 100 200',
        'arrow': '<polygon points="97,145 100,153 103,145" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-right-to-up': {
        'path': 'M 200 100 L 100 100 L 100 0',
        'arrow': '<polygon points="97,55 100,47 103,55" fill="{fluid}" />',
        'collars': [(196, 94.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-right-to-down': {
        'path': 'M 200 100 L 100 100 L 100 200',
        'arrow': '<polygon points="97,145 100,153 103,145" fill="{fluid}" />',
        'collars': [(196, 94.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-up-to-left': {
        'path': 'M 100 0 L 100 100 L 0 100',
        'arrow': '<polygon points="55,103 47,100 55,97" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (0, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-up-to-right': {
        'path': 'M 100 0 L 100 100 L 200 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-down-to-left': {
        'path': 'M 100 200 L 100 100 L 0 100',
        'arrow': '<polygon points="55,103 47,100 55,97" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (0, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-down-to-right': {
        'path': 'M 100 200 L 100 100 L 200 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-branch-up': {
        'path': 'M 0 100 L 200 100 M 100 100 L 100 0',
        'arrow': '<polygon points="155,97 163,100 155,103" fill="{fluid}" /><polygon points="97,55 100,47 103,55" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-branch-down': {
        'path': 'M 0 100 L 200 100 M 100 100 L 100 200',
        'arrow': '<polygon points="155,97 163,100 155,103" fill="{fluid}" /><polygon points="97,145 100,153 103,145" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-branch-left': {
        'path': 'M 100 0 L 100 200 M 100 100 L 0 100',
        'arrow': '<polygon points="97,155 100,163 103,155" fill="{fluid}" /><polygon points="55,103 47,100 55,97" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4), (0, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-branch-right': {
        'path': 'M 100 0 L 100 200 M 100 100 L 200 100',
        'arrow': '<polygon points="97,155 100,163 103,155" fill="{fluid}" /><polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'cross-4way': {
        'path': 'M 0 100 L 200 100 M 100 0 L 100 200',
        'arrow': '<polygon points="155,97 163,100 155,103" fill="{fluid}" /><polygon points="97,155 100,163 103,155" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (94.5, 0, 11, 4), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # =========================================================================
    # 2. TANK RIGHT-SIDE (EAST) COMBINATIONS (Top y=48, Center y=100, Bottom y=110)
    # =========================================================================
    'tank-right-top-straight': {
        'path': 'M 0 48 L 200 48',
        'arrow': '<polygon points="105,45 113,48 105,51" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (196, 42.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-right-top-turn-up': {
        'path': 'M 0 48 L 100 48 L 100 0',
        'arrow': '<polygon points="97,25 100,17 103,25" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-right-top-turn-down': {
        'path': 'M 0 48 L 100 48 L 100 200',
        'arrow': '<polygon points="97,125 100,133 103,125" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-right-top-step-to-center': {
        'path': 'M 0 48 L 80 48 L 80 100 L 200 100',
        'arrow': '<polygon points="135,97 143,100 135,103" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-right-center-straight': {
        'path': 'M 0 100 L 200 100',
        'arrow': '<polygon points="105,97 113,100 105,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-right-center-turn-up': {
        'path': 'M 0 100 L 100 100 L 100 0',
        'arrow': '<polygon points="97,55 100,47 103,55" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-right-center-turn-down': {
        'path': 'M 0 100 L 100 100 L 100 200',
        'arrow': '<polygon points="97,145 100,153 103,145" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-right-bottom-straight': {
        'path': 'M 0 110 L 200 110',
        'arrow': '<polygon points="105,107 113,110 105,113" fill="{fluid}" />',
        'collars': [(0, 104.5, 4, 11), (196, 104.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-right-bottom-turn-up': {
        'path': 'M 0 110 L 100 110 L 100 0',
        'arrow': '<polygon points="97,55 100,47 103,55" fill="{fluid}" />',
        'collars': [(0, 104.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-right-bottom-turn-down': {
        'path': 'M 0 110 L 100 110 L 100 200',
        'arrow': '<polygon points="97,155 100,163 103,155" fill="{fluid}" />',
        'collars': [(0, 104.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-right-bottom-step-to-center': {
        'path': 'M 0 110 L 80 110 L 80 100 L 200 100',
        'arrow': '<polygon points="135,97 143,100 135,103" fill="{fluid}" />',
        'collars': [(0, 104.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # =========================================================================
    # 3. TANK LEFT-SIDE (WEST) COMBINATIONS (Inflow Top y=48, Center y=100, Bottom y=110)
    # =========================================================================
    'tank-left-top-straight': {
        'path': 'M 0 48 L 200 48',
        'arrow': '<polygon points="105,45 113,48 105,51" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (196, 42.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-left-top-from-up': {
        'path': 'M 100 0 L 100 48 L 200 48',
        'arrow': '<polygon points="145,45 153,48 145,51" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (196, 42.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-left-top-from-down': {
        'path': 'M 100 200 L 100 48 L 200 48',
        'arrow': '<polygon points="145,45 153,48 145,51" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (196, 42.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-left-center-straight': {
        'path': 'M 0 100 L 200 100',
        'arrow': '<polygon points="105,97 113,100 105,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-left-center-from-up': {
        'path': 'M 100 0 L 100 100 L 200 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-left-center-from-down': {
        'path': 'M 100 200 L 100 100 L 200 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-left-center-step-from-top': {
        'path': 'M 0 48 L 80 48 L 80 100 L 200 100',
        'arrow': '<polygon points="135,97 143,100 135,103" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-left-center-step-from-bottom': {
        'path': 'M 0 110 L 80 110 L 80 100 L 200 100',
        'arrow': '<polygon points="135,97 143,100 135,103" fill="{fluid}" />',
        'collars': [(0, 104.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-left-bottom-straight': {
        'path': 'M 0 110 L 200 110',
        'arrow': '<polygon points="105,107 113,110 105,113" fill="{fluid}" />',
        'collars': [(0, 104.5, 4, 11), (196, 104.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-left-bottom-from-up': {
        'path': 'M 100 0 L 100 110 L 200 110',
        'arrow': '<polygon points="145,107 153,110 145,113" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (196, 104.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-left-bottom-from-down': {
        'path': 'M 100 200 L 100 110 L 200 110',
        'arrow': '<polygon points="145,107 153,110 145,113" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (196, 104.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # =========================================================================
    # 4. TANK TOP-SIDE (NORTH / ABOVE THE TANK)
    # =========================================================================
    'tank-top-vertical-drop-in': {
        'path': 'M 100 0 L 100 130',
        'arrow': '<polygon points="97,75 100,83 103,75" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 126, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-top-vertical-rise-out': {
        'path': 'M 100 130 L 100 0',
        'arrow': '<polygon points="97,55 100,47 103,55" fill="{fluid}" />',
        'collars': [(94.5, 126, 11, 4), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-top-drop-from-left': {
        'path': 'M 0 48 L 100 48 L 100 140',
        'arrow': '<polygon points="97,95 100,103 103,95" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (94.5, 136, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-top-drop-from-right': {
        'path': 'M 200 48 L 100 48 L 100 140',
        'arrow': '<polygon points="97,95 100,103 103,95" fill="{fluid}" />',
        'collars': [(196, 42.5, 4, 11), (94.5, 136, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-top-overhead-tee-drop': {
        'path': 'M 0 48 L 200 48 M 100 48 L 100 140',
        'arrow': '<polygon points="155,45 163,48 155,51" fill="{fluid}" /><polygon points="97,95 100,103 103,95" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (196, 42.5, 4, 11), (94.5, 136, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # =========================================================================
    # 5. TANK BELOW-SIDE (SOUTH / UNDERNEATH THE TANK)
    # =========================================================================
    'tank-below-vertical-drain': {
        'path': 'M 100 60 L 100 200',
        'arrow': '<polygon points="97,135 100,143 103,135" fill="{fluid}" />',
        'collars': [(94.5, 56, 11, 4), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-below-vertical-feed-in': {
        'path': 'M 100 200 L 100 60',
        'arrow': '<polygon points="97,115 100,107 103,115" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (94.5, 56, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-below-drain-turn-left': {
        'path': 'M 100 60 L 100 140 L 0 140',
        'arrow': '<polygon points="45,143 37,140 45,137" fill="{fluid}" />',
        'collars': [(94.5, 56, 11, 4), (0, 134.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-below-drain-turn-right': {
        'path': 'M 100 60 L 100 140 L 200 140',
        'arrow': '<polygon points="155,137 163,140 155,143" fill="{fluid}" />',
        'collars': [(94.5, 56, 11, 4), (196, 134.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tank-below-floor-tee-feed': {
        'path': 'M 0 140 L 200 140 M 100 140 L 100 60',
        'arrow': '<polygon points="155,137 163,140 155,143" fill="{fluid}" /><polygon points="97,105 100,97 103,105" fill="{fluid}" />',
        'collars': [(0, 134.5, 4, 11), (196, 134.5, 4, 11), (94.5, 56, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # =========================================================================
    # 6. BYPASSES, JOGS, MANIFOLDS & SPECIALTY SHAPES
    # =========================================================================
    'dual-bypass-loop-left-to-right': {
        'path': 'M 0 100 L 40 100 L 40 50 L 160 50 L 160 100 L 200 100 M 40 100 L 40 150 L 160 150 L 160 100',
        'arrow': '<polygon points="105,47 113,50 105,53" fill="{fluid}" /><polygon points="105,147 113,150 105,153" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'dual-bypass-loop-right-to-left': {
        'path': 'M 200 100 L 160 100 L 160 50 L 40 50 L 40 100 L 0 100 M 160 100 L 160 150 L 40 150 L 40 100',
        'arrow': '<polygon points="95,53 87,50 95,47" fill="{fluid}" /><polygon points="95,153 87,150 95,147" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'bypass-upper-half-left-to-right': {
        'path': 'M 0 100 L 40 100 L 40 45 L 160 45 L 160 100 L 200 100',
        'arrow': '<polygon points="105,42 113,45 105,48" fill="{fluid}" /><polygon points="175,97 183,100 175,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'bypass-upper-half-right-to-left': {
        'path': 'M 200 100 L 160 100 L 160 45 L 40 45 L 40 100 L 0 100',
        'arrow': '<polygon points="95,48 87,45 95,42" fill="{fluid}" /><polygon points="25,103 17,100 25,97" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'bypass-lower-half-left-to-right': {
        'path': 'M 0 100 L 40 100 L 40 155 L 160 155 L 160 100 L 200 100',
        'arrow': '<polygon points="105,152 113,155 105,158" fill="{fluid}" /><polygon points="175,97 183,100 175,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'bypass-lower-half-right-to-left': {
        'path': 'M 200 100 L 160 100 L 160 155 L 40 155 L 40 100 L 0 100',
        'arrow': '<polygon points="95,158 87,155 95,152" fill="{fluid}" /><polygon points="25,103 17,100 25,97" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'jog-drop-run-right-drop': {
        'path': 'M 50 0 L 50 100 L 150 100 L 150 200',
        'arrow': '<polygon points="105,97 113,100 105,103" fill="{fluid}" /><polygon points="147,155 150,163 153,155" fill="{fluid}" />',
        'collars': [(44.5, 0, 11, 4), (144.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'jog-drop-run-left-drop': {
        'path': 'M 150 0 L 150 100 L 50 100 L 50 200',
        'arrow': '<polygon points="95,103 87,100 95,97" fill="{fluid}" /><polygon points="47,155 50,163 53,155" fill="{fluid}" />',
        'collars': [(144.5, 0, 11, 4), (44.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'jog-rise-run-right-rise': {
        'path': 'M 50 200 L 50 100 L 150 100 L 150 0',
        'arrow': '<polygon points="105,97 113,100 105,103" fill="{fluid}" /><polygon points="147,45 150,37 153,45" fill="{fluid}" />',
        'collars': [(44.5, 196, 11, 4), (144.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'jog-rise-run-left-rise': {
        'path': 'M 150 200 L 150 100 L 50 100 L 50 0',
        'arrow': '<polygon points="95,103 87,100 95,97" fill="{fluid}" /><polygon points="47,45 50,37 53,45" fill="{fluid}" />',
        'collars': [(144.5, 196, 11, 4), (44.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'overhead-gantry-multi-turn-return': {
        'path': 'M 170 200 L 170 70 L 40 70 L 40 25 L 120 25',
        'arrow': '<polygon points="167,145 170,137 173,145" fill="{fluid}" /><polygon points="105,73 97,70 105,67" fill="{fluid}" /><polygon points="85,22 93,25 85,28" fill="{fluid}" />',
        'collars': [(164.5, 196, 11, 4), (116, 19.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    '3d-perpendicular-crossing': {
        'path': 'M 0 100 L 200 100 M 100 0 L 100 200',
        'arrow': '<polygon points="155,97 163,100 155,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (94.5, 0, 11, 4), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'bridge-over-left-to-right': {
        'path': 'M 0 100 L 60 100 Q 80 100 80 80 Q 80 60 100 60 Q 120 60 120 80 Q 120 100 140 100 L 200 100',
        'arrow': '<polygon points="105,57 113,60 105,63" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'end-cap-horizontal-left': {
        'path': 'M 196 100 L 20 100',
        'arrow': '<polygon points="105,103 97,100 105,97" fill="{fluid}" />',
        'collars': [(196, 94.5, 4, 11), (16, 92, 5, 16)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'end-cap-horizontal-right': {
        'path': 'M 0 100 L 180 100',
        'arrow': '<polygon points="95,97 103,100 95,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (180, 92, 5, 16)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'reducer-concentric-large-to-small': {
        'path': 'M 0 100 L 90 100 L 110 100 L 200 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(0, 93, 4, 14), (196, 95.5, 4, 9)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'reducer-concentric-small-to-large': {
        'path': 'M 0 100 L 90 100 L 110 100 L 200 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(0, 95.5, 4, 9), (196, 93, 4, 14)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    }
}

TEMPLATE_ANIM = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes p-flow-anim {{ {anim_dir} }}
      .anim-p-flow {{ stroke-dasharray: 5 7; animation: p-flow-anim 0.8s linear infinite; }}
    </style>
    <filter id="ssPipeShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
  </defs>
  <!-- 7px Stainless Steel 316 Outer Casing with 3D Drop Shadow -->
  <path d="{path}" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  <!-- 4px Process Fluid Core -->
  <path d="{path}" stroke="{fluid}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- 2.5px Animated Flow Dashes -->
  <path d="{path}" stroke="{pulse}" stroke-width="2.5" fill="none" stroke-linejoin="round" stroke-linecap="round" class="anim-p-flow"/>
  {arrow}
  {collars_svg}
</svg>"""

TEMPLATE_STATIC = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="ssPipeShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
  </defs>
  <!-- 7px Stainless Steel 316 Outer Casing with 3D Drop Shadow -->
  <path d="{path}" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  <!-- 4px Process Fluid Core -->
  <path d="{path}" stroke="{fluid}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  {collars_svg}
</svg>"""

TEMPLATE_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="ssPipeShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
  </defs>
  <!-- 7px Stainless Steel 316 Outer Casing (Empty / Dry) with 3D Drop Shadow -->
  <path d="{path}" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  {collars_svg}
</svg>"""

def render_collars(collar_list):
    res = []
    for x, y, w, h in collar_list:
        res.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
    return '\n  '.join(res)

def rebuild_pipes():
    print("=== DELETING PREVIOUS PIPES & GENERATING CLEAN NEW PIPELINE LIBRARY ===")
    
    # 1. Clean previous files in pipes directory
    if os.path.exists(PIPES_DIR):
        for root, dirs, files in os.walk(PIPES_DIR):
            for f in files:
                if f.endswith('.svg'):
                    os.remove(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d), ignore_errors=True)
    os.makedirs(PIPES_DIR, exist_ok=True)
    
    # Create subdirectories for blue, brown, green, and dry
    dirs_to_create = ['blue', 'brown', 'green', 'dry', 'water', 'sewage', 'chemical']
    for d in dirs_to_create:
        os.makedirs(os.path.join(PIPES_DIR, d), exist_ok=True)

    total_files = 0

    for s_name, s_cfg in ALL_SHAPES.items():
        collars_svg = render_collars(s_cfg['collars'])
        dry_xml = TEMPLATE_DRY.format(path=s_cfg['path'], collars_svg=collars_svg)

        # 1. Write Dry Static in dry/ and root pipes/
        dry_file = f"pipe-{s_name}-dry-static.svg"
        with open(os.path.join(PIPES_DIR, 'dry', dry_file), 'w', encoding='utf-8') as f:
            f.write(dry_xml.strip() + '\n')
        with open(os.path.join(PIPES_DIR, dry_file), 'w', encoding='utf-8') as f:
            f.write(dry_xml.strip() + '\n')
        total_files += 2

        # 2. Write 3 Colors: Blue, Brown, Green (both in color/ and alias/)
        for c in COLORS:
            anim_name = f"pipe-{s_name}-fluid-animated.svg"
            static_name = f"pipe-{s_name}-fluid-static.svg"
            arrow = s_cfg['arrow'].format(fluid=c['fluid'])

            anim_xml = TEMPLATE_ANIM.format(
                anim_dir=s_cfg['anim_dir'],
                path=s_cfg['path'],
                fluid=c['fluid'],
                pulse=c['pulse'],
                arrow=arrow,
                collars_svg=collars_svg
            )
            static_xml = TEMPLATE_STATIC.format(
                path=s_cfg['path'],
                fluid=c['fluid'],
                collars_svg=collars_svg
            )

            # In pipes/<color>/
            c_dir = os.path.join(PIPES_DIR, c['id'])
            with open(os.path.join(c_dir, anim_name), 'w', encoding='utf-8') as f:
                f.write(anim_xml.strip() + '\n')
            with open(os.path.join(c_dir, static_name), 'w', encoding='utf-8') as f:
                f.write(static_xml.strip() + '\n')
            total_files += 2

            # In alias directory (water, sewage, chemical)
            alias_dir = os.path.join(PIPES_DIR, c['alias'])
            with open(os.path.join(alias_dir, anim_name), 'w', encoding='utf-8') as f:
                f.write(anim_xml.strip() + '\n')
            with open(os.path.join(alias_dir, static_name), 'w', encoding='utf-8') as f:
                f.write(static_xml.strip() + '\n')
            total_files += 2

            # Mirror blue in root pipes/
            if c['id'] == 'blue':
                with open(os.path.join(PIPES_DIR, anim_name), 'w', encoding='utf-8') as f:
                    f.write(anim_xml.strip() + '\n')
                with open(os.path.join(PIPES_DIR, static_name), 'w', encoding='utf-8') as f:
                    f.write(static_xml.strip() + '\n')
                total_files += 2

    print(f"SUCCESS: Generated {total_files} pipe SVGs across Blue, Brown, Green, and Dry!")

if __name__ == '__main__':
    rebuild_pipes()
