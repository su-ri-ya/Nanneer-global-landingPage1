import os

BASE_DIR = 'public/schematic-assets'
PIPES_DIR = os.path.join(BASE_DIR, 'pipes')

COLORS = [
    {'id': 'water', 'desc': 'Treated / Process Water', 'fluid': '#0284c7', 'pulse': '#bae6fd'},
    {'id': 'sewage', 'desc': 'Raw Influent / Sewage', 'fluid': '#8d6e63', 'pulse': '#d7ccc8'},
    {'id': 'air', 'desc': 'Aeration / Blower Compressed Air', 'fluid': '#d97706', 'pulse': '#fde68a'},
    {'id': 'sludge', 'desc': 'Sludge / RAS / WAS Return', 'fluid': '#dc2626', 'pulse': '#fca5a5'},
    {'id': 'chemical', 'desc': 'Chemical Dosing (Hypo, Alum, PAC)', 'fluid': '#16a34a', 'pulse': '#bbf7d0'},
    {'id': 'permeate', 'desc': 'RO Permeate Pure Water', 'fluid': '#06b6d4', 'pulse': '#67e8f9'},
    {'id': 'brine', 'desc': 'RO Reject / High TDS Drain', 'fluid': '#ea580c', 'pulse': '#fed7aa'}
]

SHAPES = {
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
    'nozzle-stub-spool-horizontal': {
        'path': 'M 0 100 L 100 100',
        'arrow': '<polygon points="50,97 58,100 50,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (96, 92, 5, 16)],
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

def main():
    print("=== GENERATING 10 REMAINING SCHEMATIC PIPES ACROSS ALL COLORS ===")
    dry_dir = os.path.join(PIPES_DIR, 'dry')
    total = 0

    for s_name, s_cfg in SHAPES.items():
        collars_svg = render_collars(s_cfg['collars'])
        dry_xml = TEMPLATE_DRY.format(path=s_cfg['path'], collars_svg=collars_svg)

        # 1. Dry static in dry/ and root pipes/
        with open(os.path.join(dry_dir, f"pipe-{s_name}-dry-static.svg"), 'w', encoding='utf-8') as f:
            f.write(dry_xml.strip() + '\n')
        with open(os.path.join(PIPES_DIR, f"pipe-{s_name}-dry-static.svg"), 'w', encoding='utf-8') as f:
            f.write(dry_xml.strip() + '\n')
        total += 1

        # 2. 7 Process Fluid Colors
        for c in COLORS:
            c_dir = os.path.join(PIPES_DIR, c['id'])
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
            total += 1

            # Static
            static_xml = TEMPLATE_STATIC.format(
                path=s_cfg['path'],
                fluid=c['fluid'],
                collars_svg=collars_svg
            )
            with open(os.path.join(c_dir, f"pipe-{s_name}-fluid-static.svg"), 'w', encoding='utf-8') as f:
                f.write(static_xml.strip() + '\n')
            total += 1

            # Mirror water in root pipes/
            if c['id'] == 'water':
                with open(os.path.join(PIPES_DIR, f"pipe-{s_name}-fluid-animated.svg"), 'w', encoding='utf-8') as f:
                    f.write(anim_xml.strip() + '\n')
                with open(os.path.join(PIPES_DIR, f"pipe-{s_name}-fluid-static.svg"), 'w', encoding='utf-8') as f:
                    f.write(static_xml.strip() + '\n')

    print(f"SUCCESS: Generated {total} files across all 7 colors and dry!")

if __name__ == '__main__':
    main()
