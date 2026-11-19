import os
import shutil

OUTPUT_DIR = os.path.join("public", "schematic asserts", "pipe")

# Clean existing directory to ensure only requested files and color folders exist
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 4 Colors + Dry Steel
COLORS = {
    "blue": {
        "fluid": "#0284C7",
        "pulse": "#BAE6FD",
        "desc": "Treated Water / Clean Effluent"
    },
    "brown": {
        "fluid": "#8D6E63",
        "pulse": "#D7CCC8",
        "desc": "Raw Sewage / Sludge"
    },
    "red": {
        "fluid": "#DC2626",
        "pulse": "#FCA5A5",
        "desc": "Drain / Reject / Backwash"
    },
    "green": {
        "fluid": "#16A34A",
        "pulse": "#BBF7D0",
        "desc": "Chemical Dosing / Bio-Stream"
    }
}

# Create color-wise folders
for c in list(COLORS.keys()) + ["dry"]:
    os.makedirs(os.path.join(OUTPUT_DIR, c), exist_ok=True)

# Tracks (Top: y=48, Center: y=100, Bottom: y=140)
# (Left: x=48, Center: x=100, Right: x=150)
Y_TRACKS = [("top", 48), ("center", 100), ("bottom", 140)]
X_TRACKS = [("left", 48), ("center", 100), ("right", 150)]

# Collar helpers
def collar_h(x, y):
    if x <= 10:
        return f'<rect x="0" y="{y - 5.5}" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'
    else:
        return f'<rect x="196" y="{y - 5.5}" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'

def collar_v(x, y):
    if y <= 10:
        return f'<rect x="{x - 5.5}" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'
    else:
        return f'<rect x="{x - 5.5}" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'

def arrow_h(x, y, to_right=True, color="{fluid}"):
    if to_right:
        return f'<polygon points="{x-4},{y-3} {x+4},{y} {x-4},{y+3}" fill="{color}" />'
    else:
        return f'<polygon points="{x+4},{y-3} {x-4},{y} {x+4},{y+3}" fill="{color}" />'

def arrow_v(x, y, to_down=True, color="{fluid}"):
    if to_down:
        return f'<polygon points="{x-3},{y-4} {x},{y+4} {x+3},{y-4}" fill="{color}" />'
    else:
        return f'<polygon points="{x-3},{y+4} {x},{y-4} {x+3},{y+4}" fill="{color}" />'

TEMPLATE_ANIMATED = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <style>
      @keyframes p-flow-anim {{
        {anim_dir}
      }}
      .anim-p-flow {{
        stroke-dasharray: 6 8;
        animation: p-flow-anim 0.8s linear infinite;
      }}
    </style>
    <filter id="ssPipeShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
  </defs>

  <!-- Stainless Steel 316 Outer Casing (8px with 3D Drop Shadow) -->
  <path d="{path}" stroke="url(#ssPipeGradH)" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>

  <!-- Process Fluid Core (5px) -->
  <path d="{path}" stroke="{fluid}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Animated Fluid Flow Stream Dashes (2.5px) -->
  <path d="{path}" stroke="{pulse}" stroke-width="2.5" fill="none" stroke-linejoin="round" stroke-linecap="round" class="anim-p-flow"/>

  <!-- Directional Flow Arrow -->
  {arrow}

  <!-- ANSI Flange Connection Collars -->
  {collars}
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

  <!-- Stainless Steel 316 Outer Casing (8px with 3D Drop Shadow) -->
  <path d="{path}" stroke="url(#ssPipeGradH)" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>

  <!-- Process Fluid Core (5px) -->
  <path d="{path}" stroke="{fluid}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- ANSI Flange Connection Collars -->
  {collars}
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

  <!-- Stainless Steel 316 Outer Casing (Dry / Empty) -->
  <path d="{path}" stroke="url(#ssPipeGradH)" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>

  <!-- ANSI Flange Connection Collars -->
  {collars}
</svg>"""

# Dictionary to hold all shape configurations
ALL_SHAPES = {}

# =============================================================================
# 1. POSITIONAL STRAIGHT PIPES (Top y=48, Center y=100, Bottom y=140)
# =============================================================================
for y_name, y in Y_TRACKS:
    # Forward (Left to Right)
    name_fwd = f"straight-horizontal-{y_name}-left-to-right"
    ALL_SHAPES[name_fwd] = {
        "path": f"M 0 {y} L 200 {y}",
        "collars": [collar_h(0, y), collar_h(200, y)],
        "arrow": arrow_h(100, y, to_right=True),
        "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
    }
    # Reverse (Right to Left)
    name_rev = f"straight-horizontal-{y_name}-right-to-left"
    ALL_SHAPES[name_rev] = {
        "path": f"M 200 {y} L 0 {y}",
        "collars": [collar_h(0, y), collar_h(200, y)],
        "arrow": arrow_h(100, y, to_right=False),
        "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
    }
    # Alias for center
    if y_name == "center":
        ALL_SHAPES["straight-horizontal"] = ALL_SHAPES[name_fwd]
        ALL_SHAPES["straight-horizontal-reverse"] = ALL_SHAPES[name_rev]

# Positional Vertical Straights (Left x=48, Center x=100, Right x=150)
for x_name, x in X_TRACKS:
    # Forward (Top to Bottom)
    name_fwd = f"straight-vertical-{x_name}-top-to-bottom"
    ALL_SHAPES[name_fwd] = {
        "path": f"M {x} 0 L {x} 200",
        "collars": [collar_v(x, 0), collar_v(x, 200)],
        "arrow": arrow_v(x, 100, to_down=True),
        "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
    }
    # Reverse (Bottom to Top)
    name_rev = f"straight-vertical-{x_name}-bottom-to-top"
    ALL_SHAPES[name_rev] = {
        "path": f"M {x} 200 L {x} 0",
        "collars": [collar_v(x, 0), collar_v(x, 200)],
        "arrow": arrow_v(x, 100, to_down=False),
        "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
    }
    if x_name == "center":
        ALL_SHAPES["straight-vertical"] = ALL_SHAPES[name_fwd]
        ALL_SHAPES["straight-vertical-reverse"] = ALL_SHAPES[name_rev]

# =============================================================================
# 2. POSITIONAL 90° ELBOWS (Connecting all (y, x) tracks)
# =============================================================================
for y_name, y in Y_TRACKS:
    for x_name, x in X_TRACKS:
        # Elbow: Left to Up (W -> N)
        name_l_u = f"elbow-{y_name}-left-to-{x_name}-up"
        ALL_SHAPES[name_l_u] = {
            "path": f"M 0 {y} L {x} {y} L {x} 0",
            "collars": [collar_h(0, y), collar_v(x, 0)],
            "arrow": arrow_v(x, y // 2, to_down=False),
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }
        # Elbow: Up to Left (N -> W)
        name_u_l = f"elbow-{x_name}-up-to-{y_name}-left"
        ALL_SHAPES[name_u_l] = {
            "path": f"M {x} 0 L {x} {y} L 0 {y}",
            "collars": [collar_v(x, 0), collar_h(0, y)],
            "arrow": arrow_h(x // 2, y, to_right=False),
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }

        # Elbow: Left to Down (W -> S)
        name_l_d = f"elbow-{y_name}-left-to-{x_name}-down"
        ALL_SHAPES[name_l_d] = {
            "path": f"M 0 {y} L {x} {y} L {x} 200",
            "collars": [collar_h(0, y), collar_v(x, 200)],
            "arrow": arrow_v(x, (y + 200) // 2, to_down=True),
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }
        # Elbow: Down to Left (S -> W)
        name_d_l = f"elbow-{x_name}-down-to-{y_name}-left"
        ALL_SHAPES[name_d_l] = {
            "path": f"M {x} 200 L {x} {y} L 0 {y}",
            "collars": [collar_v(x, 200), collar_h(0, y)],
            "arrow": arrow_h(x // 2, y, to_right=False),
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }

        # Elbow: Right to Up (E -> N)
        name_r_u = f"elbow-{y_name}-right-to-{x_name}-up"
        ALL_SHAPES[name_r_u] = {
            "path": f"M 200 {y} L {x} {y} L {x} 0",
            "collars": [collar_h(200, y), collar_v(x, 0)],
            "arrow": arrow_v(x, y // 2, to_down=False),
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }
        # Elbow: Up to Right (N -> E)
        name_u_r = f"elbow-{x_name}-up-to-{y_name}-right"
        ALL_SHAPES[name_u_r] = {
            "path": f"M {x} 0 L {x} {y} L 200 {y}",
            "collars": [collar_v(x, 0), collar_h(200, y)],
            "arrow": arrow_h((x + 200) // 2, y, to_right=True),
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }

        # Elbow: Right to Down (E -> S)
        name_r_d = f"elbow-{y_name}-right-to-{x_name}-down"
        ALL_SHAPES[name_r_d] = {
            "path": f"M 200 {y} L {x} {y} L {x} 200",
            "collars": [collar_h(200, y), collar_v(x, 200)],
            "arrow": arrow_v(x, (y + 200) // 2, to_down=True),
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }
        # Elbow: Down to Right (S -> E)
        name_d_r = f"elbow-{x_name}-down-to-{y_name}-right"
        ALL_SHAPES[name_d_r] = {
            "path": f"M {x} 200 L {x} {y} L 200 {y}",
            "collars": [collar_v(x, 200), collar_h(200, y)],
            "arrow": arrow_h((x + 200) // 2, y, to_right=True),
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }

# Standard grid aliases for center elbows
ALL_SHAPES["elbow-bottom-left"] = ALL_SHAPES["elbow-center-left-to-center-up"]
ALL_SHAPES["elbow-bottom-right"] = ALL_SHAPES["elbow-center-down-to-center-right"]
ALL_SHAPES["elbow-top-left"] = ALL_SHAPES["elbow-center-left-to-center-down"]
ALL_SHAPES["elbow-top-right"] = ALL_SHAPES["elbow-center-up-to-center-right"]

# =============================================================================
# 3. POSITIONAL T-JUNCTIONS (Across all tracks)
# =============================================================================
for y_name, y in Y_TRACKS:
    for x_name, x in X_TRACKS:
        # Horizontal Header with Branch UP
        name_t_u = f"tee-horizontal-{y_name}-branch-{x_name}-up"
        arr_x = 150 if x <= 100 else 50
        ALL_SHAPES[name_t_u] = {
            "path": f"M 0 {y} L 200 {y} M {x} {y} L {x} 0",
            "collars": [collar_h(0, y), collar_h(200, y), collar_v(x, 0)],
            "arrow": f"{arrow_h(arr_x, y, to_right=True)} {arrow_v(x, y // 2, to_down=False)}",
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }

        # Horizontal Header with Branch DOWN
        name_t_d = f"tee-horizontal-{y_name}-branch-{x_name}-down"
        ALL_SHAPES[name_t_d] = {
            "path": f"M 0 {y} L 200 {y} M {x} {y} L {x} 200",
            "collars": [collar_h(0, y), collar_h(200, y), collar_v(x, 200)],
            "arrow": f"{arrow_h(arr_x, y, to_right=True)} {arrow_v(x, (y + 200) // 2, to_down=True)}",
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }

        # Vertical Header with Branch LEFT
        name_t_l = f"tee-vertical-{x_name}-branch-{y_name}-left"
        arr_y = 150 if y <= 100 else 50
        ALL_SHAPES[name_t_l] = {
            "path": f"M {x} 0 L {x} 200 M {x} {y} L 0 {y}",
            "collars": [collar_v(x, 0), collar_v(x, 200), collar_h(0, y)],
            "arrow": f"{arrow_v(x, arr_y, to_down=True)} {arrow_h(x // 2, y, to_right=False)}",
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }

        # Vertical Header with Branch RIGHT
        name_t_r = f"tee-vertical-{x_name}-branch-{y_name}-right"
        ALL_SHAPES[name_t_r] = {
            "path": f"M {x} 0 L {x} 200 M {x} {y} L 200 {y}",
            "collars": [collar_v(x, 0), collar_v(x, 200), collar_h(200, y)],
            "arrow": f"{arrow_v(x, arr_y, to_down=True)} {arrow_h((x + 200) // 2, y, to_right=True)}",
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }

# Standard grid aliases for center tees
ALL_SHAPES["tee-horizontal-top"] = ALL_SHAPES["tee-horizontal-center-branch-center-up"]
ALL_SHAPES["tee-horizontal-bottom"] = ALL_SHAPES["tee-horizontal-center-branch-center-down"]
ALL_SHAPES["tee-vertical-left"] = ALL_SHAPES["tee-vertical-center-branch-center-left"]
ALL_SHAPES["tee-vertical-right"] = ALL_SHAPES["tee-vertical-center-branch-center-right"]

# =============================================================================
# 4. POSITIONAL 4-WAY CROSSES
# =============================================================================
for y_name, y in Y_TRACKS:
    for x_name, x in X_TRACKS:
        name_cross = f"cross-{y_name}-{x_name}"
        ALL_SHAPES[name_cross] = {
            "path": f"M 0 {y} L 200 {y} M {x} 0 L {x} 200",
            "collars": [collar_h(0, y), collar_h(200, y), collar_v(x, 0), collar_v(x, 200)],
            "arrow": f"{arrow_h(150, y, to_right=True)} {arrow_v(x, 150, to_down=True)}",
            "anim_dir": "from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; }"
        }

ALL_SHAPES["cross-four-way"] = ALL_SHAPES["cross-center-center"]

print(f"=== GENERATING POSITIONAL PIPELINE LIBRARY INTO COLOR-WISE FOLDERS IN '{OUTPUT_DIR}' ===")
total_files = 0

for shape_name, s_cfg in ALL_SHAPES.items():
    collars_markup = "\n  ".join(s_cfg["collars"])
    path_d = s_cfg["path"]
    anim_dir_css = s_cfg["anim_dir"]

    # 1. Dry static SVG in 'dry/' folder
    dry_fname = f"pipe-{shape_name}-dry-static.svg"
    dry_svg = TEMPLATE_DRY.format(path=path_d, collars=collars_markup)
    with open(os.path.join(OUTPUT_DIR, "dry", dry_fname), "w", encoding="utf-8") as f:
        f.write(dry_svg)
    total_files += 1

    # 2. For each Color: animated and static in that color's folder
    for color_name, c_vals in COLORS.items():
        fluid_c = c_vals["fluid"]
        pulse_c = c_vals["pulse"]
        arrow_markup = s_cfg["arrow"].replace("{fluid}", fluid_c)

        # Animated
        anim_fname = f"pipe-{shape_name}-{color_name}-animated.svg"
        anim_svg = TEMPLATE_ANIMATED.format(
            anim_dir=anim_dir_css,
            path=path_d,
            fluid=fluid_c,
            pulse=pulse_c,
            arrow=arrow_markup,
            collars=collars_markup
        )
        with open(os.path.join(OUTPUT_DIR, color_name, anim_fname), "w", encoding="utf-8") as f:
            f.write(anim_svg)
        total_files += 1

        # Static
        static_fname = f"pipe-{shape_name}-{color_name}-static.svg"
        static_svg = TEMPLATE_STATIC.format(
            path=path_d,
            fluid=fluid_c,
            collars=collars_markup
        )
        with open(os.path.join(OUTPUT_DIR, color_name, static_fname), "w", encoding="utf-8") as f:
            f.write(static_svg)
        total_files += 1

print(f"\nDone! Successfully generated {total_files} pipe SVGs organized into color-wise folders in '{OUTPUT_DIR}'.")
