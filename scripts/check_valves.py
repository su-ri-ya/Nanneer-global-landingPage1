import os

valves_dir = os.path.join("public", "schematic-assets", "valves")
for f in sorted(os.listdir(valves_dir)):
    with open(os.path.join(valves_dir, f), "r") as fp:
        c = fp.read()
    has_pipe = ("Through Pipe" in c) or ("ssPipeGrad" in c) or ("width=\"150\" height=\"24\"" in c) or ("d=\"M 0 100" in c) or ("d=\"M 100 0" in c)
    print(f"{f}: {'[HAS EMBEDDED PIPE]' if has_pipe else '[STANDALONE VALVE]'}")
