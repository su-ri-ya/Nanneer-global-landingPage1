import os

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

STEP_DROP_SHAPES = {
    'elevated-step-down-drop-tee-left': {
        'path': 'M 0 140 L 200 140 M 0 60 L 100 60 L 100 140',
        'arrow': '<polygon points="155,137 163,140 155,143" fill="{fluid}" /><polygon points="97,105 100,113 103,105" fill="{fluid}" />',
        'collars': [(0, 134.5, 4, 11), (196, 134.5, 4, 11), (0, 54.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'elevated-step-down-drop-tee-right': {
        'path': 'M 0 140 L 200 140 M 200 60 L 100 60 L 100 140',
        'arrow': '<polygon points="55,137 63,140 55,143" fill="{fluid}" /><polygon points="97,105 100,113 103,105" fill="{fluid}" />',
        'collars': [(0, 134.5, 4, 11), (196, 134.5, 4, 11), (196, 54.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'bottom-riser-step-up-tee-left': {
        'path': 'M 0 60 L 200 60 M 0 140 L 100 140 L 100 60',
        'arrow': '<polygon points="155,57 163,60 155,63" fill="{fluid}" /><polygon points="97,95 100,87 103,95" fill="{fluid}" />',
        'collars': [(0, 54.5, 4, 11), (196, 54.5, 4, 11), (0, 134.5, 4, 11)],
        'anim_dir': 'from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }'
    },
    'bottom-riser-step-up-tee-right': {
        'path': 'M 0 60 L 200 60 M 200 140 L 100 140 L 100 60',
        'arrow': '<polygon points="55,57 63,60 55,63" fill="{fluid}" /><polygon points="97,95 100,87 103,95" fill="{fluid}" />',
        'collars': [(0, 54.5, 4, 11), (196, 54.5, 4, 11), (196, 134.5, 4, 11)],
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

def generate_step_pipes():
    print("=== GENERATING ELEVATED STEP-DOWN & RISER PIPES ===")
    dry_dir = os.path.join(PIPES_DIR, 'dry')
    total = 0

    # 1. Step-Down & Riser Pipes
    for s_name, s_cfg in STEP_DROP_SHAPES.items():
        collars_svg = render_collars(s_cfg['collars'])
        dry_xml = TEMPLATE_DRY.format(path=s_cfg['path'], collars_svg=collars_svg)
        
        # Dry
        with open(os.path.join(dry_dir, f"pipe-{s_name}-dry-static.svg"), 'w', encoding='utf-8') as f:
            f.write(dry_xml.strip() + '\n')
        with open(os.path.join(PIPES_DIR, f"pipe-{s_name}-dry-static.svg"), 'w', encoding='utf-8') as f:
            f.write(dry_xml.strip() + '\n')
        total += 1

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

            if c['id'] == 'water':
                with open(os.path.join(PIPES_DIR, f"pipe-{s_name}-fluid-animated.svg"), 'w', encoding='utf-8') as f:
                    f.write(anim_xml.strip() + '\n')
                with open(os.path.join(PIPES_DIR, f"pipe-{s_name}-fluid-static.svg"), 'w', encoding='utf-8') as f:
                    f.write(static_xml.strip() + '\n')

    # 2. 3D Non-Intersecting Perpendicular Crossing Fitting
    print("Generating 3D Non-Intersecting Perpendicular Crossover Pipes...")
    collars_cross = [(0, 94.5, 4, 11), (196, 94.5, 4, 11), (94.5, 0, 11, 4), (94.5, 196, 11, 4)]
    collars_cross_svg = render_collars(collars_cross)

    # Crossing Dry
    cross_dry = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="ssPipeShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
    <linearGradient id="ssPipeGradV" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
  </defs>
  <!-- Lower Underpass Vertical Pipe -->
  <path d="M 100 0 L 100 200" stroke="url(#ssPipeGradV)" stroke-width="7" fill="none" stroke-linecap="round"/>
  <!-- Elevation Shadow Cutout between Pipes -->
  <rect x="91" y="91" width="18" height="18" fill="#0f172a" opacity="0.4" filter="url(#ssPipeShadow)"/>
  <!-- Upper Overpass Horizontal Pipe Casting Shadow on Lower Pipe -->
  <path d="M 0 100 L 200 100" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round" filter="url(#ssPipeShadow)"/>
  {collars_cross_svg}
</svg>"""
    with open(os.path.join(dry_dir, "pipe-3d-perpendicular-crossing-dry-static.svg"), 'w', encoding='utf-8') as f:
        f.write(cross_dry.strip() + '\n')
    with open(os.path.join(PIPES_DIR, "pipe-3d-perpendicular-crossing-dry-static.svg"), 'w', encoding='utf-8') as f:
        f.write(cross_dry.strip() + '\n')
    total += 1

    # Crossing across 7 colors
    for c in COLORS:
        c_dir = os.path.join(PIPES_DIR, c['id'])
        
        cross_anim = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes p-flow-anim {{ from {{ stroke-dashoffset: 24; }} to {{ stroke-dashoffset: 0; }} }}
      .anim-p-flow {{ stroke-dasharray: 5 7; animation: p-flow-anim 0.8s linear infinite; }}
    </style>
    <filter id="ssPipeShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
    <linearGradient id="ssPipeGradV" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
  </defs>
  <!-- Lower Underpass Vertical Pipe (Background Line) -->
  <path d="M 100 0 L 100 200" stroke="url(#ssPipeGradV)" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M 100 0 L 100 200" stroke="{c['fluid']}" stroke-width="4" fill="none" stroke-linecap="round"/>
  <!-- Elevation Contact Shadow Cutout -->
  <rect x="91" y="91" width="18" height="18" fill="#0f172a" opacity="0.45" filter="url(#ssPipeShadow)"/>
  <!-- Upper Overpass Horizontal Pipe (Foreground Line Crossing Over) -->
  <path d="M 0 100 L 200 100" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round" filter="url(#ssPipeShadow)"/>
  <path d="M 0 100 L 200 100" stroke="{c['fluid']}" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M 0 100 L 200 100" stroke="{c['pulse']}" stroke-width="2.5" fill="none" stroke-linecap="round" class="anim-p-flow"/>
  <polygon points="108,97 116,100 108,103" fill="{c['fluid']}"/>
  {collars_cross_svg}
</svg>"""
        with open(os.path.join(c_dir, "pipe-3d-perpendicular-crossing-fluid-animated.svg"), 'w', encoding='utf-8') as f:
            f.write(cross_anim.strip() + '\n')
        total += 1

        cross_static = cross_anim.replace('class="anim-p-flow"', '')
        with open(os.path.join(c_dir, "pipe-3d-perpendicular-crossing-fluid-static.svg"), 'w', encoding='utf-8') as f:
            f.write(cross_static.strip() + '\n')
        total += 1

        if c['id'] == 'water':
            with open(os.path.join(PIPES_DIR, "pipe-3d-perpendicular-crossing-fluid-animated.svg"), 'w', encoding='utf-8') as f:
                f.write(cross_anim.strip() + '\n')
            with open(os.path.join(PIPES_DIR, "pipe-3d-perpendicular-crossing-fluid-static.svg"), 'w', encoding='utf-8') as f:
                f.write(cross_static.strip() + '\n')

    print(f"Generated {total} new step drop, riser tee, and non-intersecting crossing pipes!")

if __name__ == '__main__':
    generate_step_pipes()
