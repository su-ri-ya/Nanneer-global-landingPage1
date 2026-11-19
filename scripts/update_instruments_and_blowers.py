import os

inst_dir = os.path.join("public", "schematic-assets", "instruments-utilities")

# 1. Generate the 3 Standby Aeration Blower SVGs
# Left-to-Right Standby
with open(os.path.join(inst_dir, "aeration-blower-flow-left-to-right-stopped-static.svg"), "r", encoding="utf-8") as fp:
    c_l2r = fp.read()

c_l2r_sb = c_l2r.replace('stroke="#475569" stroke-width="3" stroke-dasharray="3 3"', 'stroke="#f59e0b" stroke-width="3" stroke-dasharray="3 3"')
c_l2r_sb = c_l2r_sb.replace('stroke="#38bdf8" stroke-width="2"', 'stroke="#f59e0b" stroke-width="2"')
with open(os.path.join(inst_dir, "aeration-blower-flow-left-to-right-standby-static.svg"), "w", encoding="utf-8") as fp:
    fp.write(c_l2r_sb)
print("Created: aeration-blower-flow-left-to-right-standby-static.svg")

# Right-to-Left Standby
with open(os.path.join(inst_dir, "aeration-blower-flow-right-to-left-stopped-static.svg"), "r", encoding="utf-8") as fp:
    c_r2l = fp.read()

c_r2l_sb = c_r2l.replace('stroke="#475569" stroke-width="3" stroke-dasharray="3 3"', 'stroke="#f59e0b" stroke-width="3" stroke-dasharray="3 3"')
c_r2l_sb = c_r2l_sb.replace('stroke="#38bdf8" stroke-width="2"', 'stroke="#f59e0b" stroke-width="2"')
with open(os.path.join(inst_dir, "aeration-blower-flow-right-to-left-standby-static.svg"), "w", encoding="utf-8") as fp:
    fp.write(c_r2l_sb)
print("Created: aeration-blower-flow-right-to-left-standby-static.svg")

# Standard Standby
with open(os.path.join(inst_dir, "aeration-blower-stopped-static.svg"), "r", encoding="utf-8") as fp:
    c_std = fp.read()

c_std_sb = c_std.replace('stroke="#475569" stroke-width="3" stroke-dasharray="3 3"', 'stroke="#f59e0b" stroke-width="3" stroke-dasharray="3 3"')
c_std_sb = c_std_sb.replace('stroke="#475569" stroke-width="2"/>\n  </g>', 'stroke="#f59e0b" stroke-width="2"/>\n  </g>')
with open(os.path.join(inst_dir, "aeration-blower-standby-static.svg"), "w", encoding="utf-8") as fp:
    fp.write(c_std_sb)
print("Created: aeration-blower-standby-static.svg")


# 2. Clean unused defs from the 6 instrument files
def clean_defs(file_name, new_defs):
    fpath = os.path.join(inst_dir, file_name)
    with open(fpath, "r", encoding="utf-8") as fp:
        c = fp.read()
    
    start_defs = c.find("<defs>")
    end_defs = c.find("</defs>")
    if start_defs != -1 and end_defs != -1:
        c_clean = c[:start_defs] + new_defs + c[end_defs + len("</defs>"):]
        with open(fpath, "w", encoding="utf-8") as fp:
            fp.write(c_clean)
        print(f"Cleaned defs in {file_name}")

defs_flow_anim = """<defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#0b2545" flood-opacity="0.18" />
    </filter>
    <style>
      @keyframes fit-glow { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
      .anim-fit { animation: fit-glow 1.5s ease-in-out infinite; }
    </style>
  </defs>"""

defs_flow_static = """<defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#0b2545" flood-opacity="0.18" />
    </filter>
  </defs>"""

defs_pg_anim = """<defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#0b2545" flood-opacity="0.18" />
    </filter>
    <style>
      @keyframes pg-pulse { 0%, 100% { transform: rotate(-15deg); } 50% { transform: rotate(15deg); } }
      .anim-needle { animation: pg-pulse 2s ease-in-out infinite; }
    </style>
  </defs>"""

defs_pg_static = """<defs>
    <filter id="bottomShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.32" />
    </filter>
    <filter id="softShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#0b2545" flood-opacity="0.18" />
    </filter>
  </defs>"""

clean_defs("flow-meter-vertical-active-animated.svg", defs_flow_anim)
clean_defs("flow-meter-vertical-static.svg", defs_flow_static)
clean_defs("pressure-gauge-side-mount-left-active-animated.svg", defs_pg_anim)
clean_defs("pressure-gauge-side-mount-left-static.svg", defs_pg_static)
clean_defs("pressure-gauge-side-mount-right-active-animated.svg", defs_pg_anim)
clean_defs("pressure-gauge-side-mount-right-static.svg", defs_pg_static)

print("\nSuccessfully updated all instruments & blowers!")
