import os
import shutil

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

POSITIONS = [
    ("top-left", 48, 48),
    ("top-center", 100, 48),
    ("top-right", 150, 48),
    ("center-left", 48, 100),
    ("center-center", 100, 100),
    ("center-right", 150, 100),
    ("bottom-left", 48, 150),
    ("bottom-center", 100, 150),
    ("bottom-right", 150, 150),
]

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
    css_style = ""
    if is_animated:
        css_style = """    <style>
      @keyframes p-flow-anim {
        from { stroke-dashoffset: 28; }
        to { stroke-dashoffset: 0; }
      }
      .anim-p-flow {
        stroke-dasharray: 6 8;
        animation: p-flow-anim 0.8s linear infinite;
      }
    </style>
"""
    defs = f"""  <defs>
{css_style}    <filter id="ssPipeShadow" x="-15%" y="-15%" width="130%" height="130%">
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
        anim_layer = f"""\n  <!-- 2.5px Animated Flow Dashes (SMIL + CSS for universal animation support) -->
  <path d="{path_d}" stroke="{pulse_color}" stroke-width="2.5" stroke-dasharray="6 8" stroke-linecap="round" stroke-linejoin="round" fill="none" class="anim-p-flow">
    <animate attributeName="stroke-dashoffset" from="28" to="0" dur="0.8s" repeatCount="indefinite" />
  </path>"""

    arrow_layer = ""
    if is_animated and arrows:
        arrow_layer = "\n  " + "\n  ".join(arrows)

    collar_layer = ""
    if collars:
        collar_layer = "\n  " + "\n  ".join(collars)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
{defs}
{body}{anim_layer}{arrow_layer}{collar_layer}
</svg>"""

def build_pipe_collection(core_color):
    files = {}

    # -------------------------------------------------------------------------
    # 1. 4-WAY CROSS (┼) (9 Positions)
    # -------------------------------------------------------------------------
    for pos, x, y in POSITIONS:
        path = f"M 0 {y} L 200 {y} M {x} 0 L {x} 200"
        collars = [get_h_collar(0, y), get_h_collar(200, y), get_v_collar(x, 0), get_v_collar(x, 200)]
        arr_x = 155 if x <= 100 else 60
        arr_y = 155 if y <= 100 else 60
        arrows = [arrow_h(arr_x, y, True, core_color), arrow_v(x, arr_y, True, core_color)]

        names = [f"pipe-cross-4way-{pos}-fluid"]
        if pos == "center-center":
            names.append("pipe-cross-4way-center-fluid")

        for name in names:
            files[name] = {"path": path, "collars": collars, "arrows": arrows}

    # -------------------------------------------------------------------------
    # 2. TEE BRANCH UP (┴) (9 Positions)
    # -------------------------------------------------------------------------
    for pos, x, y in POSITIONS:
        path = f"M 0 {y} L 200 {y} M {x} {y} L {x} 0"
        collars = [get_h_collar(0, y), get_h_collar(200, y), get_v_collar(x, 0)]
        arr_x = 155 if x <= 100 else 60
        arr_y = y // 2 if y > 30 else 24
        arrows = [arrow_h(arr_x, y, True, core_color), arrow_v(x, arr_y, False, core_color)]

        names = [
            f"pipe-tee-branch-up-{pos}-fluid",
            f"pipe-tee-header-{pos.split('-')[0]}-branch-{pos.split('-')[1]}-up-fluid"
        ]
        if pos == "center-center":
            names.extend(["pipe-tee-center-header-branch-up-fluid", "pipe-tee-branch-up-fluid"])
        elif pos == "bottom-center":
            names.append("pipe-tee-bottom-header-branch-up-fluid")

        for name in names:
            files[name] = {"path": path, "collars": collars, "arrows": arrows}

    # -------------------------------------------------------------------------
    # 3. TEE BRANCH DOWN (┬) (9 Positions)
    # -------------------------------------------------------------------------
    for pos, x, y in POSITIONS:
        path = f"M 0 {y} L 200 {y} M {x} {y} L {x} 200"
        collars = [get_h_collar(0, y), get_h_collar(200, y), get_v_collar(x, 200)]
        arr_x = 155 if x <= 100 else 60
        arr_y = (y + 200) // 2
        arrows = [arrow_h(arr_x, y, True, core_color), arrow_v(x, arr_y, True, core_color)]

        names = [
            f"pipe-tee-branch-down-{pos}-fluid",
            f"pipe-tee-header-{pos.split('-')[0]}-branch-{pos.split('-')[1]}-down-fluid"
        ]
        if pos == "center-center":
            names.extend(["pipe-tee-center-header-branch-down-fluid", "pipe-tee-branch-down-fluid"])
        elif pos == "top-center":
            names.append("pipe-tee-top-header-branch-down-fluid")

        for name in names:
            files[name] = {"path": path, "collars": collars, "arrows": arrows}

    # -------------------------------------------------------------------------
    # 4. TEE BRANCH LEFT (┤) (9 Positions)
    # -------------------------------------------------------------------------
    for pos, x, y in POSITIONS:
        path = f"M {x} 0 L {x} 200 M {x} {y} L 0 {y}"
        collars = [get_v_collar(x, 0), get_v_collar(x, 200), get_h_collar(0, y)]
        arr_y = 155 if y <= 100 else 60
        arr_x = x // 2 if x > 30 else 24
        arrows = [arrow_v(x, arr_y, True, core_color), arrow_h(arr_x, y, False, core_color)]

        names = [
            f"pipe-tee-branch-left-{pos}-fluid",
            f"pipe-tee-header-{pos.split('-')[1]}-branch-{pos.split('-')[0]}-left-fluid"
        ]
        if pos == "center-center":
            names.extend(["pipe-tee-vertical-center-branch-left-fluid", "pipe-tee-branch-left-fluid"])

        for name in names:
            files[name] = {"path": path, "collars": collars, "arrows": arrows}

    # -------------------------------------------------------------------------
    # 5. TEE BRANCH RIGHT (├) (9 Positions)
    # -------------------------------------------------------------------------
    for pos, x, y in POSITIONS:
        path = f"M {x} 0 L {x} 200 M {x} {y} L 200 {y}"
        collars = [get_v_collar(x, 0), get_v_collar(x, 200), get_h_collar(200, y)]
        arr_y = 155 if y <= 100 else 60
        arr_x = (x + 200) // 2
        arrows = [arrow_v(x, arr_y, True, core_color), arrow_h(arr_x, y, True, core_color)]

        names = [
            f"pipe-tee-branch-right-{pos}-fluid",
            f"pipe-tee-header-{pos.split('-')[1]}-branch-{pos.split('-')[0]}-right-fluid"
        ]
        if pos == "center-center":
            names.extend(["pipe-tee-vertical-center-branch-right-fluid", "pipe-tee-branch-right-fluid"])

        for name in names:
            files[name] = {"path": path, "collars": collars, "arrows": arrows}

    # -------------------------------------------------------------------------
    # 6. ELBOW 1: Left ↔ Up (Panel 3 in image) (9 Positions x 2 Directions)
    # -------------------------------------------------------------------------
    for pos, x, y in POSITIONS:
        collars = [get_h_collar(0, y), get_v_collar(x, 0)]
        arr_y = y // 2 if y > 30 else 24
        arr_x = x // 2 if x > 30 else 24
        y_name, x_name = pos.split("-")

        # Left to Up
        p_lu = f"M 0 {y} L {x} {y} L {x} 0"
        names_lu = [
            f"pipe-elbow-left-to-up-{pos}-fluid",
            f"pipe-elbow-{y_name}-{x_name}-left-to-up-fluid"
        ]
        if x_name == "center":
            names_lu.append(f"pipe-elbow-{y_name}-left-to-up-fluid")
        if pos == "center-center":
            names_lu.append("pipe-elbow-left-to-up-fluid")

        for n in names_lu:
            files[n] = {"path": p_lu, "collars": collars, "arrows": [arrow_v(x, arr_y, False, core_color)]}

        # Up to Left
        p_ul = f"M {x} 0 L {x} {y} L 0 {y}"
        names_ul = [
            f"pipe-elbow-up-to-left-{pos}-fluid",
            f"pipe-elbow-{y_name}-{x_name}-up-to-left-fluid"
        ]
        if x_name == "center":
            names_ul.append(f"pipe-elbow-{y_name}-up-to-left-fluid")
        if pos == "center-center":
            names_ul.append("pipe-elbow-up-to-left-fluid")

        for n in names_ul:
            files[n] = {"path": p_ul, "collars": collars, "arrows": [arrow_h(arr_x, y, False, core_color)]}

    # -------------------------------------------------------------------------
    # 7. ELBOW 2: Down ↔ Right (Panel 4 in image) (9 Positions x 2 Directions)
    # -------------------------------------------------------------------------
    for pos, x, y in POSITIONS:
        collars = [get_v_collar(x, 200), get_h_collar(200, y)]
        arr_x = (x + 200) // 2
        arr_y = (y + 200) // 2
        y_name, x_name = pos.split("-")

        # Down to Right
        p_dr = f"M {x} 200 L {x} {y} L 200 {y}"
        names_dr = [
            f"pipe-elbow-down-to-right-{pos}-fluid",
            f"pipe-elbow-{y_name}-{x_name}-down-to-right-fluid"
        ]
        if x_name == "center":
            names_dr.append(f"pipe-elbow-{y_name}-down-to-right-fluid")
        if pos == "center-center":
            names_dr.append("pipe-elbow-down-to-right-fluid")

        for n in names_dr:
            files[n] = {"path": p_dr, "collars": collars, "arrows": [arrow_h(arr_x, y, True, core_color)]}

        # Right to Down
        p_rd = f"M 200 {y} L {x} {y} L {x} 200"
        names_rd = [
            f"pipe-elbow-right-to-down-{pos}-fluid",
            f"pipe-elbow-{y_name}-{x_name}-right-to-down-fluid"
        ]
        if x_name == "center":
            names_rd.append(f"pipe-elbow-{y_name}-right-to-down-fluid")
        if pos == "center-center":
            names_rd.append("pipe-elbow-right-to-down-fluid")

        for n in names_rd:
            files[n] = {"path": p_rd, "collars": collars, "arrows": [arrow_v(x, arr_y, True, core_color)]}

    # -------------------------------------------------------------------------
    # 8. ELBOW 3: Top ↔ Right (Panel 5 in image) (9 Positions x 2 Directions)
    # -------------------------------------------------------------------------
    for pos, x, y in POSITIONS:
        collars = [get_v_collar(x, 0), get_h_collar(200, y)]
        arr_x = (x + 200) // 2
        arr_y = y // 2 if y > 30 else 24
        y_name, x_name = pos.split("-")

        # Top to Right
        p_tr = f"M {x} 0 L {x} {y} L 200 {y}"
        names_tr = [
            f"pipe-elbow-top-to-right-{pos}-fluid",
            f"pipe-elbow-{y_name}-{x_name}-up-to-right-fluid"
        ]
        if x_name == "center":
            names_tr.append(f"pipe-elbow-{y_name}-up-to-right-fluid")
        if pos == "center-center":
            names_tr.extend(["pipe-elbow-up-to-right-fluid", "pipe-elbow-center-up-to-right-fluid"])

        for n in names_tr:
            files[n] = {"path": p_tr, "collars": collars, "arrows": [arrow_h(arr_x, y, True, core_color)]}

        # Right to Up
        p_ru = f"M 200 {y} L {x} {y} L {x} 0"
        names_ru = [
            f"pipe-elbow-right-to-up-{pos}-fluid",
            f"pipe-elbow-{y_name}-{x_name}-right-to-up-fluid"
        ]
        if x_name == "center":
            names_ru.append(f"pipe-elbow-{y_name}-right-to-up-fluid")
        if pos == "center-center":
            names_ru.extend(["pipe-elbow-right-to-up-fluid", "pipe-elbow-center-right-to-up-fluid"])

        for n in names_ru:
            files[n] = {"path": p_ru, "collars": collars, "arrows": [arrow_v(x, arr_y, False, core_color)]}

    # -------------------------------------------------------------------------
    # 9. ELBOW 4: Left ↔ Down (Panel 6 in image) (9 Positions x 2 Directions)
    # -------------------------------------------------------------------------
    for pos, x, y in POSITIONS:
        collars = [get_h_collar(0, y), get_v_collar(x, 200)]
        arr_y = (y + 200) // 2
        arr_x = x // 2 if x > 30 else 24
        y_name, x_name = pos.split("-")

        # Left to Down
        p_ld = f"M 0 {y} L {x} {y} L {x} 200"
        names_ld = [
            f"pipe-elbow-left-to-down-{pos}-fluid",
            f"pipe-elbow-{y_name}-{x_name}-left-to-down-fluid"
        ]
        if x_name == "center":
            names_ld.append(f"pipe-elbow-{y_name}-left-to-down-fluid")
        if pos == "center-center":
            names_ld.extend(["pipe-elbow-left-to-down-fluid", "pipe-elbow-center-left-to-down-fluid"])

        for n in names_ld:
            files[n] = {"path": p_ld, "collars": collars, "arrows": [arrow_v(x, arr_y, True, core_color)]}

        # Down to Left
        p_dl = f"M {x} 200 L {x} {y} L 0 {y}"
        names_dl = [
            f"pipe-elbow-down-to-left-{pos}-fluid",
            f"pipe-elbow-{y_name}-{x_name}-down-to-left-fluid"
        ]
        if x_name == "center":
            names_dl.append(f"pipe-elbow-{y_name}-down-to-left-fluid")
        if pos == "center-center":
            names_dl.extend(["pipe-elbow-down-to-left-fluid", "pipe-elbow-center-down-to-left-fluid"])

        for n in names_dl:
            files[n] = {"path": p_dl, "collars": collars, "arrows": [arrow_h(arr_x, y, False, core_color)]}

    # -------------------------------------------------------------------------
    # 10. STRAIGHT HORIZONTAL (Panel 1 in image) (3 Tracks x 2 Directions)
    # -------------------------------------------------------------------------
    h_tracks = [("top", 48), ("center", 100), ("bottom", 150)]
    for y_name, y in h_tracks:
        collars = [get_h_collar(0, y), get_h_collar(200, y)]
        # Left to Right
        p_lr = f"M 0 {y} L 200 {y}"
        files[f"pipe-straight-horizontal-{y_name}-left-to-right-fluid"] = {
            "path": p_lr, "collars": collars, "arrows": [arrow_h(100, y, True, core_color)]
        }
        # Right to Left
        p_rl = f"M 200 {y} L 0 {y}"
        files[f"pipe-straight-horizontal-{y_name}-right-to-left-fluid"] = {
            "path": p_rl, "collars": collars, "arrows": [arrow_h(100, y, False, core_color)]
        }

    # -------------------------------------------------------------------------
    # 11. STRAIGHT VERTICAL (Panel 2 in image) (3 Tracks x 2 Directions)
    # -------------------------------------------------------------------------
    v_tracks = [("left", 48), ("center", 100), ("right", 150)]
    for x_name, x in v_tracks:
        collars = [get_v_collar(x, 0), get_v_collar(x, 200)]
        # Top to Bottom
        p_tb = f"M {x} 0 L {x} 200"
        files[f"pipe-straight-vertical-{x_name}-top-to-bottom-fluid"] = {
            "path": p_tb, "collars": collars, "arrows": [arrow_v(x, 100, True, core_color)]
        }
        # Bottom to Top
        p_bt = f"M {x} 200 L {x} 0"
        files[f"pipe-straight-vertical-{x_name}-bottom-to-top-fluid"] = {
            "path": p_bt, "collars": collars, "arrows": [arrow_v(x, 100, False, core_color)]
        }

    return files

def main():
    for color_name, c_data in COLORS.items():
        color_dir = os.path.join(BASE_DIR, color_name)
        # Clear existing directory cleanly
        if os.path.exists(color_dir):
            shutil.rmtree(color_dir)
        os.makedirs(color_dir, exist_ok=True)

        core = c_data["core"]
        pulse = c_data["pulse"]

        collection = build_pipe_collection(core)
        print(f"Generating {len(collection) * 2} files for {color_name}...")

        for base_name, data in collection.items():
            path_d = data["path"]
            collars = data["collars"]
            arrows = data["arrows"]

            # Static
            static_svg = render_svg(path_d, collars, arrows, core, pulse, False)
            with open(os.path.join(color_dir, f"{base_name}-static.svg"), "w", encoding="utf-8") as f:
                f.write(static_svg)

            # Animated
            anim_svg = render_svg(path_d, collars, arrows, core, pulse, True)
            with open(os.path.join(color_dir, f"{base_name}-animated.svg"), "w", encoding="utf-8") as f:
                f.write(anim_svg)

    print("Rebuild complete.")

if __name__ == "__main__":
    main()
