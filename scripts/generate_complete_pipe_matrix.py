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

Y_TRACKS = [("top", 48), ("center", 100), ("bottom", 150)]
X_TRACKS = [("left", 48), ("center", 100), ("right", 150)]

def get_h_collar(x, y):
    # Collar at x=0 or x=200
    if x == 0:
        return f'<rect x="0" y="{y - 5.5}" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'
    else:
        return f'<rect x="196" y="{y - 5.5}" width="4" height="11" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'

def get_v_collar(x, y):
    # Collar at y=0 or y=200
    if y == 0:
        return f'<rect x="{x - 5.5}" y="0" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'
    else:
        return f'<rect x="{x - 5.5}" y="196" width="11" height="4" rx="1" fill="#cbd5e1" stroke="#475569" stroke-width="0.8"/>'

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

def render_svg(path_d, collars, arrows, core_color, pulse_color=None, is_animated=False):
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
        arrow_layer = "\n  " + "".join(arrows)

    collar_layer = "\n  " + "\n  ".join(collars)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{defs}
{body}{anim_layer}{arrow_layer}{collar_layer}
</svg>"""

def main():
    generated_count = 0
    for color_name, c_data in COLORS.items():
        color_dir = os.path.join(BASE_DIR, color_name)
        os.makedirs(color_dir, exist_ok=True)
        core = c_data["core"]
        pulse = c_data["pulse"]

        # =====================================================================
        # 1. TEES: Horizontal Header (y = 48, 100, 150)
        # =====================================================================
        for y_name, y in Y_TRACKS:
            for x_name, x in X_TRACKS:
                # Branch UP
                path_d = f"M 0 {y} L 200 {y} M {x} {y} L {x} 0"
                collars = [get_h_collar(0, y), get_h_collar(200, y), get_v_collar(x, 0)]
                arr_h_x = 155 if x <= 100 else 60
                arrows = [
                    arrow_h(arr_h_x, y, to_right=True, core_color=core),
                    arrow_v(x, y // 2, to_down=False, core_color=core)
                ]

                # Specific filename + aliases
                names = [
                    f"pipe-tee-header-{y_name}-branch-{x_name}-up-fluid",
                ]
                if x_name == "center":
                    names.append(f"pipe-tee-{y_name}-header-branch-up-fluid")
                if y_name == "center" and x_name == "center":
                    names.append("pipe-tee-branch-up-fluid")

                for base_name in names:
                    # Static
                    with open(os.path.join(color_dir, f"{base_name}-static.svg"), "w", encoding="utf-8") as f:
                        f.write(render_svg(path_d, collars, arrows, core, pulse, False))
                    # Animated
                    with open(os.path.join(color_dir, f"{base_name}-animated.svg"), "w", encoding="utf-8") as f:
                        f.write(render_svg(path_d, collars, arrows, core, pulse, True))
                    generated_count += 2

                # Branch DOWN
                path_d = f"M 0 {y} L 200 {y} M {x} {y} L {x} 200"
                collars = [get_h_collar(0, y), get_h_collar(200, y), get_v_collar(x, 200)]
                arr_v_y = (y + 200) // 2
                arrows = [
                    arrow_h(arr_h_x, y, to_right=True, core_color=core),
                    arrow_v(x, arr_v_y, to_down=True, core_color=core)
                ]

                names = [
                    f"pipe-tee-header-{y_name}-branch-{x_name}-down-fluid",
                ]
                if x_name == "center":
                    names.append(f"pipe-tee-{y_name}-header-branch-down-fluid")
                if y_name == "center" and x_name == "center":
                    names.append("pipe-tee-branch-down-fluid")

                for base_name in names:
                    with open(os.path.join(color_dir, f"{base_name}-static.svg"), "w", encoding="utf-8") as f:
                        f.write(render_svg(path_d, collars, arrows, core, pulse, False))
                    with open(os.path.join(color_dir, f"{base_name}-animated.svg"), "w", encoding="utf-8") as f:
                        f.write(render_svg(path_d, collars, arrows, core, pulse, True))
                    generated_count += 2

        # =====================================================================
        # 2. TEES: Vertical Header (x = 48, 100, 150)
        # =====================================================================
        for x_name, x in X_TRACKS:
            for y_name, y in Y_TRACKS:
                # Branch LEFT
                path_d = f"M {x} 0 L {x} 200 M {x} {y} L 0 {y}"
                collars = [get_v_collar(x, 0), get_v_collar(x, 200), get_h_collar(0, y)]
                arr_v_y = 155 if y <= 100 else 60
                arrows = [
                    arrow_v(x, arr_v_y, to_down=True, core_color=core),
                    arrow_h(x // 2, y, to_right=False, core_color=core)
                ]

                names = [
                    f"pipe-tee-header-{x_name}-branch-{y_name}-left-fluid",
                ]
                if y_name == "center":
                    names.append(f"pipe-tee-vertical-{x_name}-branch-left-fluid")
                if x_name == "center" and y_name == "center":
                    names.append("pipe-tee-branch-left-fluid")

                for base_name in names:
                    with open(os.path.join(color_dir, f"{base_name}-static.svg"), "w", encoding="utf-8") as f:
                        f.write(render_svg(path_d, collars, arrows, core, pulse, False))
                    with open(os.path.join(color_dir, f"{base_name}-animated.svg"), "w", encoding="utf-8") as f:
                        f.write(render_svg(path_d, collars, arrows, core, pulse, True))
                    generated_count += 2

                # Branch RIGHT
                path_d = f"M {x} 0 L {x} 200 M {x} {y} L 200 {y}"
                collars = [get_v_collar(x, 0), get_v_collar(x, 200), get_h_collar(200, y)]
                arr_h_x = (x + 200) // 2
                arrows = [
                    arrow_v(x, arr_v_y, to_down=True, core_color=core),
                    arrow_h(arr_h_x, y, to_right=True, core_color=core)
                ]

                names = [
                    f"pipe-tee-header-{x_name}-branch-{y_name}-right-fluid",
                ]
                if y_name == "center":
                    names.append(f"pipe-tee-vertical-{x_name}-branch-right-fluid")
                if x_name == "center" and y_name == "center":
                    names.append("pipe-tee-branch-right-fluid")

                for base_name in names:
                    with open(os.path.join(color_dir, f"{base_name}-static.svg"), "w", encoding="utf-8") as f:
                        f.write(render_svg(path_d, collars, arrows, core, pulse, False))
                    with open(os.path.join(color_dir, f"{base_name}-animated.svg"), "w", encoding="utf-8") as f:
                        f.write(render_svg(path_d, collars, arrows, core, pulse, True))
                    generated_count += 2

        # =====================================================================
        # 3. ELBOWS: Every (y, x) intersection with 8 directions
        # =====================================================================
        for y_name, y in Y_TRACKS:
            for x_name, x in X_TRACKS:
                elbow_variants = [
                    # 1. Left to Up
                    {
                        "dir": "left-to-up",
                        "path": f"M 0 {y} L {x} {y} L {x} 0",
                        "collars": [get_h_collar(0, y), get_v_collar(x, 0)],
                        "arrows": [arrow_v(x, y // 2 if y > 30 else 24, to_down=False, core_color=core)]
                    },
                    # 2. Up to Left
                    {
                        "dir": "up-to-left",
                        "path": f"M {x} 0 L {x} {y} L 0 {y}",
                        "collars": [get_v_collar(x, 0), get_h_collar(0, y)],
                        "arrows": [arrow_h(x // 2 if x > 30 else 24, y, to_right=False, core_color=core)]
                    },
                    # 3. Left to Down
                    {
                        "dir": "left-to-down",
                        "path": f"M 0 {y} L {x} {y} L {x} 200",
                        "collars": [get_h_collar(0, y), get_v_collar(x, 200)],
                        "arrows": [arrow_v(x, (y + 200) // 2, to_down=True, core_color=core)]
                    },
                    # 4. Down to Left
                    {
                        "dir": "down-to-left",
                        "path": f"M {x} 200 L {x} {y} L 0 {y}",
                        "collars": [get_v_collar(x, 200), get_h_collar(0, y)],
                        "arrows": [arrow_h(x // 2 if x > 30 else 24, y, to_right=False, core_color=core)]
                    },
                    # 5. Right to Up
                    {
                        "dir": "right-to-up",
                        "path": f"M 200 {y} L {x} {y} L {x} 0",
                        "collars": [get_h_collar(200, y), get_v_collar(x, 0)],
                        "arrows": [arrow_v(x, y // 2 if y > 30 else 24, to_down=False, core_color=core)]
                    },
                    # 6. Up to Right
                    {
                        "dir": "up-to-right",
                        "path": f"M {x} 0 L {x} {y} L 200 {y}",
                        "collars": [get_v_collar(x, 0), get_h_collar(200, y)],
                        "arrows": [arrow_h((x + 200) // 2, y, to_right=True, core_color=core)]
                    },
                    # 7. Right to Down
                    {
                        "dir": "right-to-down",
                        "path": f"M 200 {y} L {x} {y} L {x} 200",
                        "collars": [get_h_collar(200, y), get_v_collar(x, 200)],
                        "arrows": [arrow_v(x, (y + 200) // 2, to_down=True, core_color=core)]
                    },
                    # 8. Down to Right
                    {
                        "dir": "down-to-right",
                        "path": f"M {x} 200 L {x} {y} L 200 {y}",
                        "collars": [get_v_collar(x, 200), get_h_collar(200, y)],
                        "arrows": [arrow_h((x + 200) // 2, y, to_right=True, core_color=core)]
                    },
                ]

                for ev in elbow_variants:
                    dir_name = ev["dir"]
                    names = [
                        f"pipe-elbow-{y_name}-{x_name}-{dir_name}-fluid",
                    ]
                    # Also support existing naming conventions
                    if x_name == "center":
                        names.append(f"pipe-elbow-{y_name}-{dir_name}-fluid")
                    if y_name == "center" and x_name == "center":
                        names.append(f"pipe-elbow-{dir_name}-fluid")

                    for base_name in names:
                        with open(os.path.join(color_dir, f"{base_name}-static.svg"), "w", encoding="utf-8") as f:
                            f.write(render_svg(ev["path"], ev["collars"], ev["arrows"], core, pulse, False))
                        with open(os.path.join(color_dir, f"{base_name}-animated.svg"), "w", encoding="utf-8") as f:
                            f.write(render_svg(ev["path"], ev["collars"], ev["arrows"], core, pulse, True))
                        generated_count += 2

    print(f"Generated {generated_count} SVG files across 3 colors successfully.")

if __name__ == "__main__":
    main()
