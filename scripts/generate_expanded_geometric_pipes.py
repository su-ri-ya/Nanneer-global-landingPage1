import os

BASE_DIR = r"c:\Nanneer global\draft 3\public\schematic-assets\pipes"

COLORS = {
    "blue": {
        "core": "#0284c7",
        "pulse": "#bae6fd",
    },
    "brown": {
        "core": "#8d6e63",
        "pulse": "#d7ccc8",
    },
    "green": {
        "core": "#16a34a",
        "pulse": "#bbf7d0",
    },
}

def get_h_collar(x, y):
    if x == 0:
        return f'<rect x="0" y="{y - 5.5}" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'
    else:
        return f'<rect x="196" y="{y - 5.5}" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'

def get_v_collar(x, y):
    if y == 0:
        return f'<rect x="{x - 5.5}" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'
    else:
        return f'<rect x="{x - 5.5}" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'

def get_blind_flange_h(x, y):
    # Blind flange cap at (x, y)
    return f'<rect x="{x - 3}" y="{y - 8}" width="6" height="16" rx="1.5" fill="#94a3b8" stroke="#334155" stroke-width="1.2"/><circle cx="{x}" cy="{y - 5}" r="1.2" fill="#1e293b"/><circle cx="{x}" cy="{y + 5}" r="1.2" fill="#1e293b"/>'

def get_blind_flange_v(x, y):
    return f'<rect x="{x - 8}" y="{y - 3}" width="16" height="6" rx="1.5" fill="#94a3b8" stroke="#334155" stroke-width="1.2"/><circle cx="{x - 5}" cy="{y}" r="1.2" fill="#1e293b"/><circle cx="{x + 5}" cy="{y}" r="1.2" fill="#1e293b"/>'

def arrow_h(x, y, to_right=True, core_color="#0284c7"):
    if to_right:
        return f'<polygon points="{x-4},{y-3} {x+4},{y} {x-4},{y+3}" fill="{core_color}" />'
    else:
        return f'<polygon points="{x+4},{y-3} {x-4},{y} {x+4},{y+3}" fill="{core_color}" />'

def arrow_v(x, y, to_down=True, core_color="#0284c7"):
    if to_down:
        return f'<polygon points="{x-3},{y-4} {x},{y+4} {x+3},{y-4}" fill="{core_color}" />'
    else:
        return f'<polygon points="{x-3},{y+4} {x},{y-4} {x+3},{y+4}" fill="{core_color}" />'

def render_svg(path_d, collars, arrows, core_color, pulse_color=None, is_animated=False, extra_elements=None):
    defs = f"""  <defs>
    {"<style>\\n      @keyframes p-flow-anim { from { stroke-dashoffset: 24; } to { stroke-dashoffset: 0; } }\\n      .anim-p-flow { stroke-dasharray: 5 7; animation: p-flow-anim 0.8s linear infinite; }\\n    </style>\\n    " if is_animated else ""}<filter id="ssPipeShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2.5" stdDeviation="2.5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <linearGradient id="ssPipeGradH" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748b" /><stop offset="25%" stop-color="#ffffff" />
      <stop offset="55%" stop-color="#cbd5e1" /><stop offset="85%" stop-color="#94a3b8" /><stop offset="100%" stop-color="#475569" />
    </linearGradient>
  </defs>"""

    body = f"""  <!-- 7px Stainless Steel 316 Outer Casing with 3D Drop Shadow -->
  <path d="{path_d}" stroke="url(#ssPipeGradH)" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#ssPipeShadow)"/>
  <!-- 4px Process Fluid Core -->
  <path d="{path_d}" stroke="{core_color}" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>"""

    anim_layer = ""
    if is_animated and pulse_color:
        anim_layer = f"""\n  <!-- 2.5px Animated Flow Dashes -->
  <path d="{path_d}" stroke="{pulse_color}" stroke-width="2.5" fill="none" stroke-linejoin="round" stroke-linecap="round" class="anim-p-flow"/>"""

    arrow_layer = ""
    if is_animated and arrows:
        arrow_layer = "\n  " + "\n  ".join(arrows)

    collar_layer = ""
    if collars:
        collar_layer = "\n  " + "\n  ".join(collars)

    extras = ""
    if extra_elements:
        extras = "\n  " + "\n  ".join(extra_elements)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{defs}
{body}{anim_layer}{arrow_layer}{collar_layer}{extras}
</svg>"""

def build_shape_definitions(core_color):
    shapes = {}

    # -------------------------------------------------------------------------
    # 1. Z-STEP / JOG / DOGLEG PIPES (24 Shapes)
    # -------------------------------------------------------------------------
    # A. Horizontal Z-Steps (6 pairs x 2 directions = 12 shapes)
    h_pairs = [
        ("top", "center", 48, 100),
        ("top", "bottom", 48, 150),
        ("center", "top", 100, 48),
        ("center", "bottom", 100, 150),
        ("bottom", "top", 150, 48),
        ("bottom", "center", 150, 100),
    ]
    for y1_name, y2_name, y1, y2 in h_pairs:
        mid_x = 100
        # Left-to-Right
        p_lr = f"M 0 {y1} L {mid_x} {y1} L {mid_x} {y2} L 200 {y2}"
        shapes[f"pipe-step-horizontal-{y1_name}-to-{y2_name}-left-to-right-fluid"] = {
            "path": p_lr,
            "collars": [get_h_collar(0, y1), get_h_collar(200, y2)],
            "arrows": [arrow_h(50, y1, True, core_color), arrow_h(150, y2, True, core_color)]
        }
        # Right-to-Left
        p_rl = f"M 200 {y2} L {mid_x} {y2} L {mid_x} {y1} L 0 {y1}"
        shapes[f"pipe-step-horizontal-{y2_name}-to-{y1_name}-right-to-left-fluid"] = {
            "path": p_rl,
            "collars": [get_h_collar(200, y2), get_h_collar(0, y1)],
            "arrows": [arrow_h(150, y2, False, core_color), arrow_h(50, y1, False, core_color)]
        }

    # B. Vertical Z-Steps (6 pairs x 2 directions = 12 shapes)
    v_pairs = [
        ("left", "center", 48, 100),
        ("left", "right", 48, 150),
        ("center", "left", 100, 48),
        ("center", "right", 100, 150),
        ("right", "left", 150, 48),
        ("right", "center", 150, 100),
    ]
    for x1_name, x2_name, x1, x2 in v_pairs:
        mid_y = 100
        # Top-to-Bottom
        p_tb = f"M {x1} 0 L {x1} {mid_y} L {x2} {mid_y} L {x2} 200"
        shapes[f"pipe-step-vertical-{x1_name}-to-{x2_name}-top-to-bottom-fluid"] = {
            "path": p_tb,
            "collars": [get_v_collar(x1, 0), get_v_collar(x2, 200)],
            "arrows": [arrow_v(x1, 50, True, core_color), arrow_v(x2, 150, True, core_color)]
        }
        # Bottom-to-Top
        p_bt = f"M {x2} 200 L {x2} {mid_y} L {x1} {mid_y} L {x1} 0"
        shapes[f"pipe-step-vertical-{x2_name}-to-{x1_name}-bottom-to-top-fluid"] = {
            "path": p_bt,
            "collars": [get_v_collar(x2, 200), get_v_collar(x1, 0)],
            "arrows": [arrow_v(x2, 150, False, core_color), arrow_v(x1, 50, False, core_color)]
        }

    # -------------------------------------------------------------------------
    # 2. CROSSOVER BRIDGES / JUMPERS (OVERPASS) (4 Shapes)
    # -------------------------------------------------------------------------
    # Horizontal Arch over Vertical Straight
    # L to R
    shapes["pipe-crossover-bridge-horizontal-left-to-right-fluid"] = {
        "path": "M 100 0 L 100 200 M 0 100 L 82 100 M 82 100 C 82 72, 118 72, 118 100 M 118 100 L 200 100",
        "collars": [get_v_collar(100, 0), get_v_collar(100, 200), get_h_collar(0, 100), get_h_collar(200, 100)],
        "arrows": [arrow_h(50, 100, True, core_color), arrow_h(160, 100, True, core_color), arrow_v(100, 160, True, core_color)]
    }
    # R to L
    shapes["pipe-crossover-bridge-horizontal-right-to-left-fluid"] = {
        "path": "M 100 0 L 100 200 M 200 100 L 118 100 M 118 100 C 118 72, 82 72, 82 100 M 82 100 L 0 100",
        "collars": [get_v_collar(100, 0), get_v_collar(100, 200), get_h_collar(0, 100), get_h_collar(200, 100)],
        "arrows": [arrow_h(160, 100, False, core_color), arrow_h(50, 100, False, core_color), arrow_v(100, 160, True, core_color)]
    }
    # Vertical Arch over Horizontal Straight
    # T to B
    shapes["pipe-crossover-bridge-vertical-top-to-bottom-fluid"] = {
        "path": "M 0 100 L 200 100 M 100 0 L 100 82 M 100 82 C 128 82, 128 118, 100 118 M 100 118 L 100 200",
        "collars": [get_h_collar(0, 100), get_h_collar(200, 100), get_v_collar(100, 0), get_v_collar(100, 200)],
        "arrows": [arrow_v(100, 50, True, core_color), arrow_v(100, 160, True, core_color), arrow_h(160, 100, True, core_color)]
    }
    # B to T
    shapes["pipe-crossover-bridge-vertical-bottom-to-top-fluid"] = {
        "path": "M 0 100 L 200 100 M 100 200 L 100 118 M 100 118 C 128 118, 128 82, 100 82 M 100 82 L 100 0",
        "collars": [get_h_collar(0, 100), get_h_collar(200, 100), get_v_collar(100, 0), get_v_collar(100, 200)],
        "arrows": [arrow_v(100, 160, False, core_color), arrow_v(100, 50, False, core_color), arrow_h(160, 100, True, core_color)]
    }

    # -------------------------------------------------------------------------
    # 3. 45° LATERAL WYES (Y-FITTINGS) (8 Shapes)
    # -------------------------------------------------------------------------
    # Wye Horizontal with 45° Branch UP
    shapes["pipe-wye-45-branch-up-left-to-right-fluid"] = {
        "path": "M 0 100 L 200 100 M 100 100 L 170 30",
        "collars": [get_h_collar(0, 100), get_h_collar(200, 100)],
        "arrows": [arrow_h(60, 100, True, core_color), arrow_h(160, 100, True, core_color)]
    }
    shapes["pipe-wye-45-branch-up-right-to-left-fluid"] = {
        "path": "M 200 100 L 0 100 M 100 100 L 30 30",
        "collars": [get_h_collar(0, 100), get_h_collar(200, 100)],
        "arrows": [arrow_h(150, 100, False, core_color), arrow_h(60, 100, False, core_color)]
    }
    # Wye Horizontal with 45° Branch DOWN
    shapes["pipe-wye-45-branch-down-left-to-right-fluid"] = {
        "path": "M 0 100 L 200 100 M 100 100 L 170 170",
        "collars": [get_h_collar(0, 100), get_h_collar(200, 100)],
        "arrows": [arrow_h(60, 100, True, core_color), arrow_h(160, 100, True, core_color)]
    }
    shapes["pipe-wye-45-branch-down-right-to-left-fluid"] = {
        "path": "M 200 100 L 0 100 M 100 100 L 30 170",
        "collars": [get_h_collar(0, 100), get_h_collar(200, 100)],
        "arrows": [arrow_h(150, 100, False, core_color), arrow_h(60, 100, False, core_color)]
    }
    # Wye Vertical with 45° Branch LEFT
    shapes["pipe-wye-45-vertical-branch-left-top-to-bottom-fluid"] = {
        "path": "M 100 0 L 100 200 M 100 100 L 30 170",
        "collars": [get_v_collar(100, 0), get_v_collar(100, 200)],
        "arrows": [arrow_v(100, 60, True, core_color), arrow_v(100, 160, True, core_color)]
    }
    shapes["pipe-wye-45-vertical-branch-left-bottom-to-top-fluid"] = {
        "path": "M 100 200 L 100 0 M 100 100 L 30 30",
        "collars": [get_v_collar(100, 0), get_v_collar(100, 200)],
        "arrows": [arrow_v(100, 150, False, core_color), arrow_v(100, 50, False, core_color)]
    }
    # Wye Vertical with 45° Branch RIGHT
    shapes["pipe-wye-45-vertical-branch-right-top-to-bottom-fluid"] = {
        "path": "M 100 0 L 100 200 M 100 100 L 170 170",
        "collars": [get_v_collar(100, 0), get_v_collar(100, 200)],
        "arrows": [arrow_v(100, 60, True, core_color), arrow_v(100, 160, True, core_color)]
    }
    shapes["pipe-wye-45-vertical-branch-right-bottom-to-top-fluid"] = {
        "path": "M 100 200 L 100 0 M 100 100 L 170 30",
        "collars": [get_v_collar(100, 0), get_v_collar(100, 200)],
        "arrows": [arrow_v(100, 150, False, core_color), arrow_v(100, 50, False, core_color)]
    }

    # -------------------------------------------------------------------------
    # 4. 180° U-BENDS / RETURN LOOPS (HAIRPINS) (8 Shapes)
    # -------------------------------------------------------------------------
    # Left-Facing U-Bend (enters y=48, returns y=150)
    shapes["pipe-loop-u-turn-left-facing-top-to-bottom-fluid"] = {
        "path": "M 0 48 L 120 48 C 160 48, 160 150, 120 150 L 0 150",
        "collars": [get_h_collar(0, 48), get_h_collar(0, 150)],
        "arrows": [arrow_h(60, 48, True, core_color), arrow_h(60, 150, False, core_color)]
    }
    shapes["pipe-loop-u-turn-left-facing-bottom-to-top-fluid"] = {
        "path": "M 0 150 L 120 150 C 160 150, 160 48, 120 48 L 0 48",
        "collars": [get_h_collar(0, 48), get_h_collar(0, 150)],
        "arrows": [arrow_h(60, 150, True, core_color), arrow_h(60, 48, False, core_color)]
    }
    # Right-Facing U-Bend (enters y=48, returns y=150)
    shapes["pipe-loop-u-turn-right-facing-top-to-bottom-fluid"] = {
        "path": "M 200 48 L 80 48 C 40 48, 40 150, 80 150 L 200 150",
        "collars": [get_h_collar(200, 48), get_h_collar(200, 150)],
        "arrows": [arrow_h(140, 48, False, core_color), arrow_h(140, 150, True, core_color)]
    }
    shapes["pipe-loop-u-turn-right-facing-bottom-to-top-fluid"] = {
        "path": "M 200 150 L 80 150 C 40 150, 40 48, 80 48 L 200 48",
        "collars": [get_h_collar(200, 48), get_h_collar(200, 150)],
        "arrows": [arrow_h(140, 150, False, core_color), arrow_h(140, 48, True, core_color)]
    }
    # Top-Facing U-Bend (enters x=48, returns x=150)
    shapes["pipe-loop-u-turn-top-facing-left-to-right-fluid"] = {
        "path": "M 48 0 L 48 120 C 48 160, 150 160, 150 120 L 150 0",
        "collars": [get_v_collar(48, 0), get_v_collar(150, 0)],
        "arrows": [arrow_v(48, 60, True, core_color), arrow_v(150, 60, False, core_color)]
    }
    shapes["pipe-loop-u-turn-top-facing-right-to-left-fluid"] = {
        "path": "M 150 0 L 150 120 C 150 160, 48 160, 48 120 L 48 0",
        "collars": [get_v_collar(48, 0), get_v_collar(150, 0)],
        "arrows": [arrow_v(150, 60, True, core_color), arrow_v(48, 60, False, core_color)]
    }
    # Bottom-Facing U-Bend (enters x=48, returns x=150)
    shapes["pipe-loop-u-turn-bottom-facing-left-to-right-fluid"] = {
        "path": "M 48 200 L 48 80 C 48 40, 150 40, 150 80 L 150 200",
        "collars": [get_v_collar(48, 200), get_v_collar(150, 200)],
        "arrows": [arrow_v(48, 140, False, core_color), arrow_v(150, 140, True, core_color)]
    }
    shapes["pipe-loop-u-turn-bottom-facing-right-to-left-fluid"] = {
        "path": "M 150 200 L 150 80 C 150 40, 48 40, 48 80 L 48 200",
        "collars": [get_v_collar(48, 200), get_v_collar(150, 200)],
        "arrows": [arrow_v(150, 140, False, core_color), arrow_v(48, 140, True, core_color)]
    }

    # -------------------------------------------------------------------------
    # 5. EQUIPMENT MANIFOLDS (SPLITTERS & COMBINERS) (4 Shapes)
    # -------------------------------------------------------------------------
    shapes["pipe-manifold-dual-pump-suction-splitter-fluid"] = {
        "path": "M 100 0 L 100 60 M 48 60 L 150 60 M 48 60 L 48 200 M 150 60 L 150 200",
        "collars": [get_v_collar(100, 0), get_v_collar(48, 200), get_v_collar(150, 200)],
        "arrows": [arrow_v(100, 35, True, core_color), arrow_v(48, 145, True, core_color), arrow_v(150, 145, True, core_color)]
    }
    shapes["pipe-manifold-dual-pump-discharge-combiner-fluid"] = {
        "path": "M 48 200 L 48 100 L 150 100 L 150 200 M 100 100 L 100 0",
        "collars": [get_v_collar(48, 200), get_v_collar(150, 200), get_v_collar(100, 0)],
        "arrows": [arrow_v(48, 155, False, core_color), arrow_v(150, 155, False, core_color), arrow_v(100, 50, False, core_color)]
    }
    shapes["pipe-manifold-dual-blower-interconnect-fluid"] = {
        "path": "M 0 48 L 70 48 L 70 150 L 0 150 M 70 100 L 200 100",
        "collars": [get_h_collar(0, 48), get_h_collar(0, 150), get_h_collar(200, 100)],
        "arrows": [arrow_h(35, 48, True, core_color), arrow_h(35, 150, True, core_color), arrow_h(140, 100, True, core_color)]
    }
    shapes["pipe-manifold-dual-blower-splitter-fluid"] = {
        "path": "M 0 100 L 130 100 M 130 48 L 130 150 M 130 48 L 200 48 M 130 150 L 200 150",
        "collars": [get_h_collar(0, 100), get_h_collar(200, 48), get_h_collar(200, 150)],
        "arrows": [arrow_h(60, 100, True, core_color), arrow_h(165, 48, True, core_color), arrow_h(165, 150, True, core_color)]
    }

    # -------------------------------------------------------------------------
    # 6. DUAL BYPASS LOOP ASSEMBLIES (2 Shapes)
    # -------------------------------------------------------------------------
    shapes["pipe-bypass-dual-loop-left-to-right-fluid"] = {
        "path": "M 0 100 L 40 100 L 70 50 L 130 50 L 160 100 L 200 100 M 40 100 L 70 150 L 130 150 L 160 100 M 40 100 L 160 100",
        "collars": [get_h_collar(0, 100), get_h_collar(200, 100)],
        "arrows": [arrow_h(100, 50, True, core_color), arrow_h(100, 100, True, core_color), arrow_h(100, 150, True, core_color)]
    }
    shapes["pipe-bypass-dual-loop-right-to-left-fluid"] = {
        "path": "M 200 100 L 160 100 L 130 50 L 70 50 L 40 100 L 0 100 M 160 100 L 130 150 L 70 150 L 40 100 M 160 100 L 40 100",
        "collars": [get_h_collar(0, 100), get_h_collar(200, 100)],
        "arrows": [arrow_h(100, 50, False, core_color), arrow_h(100, 100, False, core_color), arrow_h(100, 150, False, core_color)]
    }

    # -------------------------------------------------------------------------
    # 7. BLIND FLANGE END-CAPS (TERMINATIONS) (8 Shapes)
    # -------------------------------------------------------------------------
    shapes["pipe-endcap-blind-flange-horizontal-left-center-fluid"] = {
        "path": "M 0 100 L 100 100",
        "collars": [get_h_collar(0, 100)],
        "arrows": [arrow_h(50, 100, True, core_color)],
        "extras": [get_blind_flange_h(100, 100)]
    }
    shapes["pipe-endcap-blind-flange-horizontal-right-center-fluid"] = {
        "path": "M 200 100 L 100 100",
        "collars": [get_h_collar(200, 100)],
        "arrows": [arrow_h(150, 100, False, core_color)],
        "extras": [get_blind_flange_h(100, 100)]
    }
    shapes["pipe-endcap-blind-flange-horizontal-left-top-fluid"] = {
        "path": "M 0 48 L 100 48",
        "collars": [get_h_collar(0, 48)],
        "arrows": [arrow_h(50, 48, True, core_color)],
        "extras": [get_blind_flange_h(100, 48)]
    }
    shapes["pipe-endcap-blind-flange-horizontal-left-bottom-fluid"] = {
        "path": "M 0 150 L 100 150",
        "collars": [get_h_collar(0, 150)],
        "arrows": [arrow_h(50, 150, True, core_color)],
        "extras": [get_blind_flange_h(100, 150)]
    }
    shapes["pipe-endcap-blind-flange-vertical-top-center-fluid"] = {
        "path": "M 100 0 L 100 100",
        "collars": [get_v_collar(100, 0)],
        "arrows": [arrow_v(100, 50, True, core_color)],
        "extras": [get_blind_flange_v(100, 100)]
    }
    shapes["pipe-endcap-blind-flange-vertical-bottom-center-fluid"] = {
        "path": "M 100 200 L 100 100",
        "collars": [get_v_collar(100, 200)],
        "arrows": [arrow_v(100, 150, False, core_color)],
        "extras": [get_blind_flange_v(100, 100)]
    }
    shapes["pipe-endcap-blind-flange-vertical-top-left-fluid"] = {
        "path": "M 48 0 L 48 100",
        "collars": [get_v_collar(48, 0)],
        "arrows": [arrow_v(48, 50, True, core_color)],
        "extras": [get_blind_flange_v(48, 100)]
    }
    shapes["pipe-endcap-blind-flange-vertical-top-right-fluid"] = {
        "path": "M 150 0 L 150 100",
        "collars": [get_v_collar(150, 0)],
        "arrows": [arrow_v(150, 50, True, core_color)],
        "extras": [get_blind_flange_v(150, 100)]
    }

    return shapes

def main():
    generated_count = 0
    total_shapes = 0
    for color_name, c_data in COLORS.items():
        color_dir = os.path.join(BASE_DIR, color_name)
        os.makedirs(color_dir, exist_ok=True)
        core = c_data["core"]
        pulse = c_data["pulse"]

        shapes = build_shape_definitions(core)
        total_shapes = len(shapes)

        for base_name, s_data in shapes.items():
            path_d = s_data["path"]
            collars = s_data.get("collars", [])
            arrows = s_data.get("arrows", [])
            extras = s_data.get("extras", [])

            # Static SVG
            static_svg = render_svg(path_d, collars, arrows, core, pulse, False, extras)
            with open(os.path.join(color_dir, f"{base_name}-static.svg"), "w", encoding="utf-8") as f:
                f.write(static_svg)
            generated_count += 1

            # Animated SVG
            anim_svg = render_svg(path_d, collars, arrows, core, pulse, True, extras)
            with open(os.path.join(color_dir, f"{base_name}-animated.svg"), "w", encoding="utf-8") as f:
                f.write(anim_svg)
            generated_count += 1

    print(f"Successfully generated {generated_count} SVG files for {total_shapes} unique geometric shapes across all 3 colors.")

if __name__ == "__main__":
    main()
