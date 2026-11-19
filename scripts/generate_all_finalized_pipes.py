import os
import shutil

output_dir = os.path.join("public", "schematic asserts", "pipe")
# Wipe out all other extra files and folders to keep ONLY these shapes
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)

# Colors: Blue, Brown, Red, Green
COLORS = {
    "blue": {
        "fluid": "#0284C7",
        "pulse": "#BAE6FD"
    },
    "brown": {
        "fluid": "#8D6E63",
        "pulse": "#D7CCC8"
    },
    "red": {
        "fluid": "#DC2626",
        "pulse": "#FCA5A5"
    },
    "green": {
        "fluid": "#16A34A",
        "pulse": "#BBF7D0"
    }
}

# The 10 Grid Tile Shapes from the user's uploaded reference image (+ 4-way cross)
# Canvas is standard 200 x 200, center at (100, 100)
# Flange collars at connection boundaries:
#   Left (W): x=0, y=92, w=6, h=16
#   Right (E): x=194, y=92, w=6, h=16
#   Top (N): x=92, y=0, w=16, h=6
#   Bottom (S): x=92, y=194, w=16, h=6
SHAPES = {
    # 1. Straight Pipes
    "straight-horizontal": {
        "path_forward": "M 0 100 L 200 100",
        "path_reverse": "M 200 100 L 0 100",
        "static_path": "M 0 100 L 200 100",
        "collars": [(0, 92, 6, 16), (194, 92, 6, 16)],
        "arrow_forward": '<polygon points="108,96 118,100 108,104" fill="{fluid}" />',
        "arrow_reverse": '<polygon points="92,104 82,100 92,96" fill="{fluid}" />',
    },
    "straight-vertical": {
        "path_forward": "M 100 0 L 100 200",
        "path_reverse": "M 100 200 L 100 0",
        "static_path": "M 100 0 L 100 200",
        "collars": [(92, 0, 16, 6), (92, 194, 16, 6)],
        "arrow_forward": '<polygon points="96,108 100,118 104,108" fill="{fluid}" />',
        "arrow_reverse": '<polygon points="96,92 100,82 104,92" fill="{fluid}" />',
    },

    # 2. 90-Degree Elbows (Matching rows 1 & 2 in uploaded photo)
    "elbow-bottom-left": { # Connects Left (West) and Top (North)
        "path_forward": "M 0 100 L 100 100 L 100 0",
        "path_reverse": "M 100 0 L 100 100 L 0 100",
        "static_path": "M 0 100 L 100 100 L 100 0",
        "collars": [(0, 92, 6, 16), (92, 0, 16, 6)],
        "arrow_forward": '<polygon points="96,55 100,45 104,55" fill="{fluid}" />',
        "arrow_reverse": '<polygon points="55,104 45,100 55,96" fill="{fluid}" />',
    },
    "elbow-bottom-right": { # Connects Bottom (South) and Right (East)
        "path_forward": "M 100 200 L 100 100 L 200 100",
        "path_reverse": "M 200 100 L 100 100 L 100 200",
        "static_path": "M 100 200 L 100 100 L 200 100",
        "collars": [(92, 194, 16, 6), (194, 92, 6, 16)],
        "arrow_forward": '<polygon points="145,96 155,100 145,104" fill="{fluid}" />',
        "arrow_reverse": '<polygon points="96,145 100,155 104,145" fill="{fluid}" />',
    },
    "elbow-top-right": { # Connects Top (North) and Right (East)
        "path_forward": "M 100 0 L 100 100 L 200 100",
        "path_reverse": "M 200 100 L 100 100 L 100 0",
        "static_path": "M 100 0 L 100 100 L 200 100",
        "collars": [(92, 0, 16, 6), (194, 92, 6, 16)],
        "arrow_forward": '<polygon points="145,96 155,100 145,104" fill="{fluid}" />',
        "arrow_reverse": '<polygon points="96,55 100,45 104,55" fill="{fluid}" />',
    },
    "elbow-top-left": { # Connects Left (West) and Bottom (South)
        "path_forward": "M 0 100 L 100 100 L 100 200",
        "path_reverse": "M 100 200 L 100 100 L 0 100",
        "static_path": "M 0 100 L 100 100 L 100 200",
        "collars": [(0, 92, 6, 16), (92, 194, 16, 6)],
        "arrow_forward": '<polygon points="96,145 100,155 104,145" fill="{fluid}" />',
        "arrow_reverse": '<polygon points="55,104 45,100 55,96" fill="{fluid}" />',
    },

    # 3. T-Junctions / Tees
    "tee-horizontal-top": { # Horizontal with North branch
        "path_forward": "M 0 100 L 200 100 M 100 100 L 100 0",
        "static_path": "M 0 100 L 200 100 M 100 100 L 100 0",
        "collars": [(0, 92, 6, 16), (194, 92, 6, 16), (92, 0, 16, 6)],
        "arrow_forward": '<polygon points="108,96 118,100 108,104" fill="{fluid}" /><polygon points="96,55 100,45 104,55" fill="{fluid}" />',
    },
    "tee-horizontal-bottom": { # Horizontal with South branch
        "path_forward": "M 0 100 L 200 100 M 100 100 L 100 200",
        "static_path": "M 0 100 L 200 100 M 100 100 L 100 200",
        "collars": [(0, 92, 6, 16), (194, 92, 6, 16), (92, 194, 16, 6)],
        "arrow_forward": '<polygon points="108,96 118,100 108,104" fill="{fluid}" /><polygon points="96,145 100,155 104,145" fill="{fluid}" />',
    },
    "tee-vertical-left": { # Vertical with West branch
        "path_forward": "M 100 0 L 100 200 M 100 100 L 0 100",
        "static_path": "M 100 0 L 100 200 M 100 100 L 0 100",
        "collars": [(92, 0, 16, 6), (92, 194, 16, 6), (0, 92, 6, 16)],
        "arrow_forward": '<polygon points="96,108 100,118 104,108" fill="{fluid}" /><polygon points="55,104 45,100 55,96" fill="{fluid}" />',
    },
    "tee-vertical-right": { # Vertical with East branch
        "path_forward": "M 100 0 L 100 200 M 100 100 L 200 100",
        "static_path": "M 100 0 L 100 200 M 100 100 L 200 100",
        "collars": [(92, 0, 16, 6), (92, 194, 16, 6), (194, 92, 6, 16)],
        "arrow_forward": '<polygon points="96,108 100,118 104,108" fill="{fluid}" /><polygon points="145,96 155,100 145,104" fill="{fluid}" />',
    },

    # 4. 4-Way Cross
    "cross-four-way": { # N-S and W-E intersection
        "path_forward": "M 0 100 L 200 100 M 100 0 L 100 200",
        "static_path": "M 0 100 L 200 100 M 100 0 L 100 200",
        "collars": [(0, 92, 6, 16), (194, 92, 6, 16), (92, 0, 16, 6), (92, 194, 16, 6)],
        "arrow_forward": '<polygon points="145,96 155,100 145,104" fill="{fluid}" /><polygon points="96,145 100,155 104,145" fill="{fluid}" />',
    }
}

def render_collars(collars):
    elements = []
    for x, y, w, h in collars:
        elements.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.5" fill="#CBD5E1" stroke="#475569" stroke-width="0.8" />')
    return "\n  ".join(elements)

# Template for Fluid Animated Pipe
TEMPLATE_ANIMATED = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="pipeShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="2.5" flood-color="#0F172A" flood-opacity="0.3" />
    </filter>
    <linearGradient id="ssPipeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748B" />
      <stop offset="25%" stop-color="#FFFFFF" />
      <stop offset="55%" stop-color="#CBD5E1" />
      <stop offset="85%" stop-color="#94A3B8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>
  </defs>

  <!-- 1. Heavy Stainless Steel 316 Outer Casing (8px with 3D Drop Shadow) -->
  <path d="{path}" stroke="url(#ssPipeGrad)" stroke-width="8" fill="none" stroke-linejoin="round" filter="url(#pipeShadow)" />

  <!-- 2. Process Fluid Core (5px) -->
  <path d="{path}" stroke="{fluid}" stroke-width="5" fill="none" stroke-linejoin="round" />

  <!-- 3. Animated Flow Stream Dashes (2.5px with SVG animate) -->
  <path d="{path}" stroke="{pulse}" stroke-width="2.5" stroke-dasharray="6 8" fill="none" stroke-linejoin="round">
    <animate attributeName="stroke-dashoffset" from="28" to="0" dur="0.8s" repeatCount="indefinite" />
  </path>

  <!-- Flow Direction Arrow -->
  {arrow}

  <!-- ANSI Flange Pipe Connection Collars -->
  {collars}
</svg>"""

# Template for Static Fluid Pipe
TEMPLATE_STATIC = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="pipeShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="2.5" flood-color="#0F172A" flood-opacity="0.3" />
    </filter>
    <linearGradient id="ssPipeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748B" />
      <stop offset="25%" stop-color="#FFFFFF" />
      <stop offset="55%" stop-color="#CBD5E1" />
      <stop offset="85%" stop-color="#94A3B8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>
  </defs>

  <!-- 1. Heavy Stainless Steel 316 Outer Casing (8px with 3D Drop Shadow) -->
  <path d="{path}" stroke="url(#ssPipeGrad)" stroke-width="8" fill="none" stroke-linejoin="round" filter="url(#pipeShadow)" />

  <!-- 2. Process Fluid Core (5px) -->
  <path d="{path}" stroke="{fluid}" stroke-width="5" fill="none" stroke-linejoin="round" />

  <!-- ANSI Flange Pipe Connection Collars -->
  {collars}
</svg>"""

# Template for Dry / Empty Pipe (No fluid core)
TEMPLATE_DRY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <filter id="pipeShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="2.5" flood-color="#0F172A" flood-opacity="0.3" />
    </filter>
    <linearGradient id="ssPipeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#64748B" />
      <stop offset="25%" stop-color="#FFFFFF" />
      <stop offset="55%" stop-color="#CBD5E1" />
      <stop offset="85%" stop-color="#94A3B8" />
      <stop offset="100%" stop-color="#475569" />
    </linearGradient>
  </defs>

  <!-- 1. Heavy Stainless Steel 316 Outer Casing (Dry / Empty 8px with 3D Drop Shadow) -->
  <path d="{path}" stroke="url(#ssPipeGrad)" stroke-width="8" fill="none" stroke-linejoin="round" filter="url(#pipeShadow)" />

  <!-- ANSI Flange Pipe Connection Collars -->
  {collars}
</svg>"""

print("=== GENERATING COMPLETE MODULAR GRID PIPE MATRIX IN 'public/schematic asserts/pipe' ===")
count = 0

for shape_name, shape_data in SHAPES.items():
    collars_markup = render_collars(shape_data["collars"])
    static_path = shape_data["static_path"]

    # 1. Generate Dry / Empty version (1 per shape)
    dry_fname = f"pipe-{shape_name}-dry-static.svg"
    dry_svg = TEMPLATE_DRY.format(path=static_path, collars=collars_markup)
    with open(os.path.join(output_dir, dry_fname), "w", encoding="utf-8") as f:
        f.write(dry_svg)
    count += 1

    # 2. Generate 3 Colors (Blue, Brown, Red) in both Static and Animated
    for color_name, color_vals in COLORS.items():
        fluid_color = color_vals["fluid"]
        pulse_color = color_vals["pulse"]

        # Static with fluid
        static_fname = f"pipe-{shape_name}-{color_name}-static.svg"
        static_svg = TEMPLATE_STATIC.format(path=static_path, fluid=fluid_color, collars=collars_markup)
        with open(os.path.join(output_dir, static_fname), "w", encoding="utf-8") as f:
            f.write(static_svg)
        count += 1

        # Animated forward flow
        anim_fname = f"pipe-{shape_name}-{color_name}-animated.svg"
        arrow_markup = shape_data["arrow_forward"].format(fluid=fluid_color)
        anim_svg = TEMPLATE_ANIMATED.format(
            path=shape_data["path_forward"],
            fluid=fluid_color,
            pulse=pulse_color,
            arrow=arrow_markup,
            collars=collars_markup
        )
        with open(os.path.join(output_dir, anim_fname), "w", encoding="utf-8") as f:
            f.write(anim_svg)
        count += 1

        # If shape has a distinct reverse path, generate reverse animated as well
        if "path_reverse" in shape_data:
            anim_rev_fname = f"pipe-{shape_name}-{color_name}-reverse-animated.svg"
            arrow_rev_markup = shape_data["arrow_reverse"].format(fluid=fluid_color)
            anim_rev_svg = TEMPLATE_ANIMATED.format(
                path=shape_data["path_reverse"],
                fluid=fluid_color,
                pulse=pulse_color,
                arrow=arrow_rev_markup,
                collars=collars_markup
            )
            with open(os.path.join(output_dir, anim_rev_fname), "w", encoding="utf-8") as f:
                f.write(anim_rev_svg)
            count += 1

print(f"\nDone! Successfully generated {count} modular pipeline SVGs in '{output_dir}'.")
