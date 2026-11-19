import os

inst_dir = os.path.join("public", "schematic-assets", "instruments-utilities")
files = sorted(os.listdir(inst_dir))
print(f"Total instruments/utilities files: {len(files)}\n")

for f in files:
    fpath = os.path.join(inst_dir, f)
    with open(fpath, "r", encoding="utf-8") as fp:
        c = fp.read()
    
    # check for embedded pipe runs extending to canvas borders (0 or 200, or through pipe)
    has_edge_pipe = any(k in c for k in ["M 0 100", "L 200 100", "M 100 0", "L 100 200", "Through Pipe", "ssPipeGradH", "ssPipeGradV", "anim-v-dash"])
    
    print(f"{f:55} | Length: {len(c):5} | Has Embedded Pipe: {has_edge_pipe}")
