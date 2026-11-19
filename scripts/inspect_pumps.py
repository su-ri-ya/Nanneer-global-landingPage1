import os

pumps_dir = os.path.join("public", "schematic-assets", "pumps")
files = sorted(os.listdir(pumps_dir))
print(f"Total pump files: {len(files)}\n")

for f in files:
    with open(os.path.join(pumps_dir, f), "r", encoding="utf-8") as fp:
        c = fp.read()
    
    # check for pipe mentions or pipes extending to edge
    has_edge_pipe = any(k in c for k in ["M 0 ", "M 200 ", "L 0 ", "L 200 ", "Through Pipe", "ssPipeGrad", "anim-dash", "anim-v-dash"])
    # check state
    state = "unknown"
    if "running" in f or "active" in f or "animated" in f:
        state = "RUNNING / ACTIVE"
    elif "standby" in f or "idle" in f:
        state = "STANDBY / IDLE"
    elif "fault" in f or "tripped" in f or "off" in f or "closed" in f:
        state = "FAULT / OFF"
    elif "static" in f:
        state = "STATIC (OFF/READY)"

    print(f"{f:55} | State: {state:18} | Has Edge Pipe/Nozzle: {has_edge_pipe}")
