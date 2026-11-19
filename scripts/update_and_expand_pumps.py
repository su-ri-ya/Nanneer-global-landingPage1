import os

pumps_dir = os.path.join("public", "schematic-assets", "pumps")

# Reusable flange snippets for Centrifugal Pumps
# Canvas is 300 x 264. Volute center is at (150, 132), outer casing r=66 (bounds: x in [84, 216], y in [66, 198]).
# Left-to-Right: Suction on Left (attaches to x=84), Discharge on Top (attaches to y=66).
nozzles_l2r = """  <!-- Suction (Left) & Discharge (Top) Flanged Nozzles -->
  <rect x="64" y="119" width="20" height="26" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="56" y="115" width="8" height="34" rx="2" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/>
  <rect x="137" y="46" width="26" height="20" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="133" y="38" width="34" height="8" rx="2" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/>"""

# Right-to-Left: Suction on Right (attaches to x=216), Discharge on Top (attaches to y=66).
nozzles_r2l = """  <!-- Suction (Right) & Discharge (Top) Flanged Nozzles -->
  <rect x="216" y="119" width="20" height="26" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="236" y="115" width="8" height="34" rx="2" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/>
  <rect x="137" y="46" width="26" height="20" rx="2" fill="#334155" stroke="#64748b" stroke-width="2"/>
  <rect x="133" y="38" width="34" height="8" rx="2" fill="#475569" stroke="#94a3b8" stroke-width="1.5"/>"""

def clean_centrifugal_content(content, is_r2l=False):
    # Strip everything from <!-- Flush Connection Nozzles to </svg>
    idx = content.find("<!-- Flush Connection Nozzles")
    if idx == -1:
        idx = content.find("<path d=\"M 0 132")
    if idx == -1:
        idx = content.find("<path d=\"M 300 132")
    
    if idx != -1:
        body = content[:idx].rstrip()
    else:
        # Fallback: remove end tag
        body = content.replace("</svg>", "").rstrip()

    # Also clean unused ssPipe defs if present
    # Keep standard bottomShadow, softShadow, specularSheen, styles, cp_case, cp_fluid
    nozzles = nozzles_r2l if is_r2l else nozzles_l2r
    return body + "\n" + nozzles + "\n</svg>"

# Step 1: Clean all 24 centrifugal pump files
centrifugal_types = [
    "centrifugal-pump-dn100-flow-left-to-right",
    "centrifugal-pump-dn100-flow-right-to-left",
    "centrifugal-pump-dn50-flow-left-to-right",
    "centrifugal-pump-dn50-flow-right-to-left",
    "centrifugal-pump-dn25-flow-left-to-right",
    "centrifugal-pump-dn25-flow-right-to-left",
]

states = ["running-animated", "running-static", "stopped-static", "fault-animated"]

cleaned_count = 0
for base in centrifugal_types:
    is_r2l = "right-to-left" in base
    for s in states:
        fname = f"{base}-{s}.svg"
        fpath = os.path.join(pumps_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as fp:
                c = fp.read()
            c_clean = clean_centrifugal_content(c, is_r2l)
            with open(fpath, "w", encoding="utf-8") as fp:
                fp.write(c_clean)
            cleaned_count += 1

print(f"Cleaned {cleaned_count} centrifugal pump files (removed embedded pipes & edge collars).")

# Step 2: Generate standby-static.svg for all 14 pump types

# Helper for centrifugal standby
def build_centrifugal_standby(base, is_r2l):
    src_file = os.path.join(pumps_dir, f"{base}-stopped-static.svg")
    with open(src_file, "r", encoding="utf-8") as fp:
        c = fp.read()
    
    # In stopped-static, indicator ring is: stroke="#475569"
    # Change status ring to amber #f59e0b for standby ready
    c_standby = c.replace('stroke="#475569" stroke-width="3" stroke-dasharray="4 2"', 'stroke="#f59e0b" stroke-width="3" stroke-dasharray="4 2"')
    c_standby = c_standby.replace('fill="#0f172a" stroke="#64748b" stroke-width="2"', 'fill="#0f172a" stroke="#f59e0b" stroke-width="2"')
    c_standby = c_standby.replace('fill="#64748b"/>\n  </g>', 'fill="#f59e0b"/>\n  </g>')
    return c_standby

# Helper for chemical dosing pump standby
def build_chemical_standby(base):
    src_file = os.path.join(pumps_dir, f"{base}-stopped-static.svg")
    with open(src_file, "r", encoding="utf-8") as fp:
        c = fp.read()
    # Replace stopped indicator stroke="#475569" with stroke="#f59e0b"
    c_standby = c.replace('stroke="#475569" stroke-width="2"', 'stroke="#f59e0b" stroke-width="2.5"')
    c_standby = c_standby.replace('fill="#f43f5e" opacity="0.2"', 'fill="#f59e0b" opacity="0.4"')
    return c_standby

# Helper for RO pump standby
def build_ro_standby(base):
    src_file = os.path.join(pumps_dir, f"{base}-stopped-static.svg")
    with open(src_file, "r", encoding="utf-8") as fp:
        c = fp.read()
    # Replace stopped indicator stroke="#475569" with stroke="#f59e0b"
    c_standby = c.replace('stroke="#475569" stroke-width="1.5"', 'stroke="#f59e0b" stroke-width="2.5"')
    return c_standby

# Helper for Submersible Sump pump standby
def build_sump_standby(base):
    src_file = os.path.join(pumps_dir, f"{base}-stopped-static.svg")
    with open(src_file, "r", encoding="utf-8") as fp:
        c = fp.read()
    # Replace stopped indicator stroke="#475569" with stroke="#f59e0b"
    c_standby = c.replace('stroke="#475569" stroke-width="3"', 'stroke="#f59e0b" stroke-width="3"')
    return c_standby

# Generate the 14 standby files
standby_map = {
    # 6 Centrifugal
    "centrifugal-pump-dn100-flow-left-to-right": lambda b: build_centrifugal_standby(b, False),
    "centrifugal-pump-dn100-flow-right-to-left": lambda b: build_centrifugal_standby(b, True),
    "centrifugal-pump-dn50-flow-left-to-right": lambda b: build_centrifugal_standby(b, False),
    "centrifugal-pump-dn50-flow-right-to-left": lambda b: build_centrifugal_standby(b, True),
    "centrifugal-pump-dn25-flow-left-to-right": lambda b: build_centrifugal_standby(b, False),
    "centrifugal-pump-dn25-flow-right-to-left": lambda b: build_centrifugal_standby(b, True),
    # 2 Chemical Dosing
    "chemical-dosing-pump-dn15": build_chemical_standby,
    "chemical-dosing-pump-dn25": build_chemical_standby,
    # 4 RO High Pressure
    "ro-high-pressure-pump-dn25": build_ro_standby,
    "ro-high-pressure-pump-dn25-flow-right-to-left": build_ro_standby,
    "ro-high-pressure-pump-dn50": build_ro_standby,
    "ro-high-pressure-pump-dn50-flow-right-to-left": build_ro_standby,
    # 2 Submersible Sump
    "submersible-sump-pump-dn100": build_sump_standby,
    "submersible-sump-pump-dn50": build_sump_standby,
}

created_standby = 0
for base, builder in standby_map.items():
    content = builder(base)
    fname = f"{base}-standby-static.svg"
    fpath = os.path.join(pumps_dir, fname)
    with open(fpath, "w", encoding="utf-8") as fp:
        fp.write(content)
    created_standby += 1
    print(f"Generated standby state: {fname}")

print(f"\nSuccessfully generated {created_standby} standby pump SVGs!")
