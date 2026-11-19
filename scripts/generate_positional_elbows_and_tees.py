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

SHAPES = {
    # =========================================================================
    # 1. TOP CORNERS (Header at y = 48)
    # =========================================================================
    'elbow-top-left-to-down': {
        'path': 'M 0 48 L 100 48 L 100 200',
        'arrow': '<polygon points="97,125 100,133 103,125" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-top-down-to-left': {
        'path': 'M 100 200 L 100 48 L 0 48',
        'arrow': '<polygon points="55,51 47,48 55,45" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (0, 42.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-top-right-to-down': {
        'path': 'M 200 48 L 100 48 L 100 200',
        'arrow': '<polygon points="97,125 100,133 103,125" fill="{fluid}" />',
        'collars': [(196, 42.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-top-down-to-right': {
        'path': 'M 100 200 L 100 48 L 200 48',
        'arrow': '<polygon points="145,45 153,48 145,51" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (196, 42.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # =========================================================================
    # 2. CENTER CORNERS (Header at y = 100)
    # =========================================================================
    'elbow-center-left-to-up': {
        'path': 'M 0 100 L 100 100 L 100 0',
        'arrow': '<polygon points="97,55 100,47 103,55" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-center-up-to-left': {
        'path': 'M 100 0 L 100 100 L 0 100',
        'arrow': '<polygon points="55,103 47,100 55,97" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (0, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-center-left-to-down': {
        'path': 'M 0 100 L 100 100 L 100 200',
        'arrow': '<polygon points="97,145 100,153 103,145" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-center-down-to-left': {
        'path': 'M 100 200 L 100 100 L 0 100',
        'arrow': '<polygon points="55,103 47,100 55,97" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (0, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-center-right-to-up': {
        'path': 'M 200 100 L 100 100 L 100 0',
        'arrow': '<polygon points="97,55 100,47 103,55" fill="{fluid}" />',
        'collars': [(196, 94.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-center-up-to-right': {
        'path': 'M 100 0 L 100 100 L 200 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-center-right-to-down': {
        'path': 'M 200 100 L 100 100 L 100 200',
        'arrow': '<polygon points="97,145 100,153 103,145" fill="{fluid}" />',
        'collars': [(196, 94.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-center-down-to-right': {
        'path': 'M 100 200 L 100 100 L 200 100',
        'arrow': '<polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(94.5, 196, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # =========================================================================
    # 3. BOTTOM CORNERS (Header at y = 150)
    # =========================================================================
    'elbow-bottom-left-to-up': {
        'path': 'M 0 150 L 100 150 L 100 0',
        'arrow': '<polygon points="97,75 100,67 103,75" fill="{fluid}" />',
        'collars': [(0, 144.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-bottom-up-to-left': {
        'path': 'M 100 0 L 100 150 L 0 150',
        'arrow': '<polygon points="55,153 47,150 55,147" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (0, 144.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-bottom-right-to-up': {
        'path': 'M 200 150 L 100 150 L 100 0',
        'arrow': '<polygon points="97,75 100,67 103,75" fill="{fluid}" />',
        'collars': [(196, 144.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elbow-bottom-up-to-right': {
        'path': 'M 100 0 L 100 150 L 200 150',
        'arrow': '<polygon points="145,147 153,150 145,153" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (196, 144.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # =========================================================================
    # 4. T-BRANCHES (Top y=48, Center y=100, Bottom y=150)
    # =========================================================================
    'tee-top-header-branch-down': {
        'path': 'M 0 48 L 200 48 M 100 48 L 100 200',
        'arrow': '<polygon points="155,45 163,48 155,51" fill="{fluid}" /><polygon points="97,135 100,143 103,135" fill="{fluid}" />',
        'collars': [(0, 42.5, 4, 11), (196, 42.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-center-header-branch-up': {
        'path': 'M 0 100 L 200 100 M 100 100 L 100 0',
        'arrow': '<polygon points="155,97 163,100 155,103" fill="{fluid}" /><polygon points="97,55 100,47 103,55" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-center-header-branch-down': {
        'path': 'M 0 100 L 200 100 M 100 100 L 100 200',
        'arrow': '<polygon points="155,97 163,100 155,103" fill="{fluid}" /><polygon points="97,145 100,153 103,145" fill="{fluid}" />',
        'collars': [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (94.5, 196, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-bottom-header-branch-up': {
        'path': 'M 0 150 L 200 150 M 100 150 L 100 0',
        'arrow': '<polygon points="155,147 163,150 155,153" fill="{fluid}" /><polygon points="97,75 100,67 103,75" fill="{fluid}" />',
        'collars': [(0, 144.5, 4, 11), (196, 144.5, 4, 11), (94.5, 0, 11, 4)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-vertical-center-branch-left': {
        'path': 'M 100 0 L 100 200 M 100 100 L 0 100',
        'arrow': '<polygon points="97,155 100,163 103,155" fill="{fluid}" /><polygon points="55,103 47,100 55,97" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4), (0, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'tee-vertical-center-branch-right': {
        'path': 'M 100 0 L 100 200 M 100 100 L 200 100',
        'arrow': '<polygon points="97,155 100,163 103,155" fill="{fluid}" /><polygon points="145,97 153,100 145,103" fill="{fluid}" />',
        'collars': [(94.5, 0, 11, 4), (94.5, 196, 11, 4), (196, 94.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },

    # =========================================================================
    # 5. 4-WAY CROSS
    # =========================================================================
    'cross-4way-center': {
        'path': 'M 0 100 L 200 100 M 100 0 L 100 200',
        'arrow': '<polygon points="155,97 163,100 155,103" fill="{fluid}" /><polygon points="97,155 100,163 103,155" fill="{fluid}" />',
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

def render_collars(collar_list):
    res = []
    for x, y, w, h in collar_list:
        res.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>')
    return '\n  '.join(res)

def main():
    print("=== GENERATING POSITIONAL ELBOWS & TEES ACROSS BLUE, BROWN, GREEN ===")
    total = 0

    for s_name, s_cfg in SHAPES.items():
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

    print(f"SUCCESS: Generated {total} positional elbow & tee SVGs across Blue, Brown, and Green!")

if __name__ == '__main__':
    main()
