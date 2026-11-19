import os

POSITIONS = [
    ("top-left", 48, 48),
    ("top-center", 48, 100),
    ("top-right", 48, 150),
    ("center-left", 100, 48),
    ("center-center", 100, 100),
    ("center-right", 100, 150),
    ("bottom-left", 150, 48),
    ("bottom-center", 150, 100),
    ("bottom-right", 150, 150),
]

COLORS = {
    "blue": {
        "core": "#0284c7",
        "dash": "#bae6fd",
    },
    "brown": {
        "core": "#8d6e63",
        "dash": "#d7ccc8",
    },
    "green": {
        "core": "#16a34a",
        "dash": "#bbf7d0",
    },
}

BASE_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets\pipes"

def get_arrow_coords(y, x):
    # Horizontal arrow pointing right
    if x == 48:
        h_arrow = f'points="135,{y-3} 143,{y} 135,{y+3}"'
    elif x == 100:
        h_arrow = f'points="155,{y-3} 163,{y} 155,{y+3}"'
    else: # 150
        h_arrow = f'points="85,{y-3} 93,{y} 85,{y+3}"'

    # Vertical arrow pointing down
    if y == 48:
        v_arrow = f'points="{x-3},135 {x},143 {x+3},135"'
    elif y == 100:
        v_arrow = f'points="{x-3},155 {x},163 {x+3},155"'
    else: # 150
        v_arrow = f'points="{x-3},85 {x},93 {x+3},85"'

    return h_arrow, v_arrow

def generate_static_svg(y, x, core_color):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
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
  <path d="M 0 {y} L 200 {y} M {x} 0 L {x} 200" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  <!-- 4px Process Fluid Core -->
  <path d="M 0 {y} L 200 {y} M {x} 0 L {x} 200" stroke="{core_color}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="0" y="{y - 5.5}" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="196" y="{y - 5.5}" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="{x - 5.5}" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="{x - 5.5}" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""

def generate_animated_svg(y, x, core_color, dash_color):
    h_arrow, v_arrow = get_arrow_coords(y, x)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
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
  </defs>
  <!-- 7px Stainless Steel 316 Outer Casing with 3D Drop Shadow -->
  <path d="M 0 {y} L 200 {y} M {x} 0 L {x} 200" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  <!-- 4px Process Fluid Core -->
  <path d="M 0 {y} L 200 {y} M {x} 0 L {x} 200" stroke="{core_color}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- 2.5px Animated Flow Dashes -->
  <path d="M 0 {y} L 200 {y} M {x} 0 L {x} 200" stroke="{dash_color}" stroke-width="2.5" fill="none" stroke-linejoin="round" stroke-linecap="round" class="anim-p-flow"/>
  <polygon {h_arrow} fill="{core_color}" /><polygon {v_arrow} fill="{core_color}" />
  <rect x="0" y="{y - 5.5}" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="196" y="{y - 5.5}" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="{x - 5.5}" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
  <rect x="{x - 5.5}" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>
</svg>"""

total_created = 0
for color, c_data in COLORS.items():
    color_dir = os.path.join(BASE_DIR, color)
    os.makedirs(color_dir, exist_ok=True)
    for name, y, x in POSITIONS:
        # File naming: pipe-cross-4way-{name}-fluid-static.svg & animated.svg
        static_file = os.path.join(color_dir, f"pipe-cross-4way-{name}-fluid-static.svg")
        anim_file = os.path.join(color_dir, f"pipe-cross-4way-{name}-fluid-animated.svg")
        
        static_content = generate_static_svg(y, x, c_data["core"])
        anim_content = generate_animated_svg(y, x, c_data["core"], c_data["dash"])
        
        with open(static_file, "w", encoding="utf-8") as f:
            f.write(static_content)
        with open(anim_file, "w", encoding="utf-8") as f:
            f.write(anim_content)
            
        total_created += 2
        print(f"[{color}] Created {name} (static & animated)")

print(f"Successfully generated {total_created} 4-way cross SVG pipe files!")
