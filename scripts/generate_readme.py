import os
import glob

BASE_DIR = 'public/schematic-assets'
README_PATH = os.path.join(BASE_DIR, 'README.md')

def update_readme_full():
    all_svgs = glob.glob(os.path.join(BASE_DIR, '**', '*.svg'), recursive=True)
    total = len(all_svgs)

    content = f"""# Nanneer SCADA Schematic Asset Library

The complete, unified library of **{total} pure engineering SVG vector graphics** neatly organized into 6 dedicated categories under [`public/schematic-assets/`](./):

```
public/schematic-assets/
├── tanks/                  # 33 SVGs: Storage, Aeration, Clarifiers, Sludge, Feed, Treated, Soft, Mixers, Pond (with 3D bottom shadows)
├── filters/                # 30 SVGs: PSF, ACF, Softener, MGF, Micron, RO Skid, UF Skid, Press, Lamella, DAF (with 3D bottom shadows)
├── pumps/                  # 56 SVGs: Centrifugal (DN25/50/100, L2R/R2L), RO Multistage (L2R/R2L), Dosing, Submersible
├── pipes/                  # 794 SVGs: Complete Shape & Color Matrix across 7 Process Fluid Lines + Dry Unfilled Lines
│   ├── water/              # 88 SVGs: Process / Treated Potable Water (Cerulean Blue #0284c7)
│   ├── sewage/             # 88 SVGs: Raw Influent / Wastewater (Sewage Brown #8d6e63)
│   ├── air/                # 88 SVGs: Aeration Blower / Compressed Air (Pneumatic Amber #d97706)
│   ├── sludge/             # 88 SVGs: Sludge / RAS / WAS Return (Sludge Red #dc2626)
│   ├── chemical/           # 88 SVGs: Chemical Dosing Hypo/Alum/PAC (Emerald Green #16a34a)
│   ├── permeate/           # 88 SVGs: RO Permeate Pure Water (Electric Cyan #06b6d4)
│   ├── brine/              # 88 SVGs: RO Reject / Concentrated Drain (Deep Orange #ea580c)
│   └── dry/                # 44 SVGs: Unfilled Stainless Steel 316 Metallic Casing Lines
├── valves/                 # 22 SVGs: Solenoid (Horiz/Vert), Multiport (Filter/Backwash/Rinse), NRV Check (L2R/R2L/Vert), Manual (Horiz/Vert)
└── instruments-utilities/  # 33 SVGs: Aeration Blowers, Cooling Tower, UV System, FIT (Horiz/Vert), LIT, PG (Top/Side Mount), Tanker, Building
```

---

## 🌟 3D Depth & Visual Realism Standards
- **3D Grounding Bottom Contact Shadows**: Every major tank, filter vessel, pump footing, and utility node includes soft contact drop shadows (`<feDropShadow dx="0" dy="6" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.32" />`) and grounding pedestal ellipses anchoring them to the canvas.
- **2.5D Cylindrical Specular Sheen**: Metallic and glass vessel bodies feature realistic cylindrical curvature highlights (`#specularSheen`).
- **3D Pipeline Drop Shadows**: All pipes cast realistic elevation shadows (`dx="0" dy="2.5" stdDeviation="2.5"`).
- **100% Pure Engineering Graphics**: Zero text, zero numbers, and zero telemetry badges.
- **Flush Boundary Snapping**: Every pipe, pump suction/discharge, and valve port flushes edge-to-edge at canvas boundaries.

---

## 🎨 Process Fluid Color Coding Matrix

| Process Line | Color Name | Fluid Core (4px) | Animated Pulse (2.5px) | Directory |
| :--- | :--- | :---: | :---: | :--- |
| **Process / Treated Water** | Cerulean Blue | `#0284C7` | `#BAE6FD` | [`pipes/water/`](./pipes/water/) |
| **Raw Sewage / Influent** | Sewage Brown | `#8D6E63` | `#D7CCC8` | [`pipes/sewage/`](./pipes/sewage/) |
| **Aeration / Compressed Air** | Pneumatic Amber | `#D97706` | `#FDE68A` | [`pipes/air/`](./pipes/air/) |
| **Sludge / RAS / WAS** | Sludge Red | `#DC2626` | `#FCA5A5` | [`pipes/sludge/`](./pipes/sludge/) |
| **Chemical Dosing** | Emerald Green | `#16A34A` | `#BBF7D0` | [`pipes/chemical/`](./pipes/chemical/) |
| **RO Permeate (Pure Water)** | Electric Cyan | `#06B6D4` | `#67E8F9` | [`pipes/permeate/`](./pipes/permeate/) |
| **RO Reject / Brine Drain** | Deep Orange | `#EA580C` | `#FED7AA` | [`pipes/brine/`](./pipes/brine/) |
| **Dry / Empty Line** | Stainless Steel 316 | *(none)* | *(none)* | [`pipes/dry/`](./pipes/dry/) |

---

## 📐 Complete Pipeline Shape Matrix (44 Shapes per Color)

Each process fluid directory contains the full set of **44 shapes** in both `fluid-animated` (`stroke-dasharray: 5 7;` cycle 0.8s) and `fluid-static` states:

### 1. Elevated Step-Down Drop-In & Riser Step-Up Tees
- `pipe-elevated-step-down-drop-tee-left` *(Upper line turns 90° down and drops into running bottom line)*
- `pipe-elevated-step-down-drop-tee-right` *(Mirror upper drop tee)*
- `pipe-bottom-riser-step-up-tee-left` *(Bottom line rises 90° up to inject into running upper line)*
- `pipe-bottom-riser-step-up-tee-right` *(Mirror bottom riser tee)*

### 2. 3D Non-Intersecting Perpendicular Crossovers
- `pipe-3d-perpendicular-crossing` *(Horizontal line crossing over vertical line with 3D elevation contact shadow)*

### 3. Dual Pump & Blower Manifolds
- `pipe-manifold-dual-pump-suction-splitter` *(1 top inlet splits into 2 parallel pump suction drops)*
- `pipe-manifold-dual-pump-discharge-combiner` *(2 bottom pump discharges combine into 1 top outlet)*
- `pipe-manifold-dual-blower-interconnect` *(Connects 2 horizontal blowers into a center discharge)*

### 4. Dual Parallel Bypass Loops
- `pipe-dual-bypass-loop-left-to-right` *(Flow splits into upper & lower branches around obstacles, then rejoins)*
- `pipe-dual-bypass-loop-right-to-left` *(Reverse split loop)*

### 5. Multi-Tap Distribution Headers
- `pipe-header-dual-tap-drop` *(Horizontal main with 2 downward feeder taps)*
- `pipe-header-triple-tap-drop` *(Horizontal main with 3 downward feeder taps)*

### 6. 45° Lateral Wye Low-Loss Junctions
- `pipe-wye-45-branch-up-left-to-right` *(Straight run with 45° low-loss branch up)*
- `pipe-wye-45-branch-down-left-to-right` *(Straight run with 45° low-loss branch down)*
- `pipe-wye-45-symmetric-flow-join` *(Two 45° incoming streams merging into 1 straight exit)*

### 7. Trench & Overhead Elevation Loops
- `pipe-floor-trench-u-run` *(Drops to floor trench, travels across bays, rises into next vessel)*
- `pipe-overhead-gantry-run` *(Rises to overhead rack, crosses over, drops to consumer)*
- `pipe-inverted-u-bend` *(Siphon break / overhead loop)*
- `pipe-u-trap` *(P-Trap / seal loop)*

### 8. Crossovers & Jogs
- `pipe-bridge-over-left-to-right` *(Hops up over crossing pipes)*
- `pipe-bridge-under-left-to-right` *(Dips down under crossing pipes)*
- `pipe-jog-step-up-left-to-right` *(Horizontal offset stepping up 80px)*
- `pipe-jog-step-down-left-to-right` *(Horizontal offset stepping down 80px)*
- `pipe-jog-drop-run-right-drop` & `pipe-jog-drop-run-left-drop` *(Z-jog 3-segment vertical step drop to vessel inlet)*
- `pipe-jog-rise-run-right-rise` & `pipe-jog-rise-run-left-rise` *(Z-jog 3-segment vertical step riser to vessel)*
- `pipe-elevated-step-down-drop-tee-left` & `pipe-elevated-step-down-drop-tee-right` *(High-run step-down drop into horizontal pipe)*
- `pipe-bottom-riser-step-up-tee-left` & `pipe-bottom-riser-step-up-tee-right` *(Low-run step-up riser teeing into horizontal pipe)*
- `pipe-overhead-gantry-multi-turn-return` *(High-elevation multi-turn recirculation return line back into tank)*
- `pipe-nozzle-stub-spool-horizontal` *(Half-length spool stub connecting valves directly to vessel nozzles)*
- `pipe-3d-perpendicular-crossing` *(Non-intersecting perpendicular 3D pipe crossing with depth contact shadow)*
- `pipe-bypass-upper-half-left-to-right` & `pipe-bypass-upper-half-right-to-left` *(Upper duty bypass loop around M1/filter bank)*
- `pipe-bypass-lower-half-left-to-right` & `pipe-bypass-lower-half-right-to-left` *(Lower standby bypass loop around M2/filter bank)*

### 9. Straights & 90° Directional Elbows
- Straights: Horizontal (L→R, R→L), Vertical (T→B, B→T)
- 90° Elbows: All 8 permutations (L2U, U2L, L2D, D2L, R2U, U2R, R2D, D2R)

### 10. Branching Tees & Cross
- `pipe-tee-branch-up`, `...-down`, `...-left`, `...-right`
- `pipe-cross-4way` *(Symmetrical 4-port distribution manifold)*

### 11. End Caps & Concentric Reducers
- `pipe-end-cap-horizontal-left` & `pipe-end-cap-horizontal-right` *(Flanged blind caps)*
- `pipe-reducer-concentric-large-to-small` *(DN100 to DN50/DN25 reducer)*
- `pipe-reducer-concentric-small-to-large` *(DN25/DN50 to DN100 expander)*
"""

    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"README.md successfully updated with full catalog of all {total} assets!")

if __name__ == '__main__':
    update_readme_full()
