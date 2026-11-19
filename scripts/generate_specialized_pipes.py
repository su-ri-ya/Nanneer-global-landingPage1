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

# 16 Specialized Engineering Pipe Shapes
SPECIALIZED_SHAPES = {
    # 1. Dual Duty/Standby Pump Manifolds
    'manifold-dual-pump-suction-splitter': {
        'path': 'M 100 0 L 100 60 M 50 60 L 150 60 M 50 60 L 50 200 M 150 60 L 150 200',
        'arrow': '<polygon points="97,35 100,43 103,35" fill="{fluid}" /><polygon points="47,145 50,153 53,145" fill="{fluid}" /><polygon points="147,145 150,153 153,145" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (44.5, 196, 11, 4), (144.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'manifold-dual-pump-discharge-combiner': {
        'path': 'M 50 200 L 50 100 L 150 100 L 150 200 M 100 100 L 100 0',
        'arrow': '<polygon points="47,155 50,147 53,155" fill="{fluid}" /><polygon points="147,155 150,147 153,155" fill="{fluid}" /><polygon points="97,55 100,47 103,55" fill="{fluid}" />',
        'collars': [(44.5, 196, 11, 4), (144.5, 196, 11, 4), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 0; } to { stroke-dashoffset: 24; }'
    },
    'manifold-dual-blower-interconnect': {
        'path': 'M 0 60 L 70 60 L 70 140 L 0 140 M 70 100 L 200 100',
        'arrow': '<polygon points="35,57 43,60 35,63" fill="{fluid}" /><polygon points="35,137 43,140 35,143" fill="{fluid}" /><polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(0, 54.5, 4, 11), (0, 134.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    # 2. Dual Bypass Loops
    'dual-bypass-loop-left-to-right': {
        'path': 'M 0 100 L 50 100 L 75 50 L 125 50 L 150 100 L 200 100 M 50 100 L 75 150 L 125 150 L 150 100',
        'arrow': '<polygon points="98,47 106,50 98,53" fill="{fluid}" /><polygon points="98,147 106,150 98,153" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'dual-bypass-loop-right-to-left': {
        'path': 'M 200 100 L 150 100 L 125 50 L 75 50 L 50 100 L 0 100 M 150 100 L 125 150 L 75 150 L 50 100',
        'arrow': '<polygon points="102,47 94,50 102,53" fill="{fluid}" /><polygon points="102,147 94,150 102,153" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 0; } to { stroke-dashoffset: 24; }'
    },
    # 3. Multi-Tap Distribution Headers
    'header-dual-tap-drop': {
        'path': 'M 0 100 L 200 100 M 70 100 L 70 200 M 140 100 L 140 200',
        'arrow': '<polygon points="105,97 113,100 105,103" fill="{fluid}" /><polygon points="67,155 70,163 73,155" fill="{fluid}" /><polygon points="137,155 140,163 143,155" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (64.5, 196, 11, 4), (134.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'header-triple-tap-drop': {
        'path': 'M 0 100 L 200 100 M 50 100 L 50 200 M 100 100 L 100 200 M 150 100 L 150 200',
        'arrow': '<polygon points="175,97 183,100 175,103" fill="{fluid}" /><polygon points="47,155 50,163 53,155" fill="{fluid}" /><polygon points="97,155 100,163 103,155" fill="{fluid}" /><polygon points="147,155 150,163 153,155" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (44.5, 196, 11, 4), (94.5, 196, 11, 4), (144.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    # 4. 45° Lateral Wyes
    'wye-45-branch-up-left-to-right': {
        'path': 'M 0 100 L 200 100 M 70 100 L 150 20',
        'arrow': '<polygon points="105,97 113,100 105,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (145, 16, 10, 8)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'wye-45-branch-down-left-to-right': {
        'path': 'M 0 100 L 200 100 M 70 100 L 150 180',
        'arrow': '<polygon points="105,97 113,100 105,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (145, 176, 10, 8)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'wye-45-symmetric-flow-join': {
        'path': 'M 30 30 L 100 100 L 200 100 M 30 170 L 100 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(26, 26, 10, 8), (26, 166, 10, 8), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    # 5. Floor Trench & Overhead Gantry
    'floor-trench-u-run': {
        'path': 'M 40 0 L 40 160 L 160 160 L 160 0',
        'arrow': '<polygon points="98,157 106,160 98,163" fill="{fluid}" />',
        'collars': [(34.5, 0, 11, 4), (154.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'overhead-gantry-run': {
        'path': 'M 40 200 L 40 40 L 160 40 L 160 200',
        'arrow': '<polygon points="98,37 106,40 98,43" fill="{fluid}" />',
        'collars': [(34.5, 196, 11, 4), (154.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    # 6. Pipe End Caps & Concentric Reducers
    'end-cap-horizontal-left': {
        'path': 'M 200 100 L 50 100',
        'arrow': '<polygon points="125,97 117,100 125,103" fill="{fluid}" />',
        'collars': [(196, 94.5, 4, 11), (46, 92, 6, 16)],
        'anim_dir': 'from { stroke-dashoffset: 0; } to { stroke-dashoffset: 24; }'
    },
    'end-cap-horizontal-right': {
        'path': 'M 0 100 L 150 100',
        'arrow': '<polygon points="75,97 83,100 75,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (148, 92, 6, 16)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'reducer-concentric-large-to-small': {
        'path': 'M 0 100 L 90 100 M 110 100 L 200 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(0, 93, 5, 14), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'reducer-concentric-small-to-large': {
        'path': 'M 0 100 L 90 100 M 110 100 L 200 100',
        'arrow': '<polygon points="45,97 53,100 45,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 93, 5, 14)],
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

def generate_specialized():
    print("=== GENERATING 16 SPECIALIZED PIPING COMBINATIONS ===")
    dry_dir = os.path.join(PIPES_DIR, 'dry')
    total_new = 0

    # 1. Dry files
    for s_name, s_cfg in SPECIALIZED_SHAPES.items():
        collars_svg = render_collars(s_cfg['collars'])
        dry_xml = TEMPLATE_DRY.format(path=s_cfg['path'], collars_svg=collars_svg)
        
        # In pipes/dry/
        with open(os.path.join(dry_dir, f"pipe-{s_name}-dry-static.svg"), 'w', encoding='utf-8') as f:
            f.write(dry_xml.strip() + '\n')
        total_new += 1

        # Also in root pipes/
        with open(os.path.join(PIPES_DIR, f"pipe-{s_name}-dry-static.svg"), 'w', encoding='utf-8') as f:
            f.write(dry_xml.strip() + '\n')

    # 2. Fluid files across 7 colors
    for c in COLORS:
        c_dir = os.path.join(PIPES_DIR, c['id'])
        for s_name, s_cfg in SPECIALIZED_SHAPES.items():
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
            with open(os.path.join(c_dir, f"pipe-{s_name}-fluid-animated.svg"), 'w', encoding='utf-8') as f:
                f.write(anim_xml.strip() + '\n')
            total_new += 1

            # Static
            static_xml = TEMPLATE_STATIC.format(
                path=s_cfg['path'],
                fluid=c['fluid'],
                collars_svg=collars_svg
            )
            with open(os.path.join(c_dir, f"pipe-{s_name}-fluid-static.svg"), 'w', encoding='utf-8') as f:
                f.write(static_xml.strip() + '\n')
            total_new += 1

            # If water, also mirror in root pipes/
            if c['id'] == 'water':
                with open(os.path.join(PIPES_DIR, f"pipe-{s_name}-fluid-animated.svg"), 'w', encoding='utf-8') as f:
                    f.write(anim_xml.strip() + '\n')
                with open(os.path.join(PIPES_DIR, f"pipe-{s_name}-fluid-static.svg"), 'w', encoding='utf-8') as f:
                    f.write(static_xml.strip() + '\n')

    print(f"Generated {total_new} specialized piping assets across all 7 colors + dry!")

if __name__ == '__main__':
    generate_specialized()
