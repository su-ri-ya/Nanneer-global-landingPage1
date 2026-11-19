import os

BASE_DIR = 'public/schematic-assets'
PIPES_DIR = os.path.join(BASE_DIR, 'pipes')

COLORS = [
    {
        'id': 'blue',
        'fluid': '#0284c7',
        'pulse': '#bae6fd'
    },
    {
        'id': 'brown',
        'fluid': '#8d6e63',
        'pulse': '#d7ccc8'
    },
    {
        'id': 'green',
        'fluid': '#16a34a',
        'pulse': '#bbf7d0'
    }
]

# Positional Straight Pipes & Stubs Across All Sides & Tracks
STRAIGHT_POSITION_SHAPES = {
    # 1. Horizontal Straights Across Top (y=48), Center (y=100), Bottom (y=150)
    'straight-horizontal-top-left-to-right': {
        'path': 'M 0 48 L 200 48',
        'arrow': '<polygon points="105,45 113,48 105,51" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (196, 42.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'straight-horizontal-top-right-to-left': {
        'path': 'M 200 48 L 0 48',
        'arrow': '<polygon points="95,51 87,48 95,45" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (196, 42.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'straight-horizontal-center-left-to-right': {
        'path': 'M 0 100 L 200 100',
        'arrow': '<polygon points="105,97 113,100 105,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'straight-horizontal-center-right-to-left': {
        'path': 'M 200 100 L 0 100',
        'arrow': '<polygon points="95,103 87,100 95,97" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'straight-horizontal-bottom-left-to-right': {
        'path': 'M 0 150 L 200 150',
        'arrow': '<polygon points="105,147 113,150 105,153" fill="{fluid}" />',
        'collars': [(0, 144.5, 4, 11), (196, 144.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'straight-horizontal-bottom-right-to-left': {
        'path': 'M 200 150 L 0 150',
        'arrow': '<polygon points="95,153 87,150 95,147" fill="{fluid}" />',
        'collars': [(0, 144.5, 4, 11), (196, 144.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # 2. Vertical Straights Across Left Column (x=48), Center (x=100), Right Column (x=150)
    'straight-vertical-left-top-to-bottom': {
        'path': 'M 48 0 L 48 200',
        'arrow': '<polygon points="45,105 48,113 51,105" fill="{fluid}" />',
        'collars': [(42.5, 0, 11, 4), (42.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'straight-vertical-left-bottom-to-top': {
        'path': 'M 48 200 L 48 0',
        'arrow': '<polygon points="45,95 48,87 51,95" fill="{fluid}" />',
        'collars': [(42.5, 0, 11, 4), (42.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'straight-vertical-center-top-to-bottom': {
        'path': 'M 100 0 L 100 200',
        'arrow': '<polygon points="97,105 100,113 103,105" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'straight-vertical-center-bottom-to-top': {
        'path': 'M 100 200 L 100 0',
        'arrow': '<polygon points="97,95 100,87 103,95" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'straight-vertical-right-top-to-bottom': {
        'path': 'M 150 0 L 150 200',
        'arrow': '<polygon points="147,105 150,113 153,105" fill="{fluid}" />',
        'collars': [(144.5, 0, 11, 4), (144.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'straight-vertical-right-bottom-to-top': {
        'path': 'M 150 200 L 150 0',
        'arrow': '<polygon points="147,95 150,87 153,95" fill="{fluid}" />',
        'collars': [(144.5, 0, 11, 4), (144.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # 3. Connection Stubs (Half Length)
    'stub-horizontal-top-left': {
        'path': 'M 0 48 L 100 48',
        'arrow': '<polygon points="50,45 58,48 50,51" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (96, 40.5, 5, 15)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'stub-horizontal-top-right': {
        'path': 'M 100 48 L 200 48',
        'arrow': '<polygon points="145,45 153,48 145,51" fill="{fluid}" />',
        'collars': [(100, 40.5, 5, 15), (196, 42.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'stub-horizontal-center-left': {
        'path': 'M 0 100 L 100 100',
        'arrow': '<polygon points="50,97 58,100 50,103" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (96, 92.5, 5, 15)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'stub-horizontal-center-right': {
        'path': 'M 100 100 L 200 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(100, 92.5, 5, 15), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'stub-horizontal-bottom-left': {
        'path': 'M 0 150 L 100 150',
        'arrow': '<polygon points="50,147 58,150 50,153" fill="{fluid}" />',
        'collars': [(0, 144.5, 4, 11), (96, 142.5, 5, 15)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'stub-horizontal-bottom-right': {
        'path': 'M 100 150 L 200 150',
        'arrow': '<polygon points="145,147 153,150 145,153" fill="{fluid}" />',
        'collars': [(100, 142.5, 5, 15), (196, 144.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'stub-vertical-top-drop': {
        'path': 'M 100 0 L 100 100',
        'arrow': '<polygon points="97,50 100,58 103,50" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (92.5, 96, 15, 5)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'stub-vertical-bottom-rise': {
        'path': 'M 100 200 L 100 100',
        'arrow': '<polygon points="97,150 100,142 103,150" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (92.5, 96, 15, 5)],
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

def render_collars(collar_list):
    res = []
    for x, y, w, h in collar_list:
        res.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
    return '\n  '.join(res)

def main():
    print("=== GENERATING POSITIONAL STRAIGHT PIPES ACROSS BLUE, BROWN, GREEN ===")
    total = 0

    for s_name, s_cfg in STRAIGHT_POSITION_SHAPES.items():
        collars_svg = render_collars(s_cfg['collars'])

        for c in COLORS:
            c_dir = os.path.join(PIPES_DIR, c['id'])
            arrow = s_cfg['arrow'].format(fluid=c['fluid'])

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

            static_xml = TEMPLATE_STATIC.format(
                path=s_cfg['path'],
                fluid=c['fluid'],
                collars_svg=collars_svg
            )
            with open(os.path.join(c_dir, f"pipe-{s_name}-fluid-static.svg"), 'w', encoding='utf-8') as f:
                f.write(static_xml.strip() + '\n')
            total += 1

    print(f"SUCCESS: Generated {total} positional straight pipe SVGs across Blue, Brown, and Green!")

if __name__ == '__main__':
    main()
