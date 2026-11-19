import os
import re

BASE_DIR = 'public/schematic-assets'
PIPES_DIR = os.path.join(BASE_DIR, 'pipes')

COLORS = [
    {
        'id': 'water',
        'desc': 'Treated / Process Water',
        'fluid': '#0284c7',
        'pulse': '#bae6fd'
    },
    {
        'id': 'sewage',
        'desc': 'Raw Influent / Sewage',
        'fluid': '#8d6e63',
        'pulse': '#d7ccc8'
    },
    {
        'id': 'air',
        'desc': 'Aeration / Blower Compressed Air',
        'fluid': '#d97706',
        'pulse': '#fde68a'
    },
    {
        'id': 'sludge',
        'desc': 'Sludge / RAS / WAS Return',
        'fluid': '#dc2626',
        'pulse': '#fca5a5'
    },
    {
        'id': 'chemical',
        'desc': 'Chemical Dosing (Hypo, Alum, PAC)',
        'fluid': '#16a34a',
        'pulse': '#bbf7d0'
    },
    {
        'id': 'permeate',
        'desc': 'RO Permeate Pure Water',
        'fluid': '#06b6d4',
        'pulse': '#67e8f9'
    },
    {
        'id': 'brine',
        'desc': 'RO Reject / High TDS Drain',
        'fluid': '#ea580c',
        'pulse': '#fed7aa'
    }
]

# Definitions of all pipe shapes with paths & collars
SHAPES = {
    'horizontal-flow-left-to-right': {
        'path': 'M 0 100 L 200 100',
        'arrow': '<polygon points="108,97 116,100 108,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'horizontal-flow-right-to-left': {
        'path': 'M 200 100 L 0 100',
        'arrow': '<polygon points="92,97 84,100 92,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 0; } to { stroke-dashoffset: 24; }'
    },
    'vertical-flow-top-to-bottom': {
        'path': 'M 100 0 L 100 200',
        'arrow': '<polygon points="97,108 100,116 103,108" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'vertical-flow-bottom-to-top': {
        'path': 'M 100 200 L 100 0',
        'arrow': '<polygon points="97,92 100,84 103,92" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 0; } to { stroke-dashoffset: 24; }'
    },
    # 8 Elbows
    'elbow-left-to-up': {
        'path': 'M 0 100 L 100 100 L 100 0',
        'arrow': '<polygon points="97,48 100,40 103,48" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-up-to-left': {
        'path': 'M 100 0 L 100 100 L 0 100',
        'arrow': '<polygon points="48,97 40,100 48,103" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (0, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-left-to-down': {
        'path': 'M 0 100 L 100 100 L 100 200',
        'arrow': '<polygon points="97,152 100,160 103,152" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-down-to-left': {
        'path': 'M 100 200 L 100 100 L 0 100',
        'arrow': '<polygon points="48,97 40,100 48,103" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (0, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-right-to-up': {
        'path': 'M 200 100 L 100 100 L 100 0',
        'arrow': '<polygon points="97,48 100,40 103,48" fill="{fluid}" />',
        'collars': [(196, 94.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-up-to-right': {
        'path': 'M 100 0 L 100 100 L 200 100',
        'arrow': '<polygon points="152,97 160,100 152,103" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-right-to-down': {
        'path': 'M 200 100 L 100 100 L 100 200',
        'arrow': '<polygon points="97,152 100,160 103,152" fill="{fluid}" />',
        'collars': [(196, 94.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-down-to-right': {
        'path': 'M 100 200 L 100 100 L 200 100',
        'arrow': '<polygon points="152,97 160,100 152,103" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    # Specialized Schematic Crossovers & Traps
    'bridge-over-left-to-right': {
        'path': 'M 0 100 L 65 100 L 65 65 L 135 65 L 135 100 L 200 100',
        'arrow': '<polygon points="108,62 116,65 108,68" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'bridge-under-left-to-right': {
        'path': 'M 0 100 L 65 100 L 65 135 L 135 135 L 135 100 L 200 100',
        'arrow': '<polygon points="108,132 116,135 108,138" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'inverted-u-bend': {
        'path': 'M 50 200 L 50 55 L 150 55 L 150 200',
        'arrow': '<polygon points="108,52 116,55 108,58" fill="{fluid}" />',
        'collars': [(44.5, 196, 11, 4), (144.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'u-trap': {
        'path': 'M 50 0 L 50 145 L 150 145 L 150 0',
        'arrow': '<polygon points="108,142 116,145 108,148" fill="{fluid}" />',
        'collars': [(44.5, 0, 11, 4), (144.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'jog-step-up-left-to-right': {
        'path': 'M 0 140 L 70 140 L 130 60 L 200 60',
        'arrow': '<polygon points="168,57 176,60 168,63" fill="{fluid}" />',
        'collars': [(0, 134.5, 4, 11), (196, 54.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'jog-step-down-left-to-right': {
        'path': 'M 0 60 L 70 60 L 130 140 L 200 140',
        'arrow': '<polygon points="168,137 176,140 168,143" fill="{fluid}" />',
        'collars': [(0, 54.5, 4, 11), (196, 134.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    # 4 Tees
    'tee-branch-up': {
        'path': 'M 0 100 L 200 100 M 100 100 L 100 0',
        'arrow': '<polygon points="97,48 100,40 103,48" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-branch-down': {
        'path': 'M 0 100 L 200 100 M 100 100 L 100 200',
        'arrow': '<polygon points="97,152 100,160 103,152" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-branch-left': {
        'path': 'M 100 0 L 100 200 M 100 100 L 0 100',
        'arrow': '<polygon points="48,97 40,100 48,103" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4), (0, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-branch-right': {
        'path': 'M 100 0 L 100 200 M 100 100 L 200 100',
        'arrow': '<polygon points="152,97 160,100 152,103" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    # Cross 4-Way
    'cross-4way': {
        'path': 'M 0 100 L 200 100 M 100 0 L 100 200',
        'arrow': '<polygon points="108,97 116,100 108,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (94.5, 0, 11, 4), (94.5, 196, 11, 4)],
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

def generate_pipes():
    print("=== GENERATING COMPLETE MATRIX OF PIPES (SHAPES & COLORS) ===")
    
    # 1. Create subfolders for each color
    for c in COLORS:
        c_dir = os.path.join(PIPES_DIR, c['id'])
        os.makedirs(c_dir, exist_ok=True)
    
    dry_dir = os.path.join(PIPES_DIR, 'dry')
    os.makedirs(dry_dir, exist_ok=True)

    created_count = 0

    # 2. Generate dry pipes (one per shape)
    for s_name, s_cfg in SHAPES.items():
        collars_svg = render_collars(s_cfg['collars'])
        dry_xml = TEMPLATE_DRY.format(path=s_cfg['path'], collars_svg=collars_svg)
        
        # Save in pipes/dry/
        dry_path = os.path.join(dry_dir, f"pipe-{s_name}-dry-static.svg")
        with open(dry_path, 'w', encoding='utf-8') as f:
            f.write(dry_xml.strip() + '\n')
        created_count += 1
        
        # Also ensure root pipes/ has the dry pipe
        root_dry_path = os.path.join(PIPES_DIR, f"pipe-{s_name}-dry-static.svg")
        with open(root_dry_path, 'w', encoding='utf-8') as f:
            f.write(dry_xml.strip() + '\n')

    # 3. Generate fluid pipes for all 7 colors
    for c in COLORS:
        c_dir = os.path.join(PIPES_DIR, c['id'])
        for s_name, s_cfg in SHAPES.items():
            collars_svg = render_collars(s_cfg['collars'])
            arrow = s_cfg['arrow'].format(fluid=c['fluid'])

            # Animated
            anim_xml = TEMPLATE_ANIM.format(
                anim_dir=s_cfg['anim_dir'],
                path=s_cfg['path'],
                fluid=c['fluid'],
                pulse=c['pulse'],
                arrow=arrow,
                collars_svg=collars_svg
            )
            anim_path = os.path.join(c_dir, f"pipe-{s_name}-fluid-animated.svg")
            with open(anim_path, 'w', encoding='utf-8') as f:
                f.write(anim_xml.strip() + '\n')
            created_count += 1

            # Static
            static_xml = TEMPLATE_STATIC.format(
                path=s_cfg['path'],
                fluid=c['fluid'],
                collars_svg=collars_svg
            )
            static_path = os.path.join(c_dir, f"pipe-{s_name}-fluid-static.svg")
            with open(static_path, 'w', encoding='utf-8') as f:
                f.write(static_xml.strip() + '\n')
            created_count += 1

            # If water (default), also mirror in root pipes/
            if c['id'] == 'water':
                root_anim = os.path.join(PIPES_DIR, f"pipe-{s_name}-fluid-animated.svg")
                root_static = os.path.join(PIPES_DIR, f"pipe-{s_name}-fluid-static.svg")
                with open(root_anim, 'w', encoding='utf-8') as f:
                    f.write(anim_xml.strip() + '\n')
                with open(root_static, 'w', encoding='utf-8') as f:
                    f.write(static_xml.strip() + '\n')

    print(f"Generated {created_count} pipe asset files across 8 dedicated categories!")

if __name__ == '__main__':
    generate_pipes()
