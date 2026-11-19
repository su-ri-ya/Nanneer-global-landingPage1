import os
import shutil

output_dir = os.path.join("public", "schematic asserts", "pipe")
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)

# 3 Colors strictly from components/ScadaSchematicSimulation.tsx
COLORS = {
    "blue": {
        "color": "#0284C7",
        "pulse": "#BAE6FD",
        "desc": "Treated Water / Pure Effluent"
    },
    "brown": {
        "color": "#8D6E63",
        "pulse": "#D7CCC8",
        "desc": "Raw Sewage / Bio-Mix / Sludge"
    },
    "red": {
        "color": "#DC2626",
        "pulse": "#FCA5A5",
        "desc": "Drain / Backwash / Reject"
    }
}

# The 11 standard grid shapes matching the user's reference image (+ 4-way cross)
# Standard 48x48 canvas, center axis at (24, 24)
SHAPES = {
    # 1. Straight Horizontal (W <-> E)
    "straight-horizontal": {
        "path_fwd": "M 0 24 L 48 24",
        "path_rev": "M 48 24 L 0 24",
        "static_path": "M 0 24 L 48 24",
        "arrow_fwd": '<polygon points="21,21 27,24 21,27" fill="{color}" />',
        "arrow_rev": '<polygon points="27,21 21,24 27,27" fill="{color}" />',
    },

    # 2. Straight Vertical (N <-> S)
    "straight-vertical": {
        "path_fwd": "M 24 0 L 24 48",
        "path_rev": "M 24 48 L 24 0",
        "static_path": "M 24 0 L 24 48",
        "arrow_fwd": '<polygon points="21,21 24,27 27,21" fill="{color}" />',
        "arrow_rev": '<polygon points="21,27 24,21 27,27" fill="{color}" />',
    },

    # 3. Elbow: West to North (Bottom-Left in reference grid)
    "elbow-bottom-left": {
        "path_fwd": "M 0 24 L 24 24 L 24 0",
        "path_rev": "M 24 0 L 24 24 L 0 24",
        "static_path": "M 0 24 L 24 24 L 24 0",
        "arrow_fwd": '<polygon points="21,17 24,11 27,17" fill="{color}" />',
        "arrow_rev": '<polygon points="17,21 11,24 17,27" fill="{color}" />',
    },

    # 4. Elbow: South to East (Bottom-Right in reference grid)
    "elbow-bottom-right": {
        "path_fwd": "M 24 48 L 24 24 L 48 24",
        "path_rev": "M 48 24 L 24 24 L 24 48",
        "static_path": "M 24 48 L 24 24 L 48 24",
        "arrow_fwd": '<polygon points="31,21 37,24 31,27" fill="{color}" />',
        "arrow_rev": '<polygon points="21,31 24,37 27,31" fill="{color}" />',
    },

    # 5. Elbow: North to East (Top-Right in reference grid)
    "elbow-top-right": {
        "path_fwd": "M 24 0 L 24 24 L 48 24",
        "path_rev": "M 48 24 L 24 24 L 24 0",
        "static_path": "M 24 0 L 24 24 L 48 24",
        "arrow_fwd": '<polygon points="31,21 37,24 31,27" fill="{color}" />',
        "arrow_rev": '<polygon points="21,17 24,11 27,17" fill="{color}" />',
    },

    # 6. Elbow: West to South (Top-Left in reference grid)
    "elbow-top-left": {
        "path_fwd": "M 0 24 L 24 24 L 24 48",
        "path_rev": "M 24 48 L 24 24 L 0 24",
        "static_path": "M 0 24 L 24 24 L 24 48",
        "arrow_fwd": '<polygon points="21,31 24,37 27,31" fill="{color}" />',
        "arrow_rev": '<polygon points="17,21 11,24 17,27" fill="{color}" />',
    },

    # 7. Tee Horizontal Top (Horizontal with North branch)
    "tee-horizontal-top": {
        "path_fwd": "M 0 24 L 48 24 M 24 24 L 24 0",
        "static_path": "M 0 24 L 48 24 M 24 24 L 24 0",
        "arrow_fwd": '<polygon points="33,21 39,24 33,27" fill="{color}" /><polygon points="21,17 24,11 27,17" fill="{color}" />',
    },

    # 8. Tee Horizontal Bottom (Horizontal with South branch)
    "tee-horizontal-bottom": {
        "path_fwd": "M 0 24 L 48 24 M 24 24 L 24 48",
        "static_path": "M 0 24 L 48 24 M 24 24 L 24 48",
        "arrow_fwd": '<polygon points="33,21 39,24 33,27" fill="{color}" /><polygon points="21,31 24,37 27,31" fill="{color}" />',
    },

    # 9. Tee Vertical Left (Vertical with West branch)
    "tee-vertical-left": {
        "path_fwd": "M 24 0 L 24 48 M 24 24 L 0 24",
        "static_path": "M 24 0 L 24 48 M 24 24 L 0 24",
        "arrow_fwd": '<polygon points="21,33 24,39 27,33" fill="{color}" /><polygon points="17,21 11,24 17,27" fill="{color}" />',
    },

    # 10. Tee Vertical Right (Vertical with East branch)
    "tee-vertical-right": {
        "path_fwd": "M 24 0 L 24 48 M 24 24 L 48 24",
        "static_path": "M 24 0 L 24 48 M 24 24 L 48 24",
        "arrow_fwd": '<polygon points="21,33 24,39 27,33" fill="{color}" /><polygon points="31,21 37,24 31,27" fill="{color}" />',
    },

    # 11. 4-Way Cross
    "cross-four-way": {
        "path_fwd": "M 0 24 L 48 24 M 24 0 L 24 48",
        "static_path": "M 0 24 L 48 24 M 24 0 L 24 48",
        "arrow_fwd": '<polygon points="33,21 39,24 33,27" fill="{color}" /><polygon points="21,33 24,39 27,33" fill="{color}" />',
    }
}

# Template: Exact Schematic Animated Pipe
TEMPLATE_ANIMATED = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
  <!-- Solid Pipe Base (4.5px from Schematic) -->
  <path d="{path}" stroke="{color}" stroke-width="4.5" fill="none" stroke-linejoin="round" />

  <!-- Direction Indicator Arrow -->
  {arrow}

  <!-- Animated Fluid Flow Stream (2.5px with Dashoffset from Schematic) -->
  <path d="{path}" stroke="{pulse}" stroke-width="2.5" stroke-dasharray="5 7" fill="none" stroke-linejoin="round">
    <animate attributeName="stroke-dashoffset" from="24" to="0" dur="0.8s" repeatCount="indefinite" />
  </path>
</svg>"""

# Template: Exact Schematic Static Pipe
TEMPLATE_STATIC = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
  <!-- Solid Pipe Base (4.5px from Schematic) -->
  <path d="{path}" stroke="{color}" stroke-width="4.5" fill="none" stroke-linejoin="round" />
</svg>"""

# Template: Dry / Uncharged Steel Pipe
TEMPLATE_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
  <!-- Uncharged Metallic Steel Pipe (4.5px) -->
  <path d="{path}" stroke="#64748B" stroke-width="4.5" fill="none" stroke-linejoin="round" />
</svg>"""

print("=== GENERATING EXACT SCHEMATIC PIPELINE LIBRARY (48x48 GRID) ===")
count = 0

for shape_name, shape_data in SHAPES.items():
    static_path = shape_data["static_path"]

    # 1. Dry Static version
    dry_fname = f"pipe-{shape_name}-dry-static.svg"
    dry_svg = TEMPLATE_DRY.format(path=static_path)
    with open(os.path.join(output_dir, dry_fname), "w", encoding="utf-8") as f:
        f.write(dry_svg)
    count += 1

    # 2. 3 Colors in Static and Animated
    for color_name, color_data in COLORS.items():
        c_val = color_data["color"]
        p_val = color_data["pulse"]

        # Static with fluid
        static_fname = f"pipe-{shape_name}-{color_name}-static.svg"
        static_svg = TEMPLATE_STATIC.format(path=static_path, color=c_val)
        with open(os.path.join(output_dir, static_fname), "w", encoding="utf-8") as f:
            f.write(static_svg)
        count += 1

        # Animated forward
        anim_fname = f"pipe-{shape_name}-{color_name}-animated.svg"
        arrow_svg = shape_data["arrow_fwd"].format(color=c_val)
        anim_svg = TEMPLATE_ANIMATED.format(
            path=shape_data["path_fwd"],
            color=c_val,
            pulse=p_val,
            arrow=arrow_svg
        )
        with open(os.path.join(output_dir, anim_fname), "w", encoding="utf-8") as f:
            f.write(anim_svg)
        count += 1

        # Reverse animated if defined
        if "path_rev" in shape_data:
            anim_rev_fname = f"pipe-{shape_name}-{color_name}-reverse-animated.svg"
            arrow_rev_svg = shape_data["arrow_rev"].format(color=c_val)
            anim_rev_svg = TEMPLATE_ANIMATED.format(
                path=shape_data["path_rev"],
                color=c_val,
                pulse=p_val,
                arrow=arrow_rev_svg
            )
            with open(os.path.join(output_dir, anim_rev_fname), "w", encoding="utf-8") as f:
                f.write(anim_rev_svg)
            count += 1

print(f"\nDone! Successfully generated {count} exact schematic pipe SVGs in '{output_dir}'.")
