import os

tanks_dir = os.path.join("public", "schematic-assets", "tanks")
for f in sorted(os.listdir(tanks_dir)):
    if f.endswith("-fluid-animated.svg"):
        p = os.path.join(tanks_dir, f)
        with open(p, "r", encoding="utf-8") as fp:
            c = fp.read()
        vb = c[c.find('viewBox="')+9:c.find('"', c.find('viewBox="')+9)]
        print(f"{f:40} | viewBox: {vb}")
