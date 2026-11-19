"""
Universal Multi-Plant SCADA Schematic Asset Generator for Nanneer Consultancy.
Covers ALL plants in the backend: STP, ETP, WTP, RO/UF, HVAC Cooling Towers, and Pumps.
STRICT USER RULE: Pure graphic elements only — ZERO text, ZERO numbers, ZERO telemetry values.
Includes both:
  - With Fluid / Active / Clamped
  - Without Fluid / Dry / Empty / Open
Exports both standalone SVG and high-resolution transparent PNG.
"""

import os
import shutil
import subprocess

SVG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public", "schematic-assets", "svg"))
PNG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "public", "schematic-assets", "png"))

if os.path.exists(SVG_DIR):
    shutil.rmtree(SVG_DIR)
if os.path.exists(PNG_DIR):
    shutil.rmtree(PNG_DIR)
os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

# Comprehensive SCADA Defs with Gradients for All Plants (STP, ETP, WTP, RO, Cooling)
SCADA_DEFS = """
  <defs>
    <!-- 1. Fluid Gradients -->
    <!-- Raw Sewage / Murky Effluent (STP / ETP) -->
    <linearGradient id="rawSewageGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#A1887F" stop-opacity="0.88" />
      <stop offset="45%" stop-color="#8D6E63" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#5D4037" stop-opacity="0.96" />
    </linearGradient>

    <!-- Chemical / Toxic Industrial Effluent (ETP Flash Mixer) -->
    <linearGradient id="chemicalEffluentGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#CA8A04" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#A16207" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#713F12" stop-opacity="0.98" />
    </linearGradient>

    <!-- Flocculation Water with Floc Particles -->
    <linearGradient id="flocculationGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#D97706" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#B45309" stop-opacity="0.9" />
      <stop offset="100%" stop-color="#78350F" stop-opacity="0.95" />
    </linearGradient>

    <!-- MBBR Aeration Fluid -->
    <linearGradient id="mbbrWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#9E8D72" stop-opacity="0.85" />
      <stop offset="45%" stop-color="#6B7852" stop-opacity="0.90" />
      <stop offset="100%" stop-color="#4A5636" stop-opacity="0.95" />
    </linearGradient>

    <!-- Clarifier Dual Phase Fluid -->
    <linearGradient id="clarifierWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#BAE6FD" stop-opacity="0.85" />
      <stop offset="40%" stop-color="#93C5FD" stop-opacity="0.82" />
      <stop offset="68%" stop-color="#8D6E63" stop-opacity="0.88" />
      <stop offset="100%" stop-color="#4E342E" stop-opacity="0.96" />
    </linearGradient>

    <!-- Sludge Blanket / Cake -->
    <linearGradient id="sludgeWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#5D4037" stop-opacity="0.95" />
      <stop offset="50%" stop-color="#3E2723" stop-opacity="0.97" />
      <stop offset="100%" stop-color="#211109" stop-opacity="0.99" />
    </linearGradient>

    <!-- Filter Feed / Secondary Effluent -->
    <linearGradient id="filterFeedGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E0F2FE" stop-opacity="0.85" />
      <stop offset="50%" stop-color="#7DD3FC" stop-opacity="0.88" />
      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.92" />
    </linearGradient>

    <!-- Potable / Treated Clean Water (WTP / STP) -->
    <linearGradient id="treatedWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E0F2FE" stop-opacity="0.95" />
      <stop offset="45%" stop-color="#38BDF8" stop-opacity="0.92" />
      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.95" />
    </linearGradient>

    <!-- High-Purity Soft Water / RO Permeate -->
    <linearGradient id="softWaterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F0F9FF" stop-opacity="0.98" />
      <stop offset="45%" stop-color="#38BDF8" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#0369A1" stop-opacity="0.98" />
    </linearGradient>

    <!-- RO Reject / Brine Concentrated Stream -->
    <linearGradient id="roBrineGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FED7AA" stop-opacity="0.9" />
      <stop offset="50%" stop-color="#FB923C" stop-opacity="0.95" />
      <stop offset="100%" stop-color="#EA580C" stop-opacity="0.98" />
    </linearGradient>

    <!-- DAF Microbubble Cloud (White Water) -->
    <linearGradient id="dafBubbleGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9" />
      <stop offset="60%" stop-color="#E0F2FE" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.8" />
    </linearGradient>

    <!-- 2. Structural & Engineering Materials -->
    <!-- 2.5D Glass Cylinder Wall -->
    <linearGradient id="glassCylinderGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.5" />
      <stop offset="8%" stop-color="#FFFFFF" stop-opacity="0.85" />
      <stop offset="22%" stop-color="#F8FAFC" stop-opacity="0.3" />
      <stop offset="70%" stop-color="#E0F2FE" stop-opacity="0.2" />
      <stop offset="92%" stop-color="#38BDF8" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.5" />
    </linearGradient>

    <!-- Top Glass Rim Flange -->
    <linearGradient id="glassRimGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#94A3B8" stop-opacity="0.8" />
      <stop offset="25%" stop-color="#FFFFFF" stop-opacity="0.95" />
      <stop offset="70%" stop-color="#E2E8F0" stop-opacity="0.7" />
      <stop offset="100%" stop-color="#64748B" stop-opacity="0.9" />
    </linearGradient>

    <!-- Specular Highlight -->
    <linearGradient id="specularSheen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.35" />
      <stop offset="30%" stop-color="#FFFFFF" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0" />
    </linearGradient>

    <!-- Pressure Vessel FRP Shell -->
    <linearGradient id="filterVesselGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0369A1" />
      <stop offset="25%" stop-color="#38BDF8" />
      <stop offset="50%" stop-color="#0284C7" />
      <stop offset="85%" stop-color="#0369A1" />
      <stop offset="100%" stop-color="#075985" />
    </linearGradient>

    <!-- Stainless Steel 316 / Metallic Parts -->
    <linearGradient id="ss316GradH" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="20%" stop-color="#94A3B8" />
      <stop offset="45%" stop-color="#FFFFFF" />
      <stop offset="70%" stop-color="#CBD5E1" />
      <stop offset="100%" stop-color="#334155" />
    </linearGradient>

    <linearGradient id="ss316GradV" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#475569" />
      <stop offset="25%" stop-color="#FFFFFF" />
      <stop offset="60%" stop-color="#CBD5E1" />
      <stop offset="100%" stop-color="#334155" />
    </linearGradient>

    <!-- Sand Media Layers (PSF & MGF) -->
    <linearGradient id="sandMediaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FDE68A" stop-opacity="0.95" />
      <stop offset="45%" stop-color="#D97706" stop-opacity="0.95" />
      <stop offset="75%" stop-color="#78350F" stop-opacity="0.98" />
      <stop offset="100%" stop-color="#451A03" stop-opacity="0.98" />
    </linearGradient>

    <!-- Multi-Grade Filter 4 Layers (Anthracite, Sand, Garnet, Gravel) -->
    <linearGradient id="mgfAnthraciteGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#334155" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>

    <!-- Carbon Media Layer (ACF) -->
    <linearGradient id="carbonMediaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#475569" stop-opacity="0.95" />
      <stop offset="50%" stop-color="#1E293B" stop-opacity="0.98" />
      <stop offset="100%" stop-color="#0F172A" stop-opacity="0.99" />
    </linearGradient>

    <!-- Resin Media Layer (Softener) -->
    <linearGradient id="resinMediaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FBBF24" stop-opacity="0.95" />
      <stop offset="60%" stop-color="#D97706" stop-opacity="0.98" />
      <stop offset="100%" stop-color="#92400E" stop-opacity="0.99" />
    </linearGradient>

    <!-- Metallic Ring -->
    <linearGradient id="metalRingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#E2E8F0" />
      <stop offset="80%" stop-color="#CBD5E1" />
      <stop offset="100%" stop-color="#94A3B8" />
    </linearGradient>

    <!-- Soft Drop Shadow -->
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0B2545" flood-opacity="0.12" />
    </filter>
  </defs>
"""

def wrap_svg(inner_content, viewbox="0 0 200 120", width=400, height=240):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" width="{width}" height="{height}" fill="none">
{SCADA_DEFS}
  <g filter="url(#softShadow)">
{inner_content}
  </g>
</svg>"""

# =========================================================================
# A. PUMPS (WITH FLUID VS. WITHOUT FLUID)
# =========================================================================

# 1. Centrifugal Pump
def get_centrifugal_pump(has_fluid=True):
    color = "#0284C7" if has_fluid else "#64748B"
    fill = "#BAE6FD" if has_fluid else "#E2E8F0"
    fluid_stream = ""
    if has_fluid:
        fluid_stream = """
          <!-- Pressurized Fluid Stream Through Volute & Discharge -->
          <circle cx="0" cy="0" r="11" fill="url(#treatedWaterGrad)" />
          <polygon points="18,-4 25,0 18,4" fill="#0284C7" />
          <line x1="-18" y1="0" x2="-14" y2="0" stroke="#0284C7" stroke-width="3" stroke-linecap="round" />
          <line x1="14" y1="0" x2="22" y2="0" stroke="#0284C7" stroke-width="3" stroke-linecap="round" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <circle cx="0" cy="0" r="18" fill="url(#metalRingGrad)" stroke="#94A3B8" stroke-width="1.5" />
        <circle cx="0" cy="0" r="14" fill="{fill}" stroke="{color}" stroke-width="2" />
        {fluid_stream}
        <!-- 4-Blade Impeller -->
        <circle cx="0" cy="0" r="4.0" fill="{color}" />
        <line x1="-9" y1="0" x2="9" y2="0" stroke="{color}" stroke-width="2.2" stroke-linecap="round" />
        <line x1="0" y1="-9" x2="0" y2="9" stroke="{color}" stroke-width="2.2" stroke-linecap="round" />
        <line x1="-6.5" y1="-6.5" x2="6.5" y2="6.5" stroke="{color}" stroke-width="1.2" stroke-linecap="round" opacity="0.45" />
        <line x1="-6.5" y1="6.5" x2="6.5" y2="-6.5" stroke="{color}" stroke-width="1.2" stroke-linecap="round" opacity="0.45" />
        <circle cx="11.5" cy="-11.5" r="3.5" fill="{color}" stroke="#FFFFFF" stroke-width="1.0" />
      </g>
    """

# 2. Vertical Multistage High-Pressure Pump (RO Feed Pump)
def get_multistage_ro_pump(has_fluid=True):
    fluid_block = ""
    if has_fluid:
        fluid_block = """
          <!-- High-Pressure Flowing Water Inside Chamber -->
          <rect x="18" y="44" width="24" height="48" rx="2" fill="url(#softWaterGrad)" opacity="0.9" />
          <polygon points="46,80 54,80 50,72" fill="#0284C7" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <!-- Top Electric Motor Housing -->
        <rect x="12" y="2" width="36" height="34" rx="4" fill="#0284C7" stroke="#0B2545" stroke-width="1.8" />
        <line x1="20" y1="2" x2="20" y2="36" stroke="#0369A1" stroke-width="1.2" />
        <line x1="28" y1="2" x2="28" y2="36" stroke="#0369A1" stroke-width="1.2" />
        <line x1="36" y1="2" x2="36" y2="36" stroke="#0369A1" stroke-width="1.2" />
        <rect x="18" y="36" width="24" height="8" fill="#1E293B" stroke="#0F172A" stroke-width="1.5" />
        <!-- Vertical Stainless Steel Multistage Stack -->
        <rect x="16" y="44" width="28" height="50" rx="3" fill="url(#ss316GradH)" stroke="#334155" stroke-width="2" />
        {fluid_block}
        <!-- Stage Stage Rings -->
        <line x1="16" y1="56" x2="44" y2="56" stroke="#64748B" stroke-width="1.5" />
        <line x1="16" y1="68" x2="44" y2="68" stroke="#64748B" stroke-width="1.5" />
        <line x1="16" y1="80" x2="44" y2="80" stroke="#64748B" stroke-width="1.5" />
        <!-- Suction & High-Pressure Discharge Nozzles -->
        <rect x="4" y="80" width="12" height="10" rx="2" fill="url(#ss316GradH)" stroke="#1E293B" stroke-width="1.2" />
        <rect x="44" y="80" width="12" height="10" rx="2" fill="url(#ss316GradH)" stroke="#1E293B" stroke-width="1.2" />
        <!-- Base Skids -->
        <rect x="10" y="94" width="40" height="8" rx="2" fill="#1E293B" />
      </g>
    """

# 3. Submersible Sump / Sewage Cutter Pump
def get_submersible_sump_pump(has_fluid=True):
    water_pit = ""
    if has_fluid:
        water_pit = """
          <!-- Submerged in Wastewater Pit -->
          <rect x="2" y="30" width="56" height="58" rx="2" fill="url(#rawSewageGrad)" opacity="0.6" />
          <ellipse cx="30" cy="30" rx="28" ry="4" fill="#8D6E63" opacity="0.8" />
        """
    return f"""
      <g transform="translate(0, 0)">
        {water_pit}
        <!-- Lifting Handle on Top -->
        <path d="M22 12 Q30 4 38 12" fill="none" stroke="#64748B" stroke-width="2.5" stroke-linecap="round" />
        <!-- Motor Casing -->
        <rect x="18" y="12" width="24" height="40" rx="4" fill="url(#ss316GradH)" stroke="#1E293B" stroke-width="2" />
        <!-- Volute Bottom Base with Suction Strainer -->
        <path d="M12 52 L48 52 L44 76 L16 76 Z" fill="#334155" stroke="#0F172A" stroke-width="2" />
        <!-- Suction Slots -->
        <line x1="20" y1="68" x2="20" y2="74" stroke="#94A3B8" stroke-width="1.2" />
        <line x1="26" y1="68" x2="26" y2="74" stroke="#94A3B8" stroke-width="1.2" />
        <line x1="34" y1="68" x2="34" y2="74" stroke="#94A3B8" stroke-width="1.2" />
        <line x1="40" y1="68" x2="40" y2="74" stroke="#94A3B8" stroke-width="1.2" />
        <!-- Side Discharge Elbow Pointing Up -->
        <path d="M44 60 L54 60 L54 42" fill="none" stroke="#1E293B" stroke-width="4" stroke-linecap="round" />
      </g>
    """

# 4. Chemical Dosing Pump
def get_chemical_dosing_pump(has_fluid=True):
    fluid_color = "#D97706" if has_fluid else "#CBD5E1"
    fluid_opacity = "0.9" if has_fluid else "0.3"
    return f"""
      <g transform="translate(0, 0)">
        <polygon points="20,0 40,11 40,34 20,45 0,34 0,11" fill="#DCFCE7" stroke="#16A34A" stroke-width="2.5" />
        <circle cx="20" cy="22.5" r="8" fill="{fluid_color}" opacity="{fluid_opacity}" />
        <line x1="20" y1="45" x2="20" y2="65" stroke="#16A34A" stroke-width="2.5" />
        <polygon points="16,65 20,72 24,65" fill="{fluid_color}" />
      </g>
    """

# =========================================================================
# B. WTP (WATER TREATMENT PLANT & INFLOW)
# =========================================================================

# 5. Water Tanker Supply Station (tankerSupply)
def get_water_tanker_supply(has_fluid=True):
    hose_fluid = ""
    if has_fluid:
        hose_fluid = """
          <!-- Flexible Unloading Hose with Water Stream into Sump -->
          <path d="M78 45 C78 65, 88 75, 92 88" fill="none" stroke="#0284C7" stroke-width="5" stroke-linecap="round" />
          <ellipse cx="94" cy="88" rx="8" ry="3" fill="#38BDF8" opacity="0.8" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <!-- Tanker Truck Cab -->
        <path d="M12 35 L26 35 L34 45 L34 72 L12 72 Z" fill="#0284C7" stroke="#0B2545" stroke-width="2" />
        <rect x="22" y="38" width="10" height="12" rx="2" fill="#E0F2FE" stroke="#0284C7" stroke-width="1" />
        <!-- Wheels -->
        <circle cx="20" cy="74" r="7" fill="#1E293B" stroke="#0F172A" stroke-width="2" />
        <circle cx="54" cy="74" r="7" fill="#1E293B" stroke="#0F172A" stroke-width="2" />
        <circle cx="70" cy="74" r="7" fill="#1E293B" stroke="#0F172A" stroke-width="2" />
        <!-- Cylindrical Water Tanker Barrel -->
        <rect x="34" y="24" width="46" height="42" rx="14" fill="url(#ss316GradH)" stroke="#334155" stroke-width="2" />
        <ellipse cx="78" cy="45" rx="4" ry="16" fill="url(#ss316GradV)" stroke="#1E293B" stroke-width="1.5" />
        <!-- Top Manhole & Access Ladder -->
        <rect x="52" y="18" width="12" height="6" rx="2" fill="#475569" stroke="#1E293B" stroke-width="1" />
        <!-- Discharge Valve on Rear -->
        <rect x="76" y="42" width="6" height="8" rx="1" fill="#D97706" />
        {hose_fluid}
      </g>
    """

# 6. Rainwater Harvesting Pond / Raw Water Basin (pond)
def get_rainwater_pond(has_fluid=True):
    water_layer = ""
    if has_fluid:
        water_layer = """
          <!-- Open Water Pond Fluid with Surface Ripples -->
          <path d="M10 22 C28 14, 72 14, 90 22 C104 30, 104 55, 90 64 C72 72, 28 72, 10 64 C-4 55, -4 30, 10 22 Z" fill="url(#treatedWaterGrad)" stroke="#38BDF8" stroke-width="2" />
          <ellipse cx="50" cy="38" rx="28" ry="8" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.6" />
          <ellipse cx="50" cy="48" rx="18" ry="5" fill="none" stroke="#FFFFFF" stroke-width="1" opacity="0.5" />
        """
    else:
        water_layer = """
          <!-- Dry Excavated Pond Basin with Geotextile Liner -->
          <path d="M10 22 C28 14, 72 14, 90 22 C104 30, 104 55, 90 64 C72 72, 28 72, 10 64 C-4 55, -4 30, 10 22 Z" fill="#E2E8F0" stroke="#94A3B8" stroke-width="2" stroke-dasharray="4 3" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <!-- Natural Basin Bank Embankment -->
        <path d="M4 18 C26 8, 74 8, 96 18 C112 28, 112 58, 96 68 C74 78, 26 78, 4 68 C-12 58, -12 28, 4 18 Z" fill="#64748B" opacity="0.3" />
        {water_layer}
      </g>
    """

# 7. Multi-Grade Filter - MGF (mgf)
def get_multi_grade_filter_mgf(is_filled=True):
    media = ""
    if is_filled:
        media = """
          <!-- MGF 4 Graded Media Layers Cutaway -->
          <g transform="translate(9, 32)">
            <rect x="0" y="0" width="64" height="62" rx="4" fill="#0F172A" stroke="#7DD3FC" stroke-width="1.2" />
            <!-- Layer 1: Coarse Anthracite Coal -->
            <rect x="2" y="2" width="60" height="15" fill="url(#mgfAnthraciteGrad)" />
            <!-- Layer 2: Fine Silica Sand -->
            <rect x="2" y="17" width="60" height="16" fill="url(#sandMediaGrad)" />
            <!-- Layer 3: Garnet / Heavy Mineral -->
            <rect x="2" y="33" width="60" height="14" fill="#B45309" />
            <!-- Layer 4: Underdrain Pebble Gravel -->
            <rect x="2" y="47" width="60" height="13" rx="2" fill="#451A03" />
            <!-- Lateral collector arms -->
            <line x1="10" y1="54" x2="54" y2="54" stroke="#CBD5E1" stroke-width="2" stroke-linecap="round" />
            <rect x="2" y="2" width="18" height="58" rx="2" fill="url(#specularSheen)" opacity="0.4" />
          </g>
        """
    else:
        media = """
          <!-- Empty MGF Vessel Cutaway Window -->
          <g transform="translate(9, 32)">
            <rect x="0" y="0" width="64" height="62" rx="4" fill="#0B2545" stroke="#7DD3FC" stroke-width="1.2" />
            <rect x="2" y="2" width="60" height="58" rx="2" fill="#1E293B" opacity="0.7" />
            <line x1="10" y1="54" x2="54" y2="54" stroke="#CBD5E1" stroke-width="2" stroke-linecap="round" />
          </g>
        """
    return f"""
      <g transform="translate(0, 0)">
        <ellipse cx="41" cy="122" rx="36" ry="6" fill="#0B2545" opacity="0.18" />
        <!-- FRP Vessel Shell -->
        <path d="M 1 20 C 1 2, 81 2, 81 20 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
        <rect x="1" y="20" width="80" height="84" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
        <path d="M 1 104 C 1 122, 81 122, 81 104 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
        <line x1="1" y1="30" x2="81" y2="30" stroke="#38BDF8" stroke-width="1.2" stroke-dasharray="3 2" opacity="0.8" />
        <line x1="1" y1="96" x2="81" y2="96" stroke="#38BDF8" stroke-width="1.2" stroke-dasharray="3 2" opacity="0.8" />
        {media}
        <rect x="5" y="8" width="10" height="104" rx="2" fill="url(#specularSheen)" opacity="0.55" />
      </g>
    """

# =========================================================================
# C. ETP (EFFLUENT TREATMENT PLANT)
# =========================================================================

# 8. Flash Mixer / Coagulation Tank (Chemical Vortex Mixer)
def get_etp_flash_mixer(has_fluid=True):
    fluid = ""
    if has_fluid:
        fluid = """
          <!-- Chemical Reaction Fluid with Vortex Depression -->
          <path d="M2 32 Q45 42 88 32 L88 88 Q45 98 2 88 Z" fill="url(#chemicalEffluentGrad)" />
          <ellipse cx="45" cy="32" rx="43" ry="5" fill="#CA8A04" opacity="0.9" />
          <!-- High-Speed Agitator Vortex Cavity -->
          <ellipse cx="45" cy="35" rx="14" ry="3" fill="#713F12" opacity="0.7" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <ellipse cx="45" cy="98" rx="42" ry="6" fill="#0B2545" opacity="0.14" />
        <!-- Tank Body -->
        <path d="M0 88 Q45 102 90 88 L90 18 Q45 28 0 18 Z" fill="url(#glassCylinderGrad)" stroke="#0B2545" stroke-width="2" />
        {fluid}
        <!-- Top Electric Motor & Gearbox -->
        <rect x="36" y="2" width="18" height="18" rx="3" fill="#0284C7" stroke="#0B2545" stroke-width="1.5" />
        <!-- Mixer Drive Shaft -->
        <line x1="45" y1="20" x2="45" y2="78" stroke="#1E293B" stroke-width="3" />
        <!-- High-Speed Marine Propeller / Impeller -->
        <polygon points="45,74 34,70 34,78" fill="#1E293B" />
        <polygon points="45,74 56,70 56,78" fill="#1E293B" />
        <!-- Chemical Dosing Pipe Inlets on Side (Alum / Lime) -->
        <path d="M8 8 L8 28 L14 28" fill="none" stroke="#D97706" stroke-width="2.5" />
        <path d="M82 8 L82 28 L76 28" fill="none" stroke="#D97706" stroke-width="2.5" />
        <ellipse cx="45" cy="18" rx="45" ry="6" fill="url(#glassRimGrad)" stroke="#0B2545" stroke-width="1.5" />
      </g>
    """

# 9. Flocculator Tank with Slow Multi-Paddle Agitator
def get_etp_flocculator_tank(has_fluid=True):
    fluid = ""
    if has_fluid:
        fluid = """
          <!-- Flocculating Effluent Fluid -->
          <path d="M2 30 Q55 42 108 30 L108 86 Q55 98 2 86 Z" fill="url(#flocculationGrad)" />
          <ellipse cx="55" cy="30" rx="53" ry="5.5" fill="#D97706" opacity="0.9" />
          <!-- Clustered Floc Particles Floating -->
          <circle cx="28" cy="45" r="3" fill="#451A03" opacity="0.8" />
          <circle cx="48" cy="62" r="3.5" fill="#451A03" opacity="0.8" />
          <circle cx="75" cy="50" r="3.2" fill="#451A03" opacity="0.8" />
          <circle cx="88" cy="68" r="4.0" fill="#451A03" opacity="0.8" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <ellipse cx="55" cy="96" rx="52" ry="6" fill="#0B2545" opacity="0.14" />
        <!-- Wide Flocculator Tank Body -->
        <path d="M0 86 Q55 100 110 86 L110 18 Q55 30 0 18 Z" fill="url(#glassCylinderGrad)" stroke="#0B2545" stroke-width="2" />
        {fluid}
        <!-- Top Reduction Gearmotor -->
        <rect x="44" y="2" width="22" height="18" rx="3" fill="#1E293B" stroke="#0B2545" stroke-width="1.5" />
        <!-- Slow Rotating Shaft -->
        <line x1="55" y1="20" x2="55" y2="82" stroke="#334155" stroke-width="3.5" />
        <!-- Multi-Tier Paddle Blades -->
        <line x1="28" y1="45" x2="82" y2="45" stroke="#475569" stroke-width="4" stroke-linecap="round" />
        <line x1="24" y1="65" x2="86" y2="65" stroke="#475569" stroke-width="4" stroke-linecap="round" />
        <ellipse cx="55" cy="18" rx="55" ry="6.5" fill="url(#glassRimGrad)" stroke="#0B2545" stroke-width="1.5" />
      </g>
    """

# 10. Lamella Tube Settler / Clarifier
def get_etp_lamella_tube_settler(has_fluid=True):
    fluid = ""
    if has_fluid:
        fluid = """
          <!-- Settling Fluid & Clarified Water on Top -->
          <path d="M2 18 L2 48 L45 84 L88 48 L88 18 Z" fill="url(#clarifierWaterGrad)" />
          <ellipse cx="45" cy="18" rx="43" ry="5" fill="#BAE6FD" opacity="0.9" />
          <!-- Dense Sludge Apex at Bottom Cone -->
          <path d="M30 60 L45 84 L60 60 Z" fill="url(#sludgeWaterGrad)" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <!-- 60 Degree Conical Hopper Hull -->
        <path d="M0 16 L0 48 L45 86 L90 48 L90 16 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />
        {fluid}
        <!-- Inclined 60° Lamella Plate / Tube Packs in Middle Section -->
        <g stroke="#0369A1" stroke-width="2.5" opacity="0.8">
          <line x1="18" y1="28" x2="32" y2="50" />
          <line x1="28" y1="28" x2="42" y2="50" />
          <line x1="38" y1="28" x2="52" y2="50" />
          <line x1="48" y1="28" x2="62" y2="50" />
          <line x1="58" y1="28" x2="72" y2="50" />
        </g>
        <!-- V-Notch Overflow Effluent Launders on Top -->
        <path d="M6 16 L84 16" stroke="#38BDF8" stroke-width="1.8" stroke-dasharray="3 2" />
        <ellipse cx="45" cy="16" rx="45" ry="6" fill="none" stroke="#0284C7" stroke-width="1.5" />
      </g>
    """

# 11. DAF (Dissolved Air Flotation) Tank
def get_etp_daf_tank(has_fluid=True):
    fluid = ""
    if has_fluid:
        fluid = """
          <!-- Fluid Filled with Dense White-Water Microbubble Blanket -->
          <rect x="4" y="24" width="92" height="48" fill="url(#treatedWaterGrad)" />
          <rect x="4" y="24" width="92" height="30" fill="url(#dafBubbleGrad)" />
          <!-- Floating Sludge / Scum Layer on Surface -->
          <rect x="4" y="22" width="92" height="6" fill="#78350F" opacity="0.9" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <!-- Rectangular Dissolved Air Flotation Tank Body -->
        <rect x="2" y="20" width="96" height="54" rx="4" fill="url(#ss316GradH)" stroke="#1E293B" stroke-width="2" />
        {fluid}
        <!-- Top Flight Chain Surface Scraper Skimmer -->
        <circle cx="16" cy="18" r="5" fill="#475569" stroke="#0F172A" stroke-width="1" />
        <circle cx="84" cy="18" r="5" fill="#475569" stroke="#0F172A" stroke-width="1" />
        <line x1="16" y1="14" x2="84" y2="14" stroke="#334155" stroke-width="2" />
        <line x1="16" y1="22" x2="84" y2="22" stroke="#334155" stroke-width="2" />
        <!-- Bottom Microbubble Saturation Manifold Header -->
        <rect x="14" y="66" width="72" height="6" rx="2" fill="#D97706" />
        <circle cx="25" cy="62" r="1.5" fill="#FFFFFF" /><circle cx="45" cy="60" r="1.5" fill="#FFFFFF" /><circle cx="65" cy="62" r="1.5" fill="#FFFFFF" />
      </g>
    """

# 12. Plate & Frame Sludge Filter Press (Recessed Chamber)
def get_sludge_filter_press(is_clamped=True):
    cake = ""
    if is_clamped:
        cake = """
          <!-- Clamped Sludge Cake Between Plates -->
          <rect x="28" y="20" width="46" height="36" fill="#451A03" opacity="0.95" />
          <line x1="34" y1="20" x2="34" y2="56" stroke="#1C1917" stroke-width="1" />
          <line x1="42" y1="20" x2="42" y2="56" stroke="#1C1917" stroke-width="1" />
          <line x1="50" y1="20" x2="50" y2="56" stroke="#1C1917" stroke-width="1" />
          <line x1="58" y1="20" x2="58" y2="56" stroke="#1C1917" stroke-width="1" />
          <line x1="66" y1="20" x2="66" y2="56" stroke="#1C1917" stroke-width="1" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <!-- Heavy Structural Frame (Side Beams) -->
        <rect x="2" y="34" width="98" height="8" rx="2" fill="#334155" stroke="#0F172A" stroke-width="1.5" />
        <!-- Stationary Head (Left) -->
        <rect x="14" y="14" width="14" height="48" rx="2" fill="#0284C7" stroke="#0B2545" stroke-width="2" />
        <!-- Movable Follower Plate (Right) Clamped by Hydraulic Ram -->
        <rect x="74" y="14" width="12" height="48" rx="2" fill="#0284C7" stroke="#0B2545" stroke-width="2" />
        {cake}
        <!-- Hydraulic Cylinder & Piston Ram (Right) -->
        <rect x="86" y="30" width="16" height="16" rx="2" fill="#1E293B" stroke="#0B2545" stroke-width="1.5" />
        <line x1="86" y1="38" x2="74" y2="38" stroke="#CBD5E1" stroke-width="4" stroke-linecap="round" />
        <!-- Structural Stand Legs -->
        <line x1="16" y1="62" x2="10" y2="82" stroke="#1E293B" stroke-width="3" stroke-linecap="round" />
        <line x1="88" y1="62" x2="94" y2="82" stroke="#1E293B" stroke-width="3" stroke-linecap="round" />
      </g>
    """

# =========================================================================
# D. RO, UF & MEMBRANE SYSTEMS
# =========================================================================

# 13. Reverse Osmosis (RO) Membrane Skid (ro)
def get_ro_membrane_skid(has_fluid=True):
    fluid_streams = ""
    if has_fluid:
        fluid_streams = """
          <!-- Pressurized Permeate & Brine Reject Flows -->
          <line x1="4" y1="22" x2="16" y2="22" stroke="#0284C7" stroke-width="3.5" stroke-linecap="round" />
          <line x1="4" y1="42" x2="16" y2="42" stroke="#0284C7" stroke-width="3.5" stroke-linecap="round" />
          <!-- Permeate Pure Line (Right Top - Cyan) -->
          <line x1="86" y1="22" x2="96" y2="22" stroke="#38BDF8" stroke-width="3" stroke-linecap="round" />
          <!-- Concentrate Brine Reject Line (Right Bottom - Orange) -->
          <line x1="86" y1="42" x2="96" y2="42" stroke="#EA580C" stroke-width="3" stroke-linecap="round" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <!-- Stainless Steel Structural Skid Frame -->
        <rect x="14" y="8" width="74" height="66" fill="none" stroke="#64748B" stroke-width="2" />
        <line x1="14" y1="32" x2="88" y2="32" stroke="#94A3B8" stroke-width="1.5" />
        <!-- Tube 1 (Top Pressure Vessel FRP Housing) -->
        <rect x="16" y="14" width="70" height="16" rx="8" fill="url(#ss316GradH)" stroke="#1E293B" stroke-width="2" />
        <!-- Tube 2 (Bottom Pressure Vessel FRP Housing) -->
        <rect x="16" y="34" width="70" height="16" rx="8" fill="url(#ss316GradH)" stroke="#1E293B" stroke-width="2" />
        <!-- End Flange Caps & Victaulic Clamps -->
        <rect x="16" y="12" width="6" height="20" rx="2" fill="#0B2545" />
        <rect x="80" y="12" width="6" height="20" rx="2" fill="#0B2545" />
        <rect x="16" y="32" width="6" height="20" rx="2" fill="#0B2545" />
        <rect x="80" y="32" width="6" height="20" rx="2" fill="#0B2545" />
        {fluid_streams}
        <!-- Pressure Gauges on Skid Manifold -->
        <circle cx="28" cy="8" r="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2" />
        <circle cx="74" cy="8" r="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2" />
      </g>
    """

# 14. Ultrafiltration (UF System) Skid
def get_uf_ultrafiltration_skid(has_fluid=True):
    fluid = ""
    if has_fluid:
        fluid = """
          <!-- Hollow Fiber Permeate Flow -->
          <rect x="22" y="18" width="14" height="52" rx="3" fill="url(#softWaterGrad)" opacity="0.9" />
          <rect x="42" y="18" width="14" height="52" rx="3" fill="url(#softWaterGrad)" opacity="0.9" />
          <rect x="62" y="18" width="14" height="52" rx="3" fill="url(#softWaterGrad)" opacity="0.9" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <!-- Skid Header Manifolds (Top Feed / Bottom Permeate) -->
        <rect x="12" y="8" width="74" height="8" rx="2" fill="url(#ss316GradH)" stroke="#1E293B" stroke-width="1.5" />
        <rect x="12" y="74" width="74" height="8" rx="2" fill="url(#ss316GradH)" stroke="#1E293B" stroke-width="1.5" />
        <!-- 3 Vertical Hollow-Fiber UF Membrane Columns -->
        <rect x="20" y="16" width="18" height="58" rx="6" fill="#F8FAFC" stroke="#0284C7" stroke-width="2" />
        <rect x="40" y="16" width="18" height="58" rx="6" fill="#F8FAFC" stroke="#0284C7" stroke-width="2" />
        <rect x="60" y="16" width="18" height="58" rx="6" fill="#F8FAFC" stroke="#0284C7" stroke-width="2" />
        {fluid}
      </g>
    """

# 15. Micron / Cartridge Filter Housing (micronFilter)
def get_micron_cartridge_filter(has_fluid=True):
    fluid = ""
    if has_fluid:
        fluid = """
          <!-- Filtered Water Surrounding Cartridge -->
          <rect x="16" y="24" width="36" height="54" rx="4" fill="url(#softWaterGrad)" opacity="0.8" />
        """
    return f"""
      <g transform="translate(0, 0)">
        <ellipse cx="34" cy="86" rx="20" ry="4" fill="#0B2545" opacity="0.14" />
        <!-- SS316 Cylindrical Vessel Housing -->
        <rect x="14" y="20" width="40" height="62" rx="6" fill="url(#ss316GradH)" stroke="#334155" stroke-width="2" />
        {fluid}
        <!-- Internal 5-Micron Pleated Filter Cartridge Core -->
        <rect x="24" y="24" width="20" height="52" rx="3" fill="#FFFFFF" stroke="#0284C7" stroke-width="1.2" />
        <line x1="28" y1="28" x2="40" y2="28" stroke="#38BDF8" stroke-width="0.8" />
        <line x1="28" y1="36" x2="40" y2="36" stroke="#38BDF8" stroke-width="0.8" />
        <line x1="28" y1="44" x2="40" y2="44" stroke="#38BDF8" stroke-width="0.8" />
        <line x1="28" y1="52" x2="40" y2="52" stroke="#38BDF8" stroke-width="0.8" />
        <line x1="28" y1="60" x2="40" y2="60" stroke="#38BDF8" stroke-width="0.8" />
        <line x1="28" y1="68" x2="40" y2="68" stroke="#38BDF8" stroke-width="0.8" />
        <!-- Top Dome Cover with Eyebolts -->
        <path d="M14 20 C14 8, 54 8, 54 20 Z" fill="url(#ss316GradV)" stroke="#1E293B" stroke-width="1.8" />
        <!-- Inlet & Outlet Flanged Ports -->
        <rect x="4" y="32" width="10" height="10" rx="2" fill="url(#ss316GradH)" stroke="#1E293B" stroke-width="1.2" />
        <rect x="54" y="52" width="10" height="10" rx="2" fill="url(#ss316GradH)" stroke="#1E293B" stroke-width="1.2" />
        <!-- Top Vent / Pressure Gauge Port -->
        <circle cx="34" cy="8" r="4" fill="#FFFFFF" stroke="#0284C7" stroke-width="1" />
      </g>
    """

# =========================================================================
# E. HVAC, COOLING & FACILITY CONSUMERS
# =========================================================================

# 16. Cooling Tower (Cooling Tower)
def get_cooling_tower(has_fluid=True):
    fluid = ""
    if has_fluid:
        fluid = """
          <!-- Cascading Water Droplets Over Fills & Full Cold Water Basin -->
          <rect x="14" y="66" width="68" height="14" rx="2" fill="url(#treatedWaterGrad)" />
          <!-- Spray Nozzle Rain Drops -->
          <g fill="#38BDF8" opacity="0.8">
            <circle cx="24" cy="46" r="1.2" /><circle cx="28" cy="54" r="1.5" /><circle cx="36" cy="48" r="1.2" />
            <circle cx="48" cy="52" r="1.5" /><circle cx="60" cy="46" r="1.2" /><circle cx="68" cy="54" r="1.5" />
          </g>
        """
    return f"""
      <g transform="translate(0, 0)">
        <!-- FRP Tower Casing (Flared Body) -->
        <polygon points="20,24 76,24 82,78 14,78" fill="url(#filterVesselGrad)" stroke="#0369A1" stroke-width="2" />
        {fluid}
        <!-- Honeycomb PVC Fill Pack Louvers -->
        <rect x="22" y="44" width="52" height="20" fill="#E2E8F0" stroke="#64748B" stroke-width="1" stroke-dasharray="3 2" />
        <!-- Top Induced-Draft Fan Cylinder Cowl & Spinning Fan -->
        <rect x="30" y="8" width="36" height="16" rx="3" fill="#1E293B" stroke="#0B2545" stroke-width="2" />
        <ellipse cx="48" cy="10" rx="14" ry="4" fill="#64748B" stroke="#CBD5E1" stroke-width="1.2" />
        <!-- Cold Water Basin on Bottom -->
        <rect x="10" y="76" width="76" height="12" rx="3" fill="#334155" stroke="#0F172A" stroke-width="1.8" />
      </g>
    """

# 17. Commercial Building / Facility Consumer (building)
def get_commercial_building():
    return """
      <g transform="translate(0, 0)">
        <!-- Skyscraper / Commercial Facility Tower -->
        <rect x="16" y="8" width="48" height="78" rx="3" fill="#0284C7" stroke="#0B2545" stroke-width="2" />
        <!-- Grid of Windows -->
        <g fill="#E0F2FE" opacity="0.9">
          <rect x="22" y="16" width="6" height="8" rx="1" /><rect x="32" y="16" width="6" height="8" rx="1" /><rect x="42" y="16" width="6" height="8" rx="1" /><rect x="52" y="16" width="6" height="8" rx="1" />
          <rect x="22" y="28" width="6" height="8" rx="1" /><rect x="32" y="28" width="6" height="8" rx="1" /><rect x="42" y="28" width="6" height="8" rx="1" /><rect x="52" y="28" width="6" height="8" rx="1" />
          <rect x="22" y="40" width="6" height="8" rx="1" /><rect x="32" y="40" width="6" height="8" rx="1" /><rect x="42" y="40" width="6" height="8" rx="1" /><rect x="52" y="40" width="6" height="8" rx="1" />
          <rect x="22" y="52" width="6" height="8" rx="1" /><rect x="32" y="52" width="6" height="8" rx="1" /><rect x="42" y="52" width="6" height="8" rx="1" /><rect x="52" y="52" width="6" height="8" rx="1" />
          <rect x="22" y="64" width="6" height="8" rx="1" /><rect x="32" y="64" width="6" height="8" rx="1" /><rect x="42" y="64" width="6" height="8" rx="1" /><rect x="52" y="64" width="6" height="8" rx="1" />
        </g>
        <!-- Entrance Canopy -->
        <rect x="34" y="74" width="12" height="12" rx="1" fill="#1E293B" />
      </g>
    """

# =========================================================================
# F. PRESERVED STP TANKS (FROM PREVIOUS BATCH)
# =========================================================================
def get_stp_collection_tank(is_filled=True):
    fluid = ""
    if is_filled:
        fluid = """
          <g>
            <path d="M 2 56 Q 87.5 68 173 56 L 173 76 Q 87.5 93 2 76 Z" fill="url(#rawSewageGrad)" />
            <ellipse cx="87.5" cy="56" rx="85.5" ry="6.5" fill="#8D6E63" stroke="#D7CCC8" stroke-width="0.8" opacity="0.95" />
            <ellipse cx="87.5" cy="56" rx="80" ry="4.5" fill="#A1887F" opacity="0.4" />
          </g>
          <circle cx="45" cy="65" r="2.0" fill="#D7CCC8" opacity="0.7" /><circle cx="80" cy="62" r="2.8" fill="#D7CCC8" opacity="0.7" />
          <circle cx="115" cy="66" r="2.2" fill="#D7CCC8" opacity="0.7" /><circle cx="145" cy="63" r="2.4" fill="#D7CCC8" opacity="0.7" />
        """
    return f"""
      <ellipse cx="87.5" cy="88" rx="84" ry="7" fill="#0B2545" opacity="0.12" />
      <path d="M 0 76 Q 87.5 94 175 76 L 175 14 Q 87.5 30 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#94A3B8" stroke-width="1.5" />
      {fluid}
      <g transform="translate(8, 25)">
        <rect x="0" y="0" width="22" height="48" rx="2" fill="#334155" opacity="0.25" stroke="#64748B" stroke-width="1" />
        <line x1="4" y1="2" x2="4" y2="46" stroke="#94A3B8" stroke-width="0.8" /><line x1="8" y1="2" x2="8" y2="46" stroke="#94A3B8" stroke-width="0.8" />
        <line x1="12" y1="2" x2="12" y2="46" stroke="#94A3B8" stroke-width="0.8" /><line x1="16" y1="2" x2="16" y2="46" stroke="#94A3B8" stroke-width="0.8" />
        <line x1="20" y1="2" x2="20" y2="46" stroke="#94A3B8" stroke-width="0.8" />
      </g>
      <line x1="30" y1="74" x2="160" y2="74" stroke="#D97706" stroke-width="2" stroke-linecap="round" />
      <rect x="6" y="16" width="16" height="58" rx="3" fill="url(#specularSheen)" />
      <line x1="168" y1="16" x2="168" y2="76" stroke="#FFFFFF" stroke-width="1.2" opacity="0.4" />
      <ellipse cx="87.5" cy="14" rx="87.5" ry="8" fill="url(#glassRimGrad)" stroke="#94A3B8" stroke-width="1.5" />
      <ellipse cx="87.5" cy="14" rx="82" ry="5.5" fill="none" stroke="#CBD5E1" stroke-width="1" stroke-dasharray="3 3" />
    """

def get_stp_mbbr_tank(is_filled=True):
    fluid = ""
    if is_filled:
        fluid = """
          <path d="M 2 24 Q 70 38 138 24 L 138 76 Q 70 93 2 76 Z" fill="url(#mbbrWaterGrad)" />
          <ellipse cx="70" cy="24" rx="68" ry="6.5" fill="#6B7852" stroke="#A3E635" stroke-width="0.8" opacity="0.92" />
          <ellipse cx="70" cy="24" rx="62" ry="4.5" fill="#9E8D72" opacity="0.4" />
          <g fill="#F8FAFC" stroke="#0284C7" stroke-width="0.8" opacity="0.88">
            <circle cx="22" cy="44" r="3.4" /><line x1="19.6" y1="44" x2="24.4" y2="44" stroke-width="0.6" /><line x1="22" y1="41.6" x2="22" y2="46.4" stroke-width="0.6" />
            <circle cx="50" cy="66" r="4.0" /><line x1="47" y1="66" x2="53" y2="66" stroke-width="0.6" /><line x1="50" y1="63" x2="50" y2="69" stroke-width="0.6" />
            <circle cx="80" cy="50" r="3.2" /><line x1="77.8" y1="50" x2="82.2" y2="50" stroke-width="0.6" /><line x1="80" y1="47.8" x2="80" y2="52.2" stroke-width="0.6" />
            <circle cx="104" cy="68" r="3.6" /><circle cx="114" cy="44" r="2.8" /><circle cx="38" cy="58" r="2.4" /><circle cx="68" cy="38" r="2.6" />
          </g>
          <g fill="#FFFFFF" opacity="0.85">
            <circle cx="22" cy="55" r="2.2" /><circle cx="46" cy="48" r="3.0" /><circle cx="70" cy="52" r="2.0" /><circle cx="94" cy="42" r="2.8" /><circle cx="112" cy="50" r="2.4" />
          </g>
        """
    return f"""
      <ellipse cx="70" cy="88" rx="66" ry="7" fill="#0B2545" opacity="0.14" />
      <path d="M 0 76 Q 70 94 140 76 L 140 14 Q 70 30 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />
      {fluid}
      <g transform="translate(126, 26)">
        <rect x="0" y="0" width="10" height="48" rx="1.5" fill="#1E293B" opacity="0.3" stroke="#0284C7" stroke-width="1" />
        <line x1="1" y1="8" x2="9" y2="8" stroke="#38BDF8" stroke-width="0.8" stroke-dasharray="1 1" />
        <line x1="1" y1="16" x2="9" y2="16" stroke="#38BDF8" stroke-width="0.8" stroke-dasharray="1 1" />
        <line x1="1" y1="24" x2="9" y2="24" stroke="#38BDF8" stroke-width="0.8" stroke-dasharray="1 1" />
      </g>
      <line x1="18" y1="74" x2="122" y2="74" stroke="#D97706" stroke-width="2.5" stroke-linecap="round" />
      <rect x="5" y="16" width="14" height="58" rx="3" fill="url(#specularSheen)" />
      <line x1="134" y1="16" x2="134" y2="76" stroke="#FFFFFF" stroke-width="1.2" opacity="0.4" />
      <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
    """

def get_stp_clarifier_tank(is_filled=True):
    fluid = ""
    if is_filled:
        fluid = """
          <path d="M 2 22 L 2 54 L 138 54 L 138 22 Z" fill="url(#clarifierWaterGrad)" opacity="0.88" />
          <ellipse cx="70" cy="22" rx="68" ry="6.5" fill="#BAE6FD" stroke="#38BDF8" stroke-width="0.8" opacity="0.92" />
          <path d="M 2 54 L 54 88 Q 70 93 86 88 L 138 54 Z" fill="url(#sludgeWaterGrad)" />
        """
    return f"""
      <ellipse cx="70" cy="94" rx="45" ry="6" fill="#0B2545" opacity="0.16" />
      <path d="M 0 14 L 0 54 L 54 88 Q 70 93 86 88 L 140 54 L 140 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />
      {fluid}
      <path d="M 4 20 L 136 20" stroke="#38BDF8" stroke-width="1.2" stroke-dasharray="3 2" opacity="0.75" />
      <g transform="translate(70, 52)">
        <circle cx="0" cy="0" r="16" fill="url(#metalRingGrad)" stroke="#16A34A" stroke-width="1.5" />
        <circle cx="0" cy="0" r="12" fill="#DCFCE7" stroke="#16A34A" stroke-width="1.2" />
        <line x1="-12" y1="0" x2="12" y2="0" stroke="#15803D" stroke-width="2.5" stroke-linecap="round" />
        <line x1="0" y1="-12" x2="0" y2="12" stroke="#15803D" stroke-width="2.5" stroke-linecap="round" />
        <circle cx="0" cy="0" r="3.5" fill="#15803D" />
      </g>
      <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
    """

def get_stp_sludge_tank(is_filled=True):
    fluid = ""
    if is_filled:
        fluid = """
          <path d="M 2 34 L 2 46 L 42 68 Q 57.5 73 73 68 L 113 46 L 113 34 Z" fill="url(#sludgeWaterGrad)" />
          <ellipse cx="57.5" cy="34" rx="55.5" ry="5.5" fill="#5D4037" stroke="#8D6E63" stroke-width="0.8" opacity="0.95" />
        """
    return f"""
      <ellipse cx="57.5" cy="72" rx="45" ry="5" fill="#0B2545" opacity="0.14" />
      <path d="M 0 12 L 0 46 L 42 68 Q 57.5 73 73 68 L 115 46 L 115 12 Z" fill="url(#glassCylinderGrad)" stroke="#94A3B8" stroke-width="1.5" />
      {fluid}
      <ellipse cx="57.5" cy="12" rx="57.5" ry="6.5" fill="url(#glassRimGrad)" stroke="#94A3B8" stroke-width="1.5" />
    """

def get_stp_filter_feed_tank(is_filled=True):
    fluid = ""
    if is_filled:
        fluid = """
          <path d="M 2 45 Q 70 57 138 45 L 138 76 Q 70 93 2 76 Z" fill="url(#filterFeedGrad)" />
          <ellipse cx="70" cy="45" rx="68" ry="6.5" fill="#7DD3FC" stroke="#0284C7" stroke-width="0.8" opacity="0.9" />
        """
    return f"""
      <ellipse cx="70" cy="88" rx="66" ry="7" fill="#0B2545" opacity="0.14" />
      <path d="M 0 76 Q 70 94 140 76 L 140 14 Q 70 30 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />
      {fluid}
      <g transform="translate(10, 22)" opacity="0.6">
        <line x1="0" y1="0" x2="8" y2="0" stroke="#0369A1" stroke-width="1" />
        <line x1="0" y1="15" x2="5" y2="15" stroke="#0369A1" stroke-width="1" />
      </g>
      <ellipse cx="70" cy="14" rx="70" ry="7.5" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
    """

def get_stp_psf(is_filled=True):
    media = ""
    if is_filled:
        media = """
          <g transform="translate(9, 38)">
            <rect x="0" y="0" width="64" height="50" rx="4" fill="#0F172A" stroke="#7DD3FC" stroke-width="1.2" />
            <rect x="2" y="2" width="60" height="18" fill="url(#sandMediaGrad)" opacity="0.9" />
            <rect x="2" y="20" width="60" height="15" fill="#B45309" opacity="0.95" />
            <rect x="2" y="35" width="60" height="13" rx="2" fill="#451A03" opacity="0.95" />
            <line x1="12" y1="44" x2="52" y2="44" stroke="#CBD5E1" stroke-width="2" stroke-linecap="round" />
          </g>
        """
    else:
        media = """
          <g transform="translate(9, 38)">
            <rect x="0" y="0" width="64" height="50" rx="4" fill="#0B2545" stroke="#7DD3FC" stroke-width="1.2" />
            <rect x="2" y="2" width="60" height="46" rx="2" fill="#1E293B" opacity="0.7" />
            <line x1="12" y1="44" x2="52" y2="44" stroke="#CBD5E1" stroke-width="2" stroke-linecap="round" />
          </g>
        """
    return f"""
      <ellipse cx="41" cy="120" rx="36" ry="6" fill="#0B2545" opacity="0.18" />
      <path d="M 1 22 C 1 4, 81 4, 81 22 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
      <rect x="1" y="22" width="80" height="78" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
      <path d="M 1 100 C 1 118, 81 118, 81 100 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
      {media}
    """

def get_stp_acf(is_filled=True):
    media = ""
    if is_filled:
        media = """
          <g transform="translate(9, 38)">
            <rect x="0" y="0" width="64" height="50" rx="4" fill="#0F172A" stroke="#7DD3FC" stroke-width="1.2" />
            <rect x="2" y="2" width="60" height="34" fill="url(#carbonMediaGrad)" opacity="0.95" />
            <rect x="2" y="36" width="60" height="12" rx="2" fill="#1E293B" opacity="0.95" />
            <line x1="12" y1="44" x2="52" y2="44" stroke="#CBD5E1" stroke-width="2" stroke-linecap="round" />
          </g>
        """
    else:
        media = """
          <g transform="translate(9, 38)">
            <rect x="0" y="0" width="64" height="50" rx="4" fill="#0B2545" stroke="#7DD3FC" stroke-width="1.2" />
            <rect x="2" y="2" width="60" height="46" rx="2" fill="#1E293B" opacity="0.7" />
            <line x1="12" y1="44" x2="52" y2="44" stroke="#CBD5E1" stroke-width="2" stroke-linecap="round" />
          </g>
        """
    return f"""
      <ellipse cx="41" cy="120" rx="36" ry="6" fill="#0B2545" opacity="0.18" />
      <path d="M 1 22 C 1 4, 81 4, 81 22 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
      <rect x="1" y="22" width="80" height="78" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
      <path d="M 1 100 C 1 118, 81 118, 81 100 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
      {media}
    """

def get_stp_softener(is_filled=True):
    media = ""
    if is_filled:
        media = """
          <g transform="translate(10, 32)">
            <rect x="0" y="0" width="58" height="40" rx="3" fill="#0F172A" stroke="#7DD3FC" stroke-width="1.2" />
            <rect x="2" y="2" width="54" height="28" fill="url(#resinMediaGrad)" opacity="0.95" />
            <rect x="2" y="30" width="54" height="8" rx="2" fill="#78350F" opacity="0.95" />
            <line x1="8" y1="34" x2="50" y2="34" stroke="#CBD5E1" stroke-width="1.8" />
          </g>
        """
    else:
        media = """
          <g transform="translate(10, 32)">
            <rect x="0" y="0" width="58" height="40" rx="3" fill="#0B2545" stroke="#7DD3FC" stroke-width="1.2" />
            <rect x="2" y="2" width="54" height="36" rx="2" fill="#1E293B" opacity="0.7" />
            <line x1="8" y1="34" x2="50" y2="34" stroke="#CBD5E1" stroke-width="1.8" />
          </g>
        """
    return f"""
      <ellipse cx="40" cy="100" rx="36" ry="5" fill="#0B2545" opacity="0.16" />
      <path d="M 1 18 C 1 3, 79 3, 79 18 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
      <rect x="1" y="18" width="78" height="68" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
      <path d="M 1 86 C 1 100, 79 100, 79 86 Z" fill="url(#filterVesselGrad)" stroke="#0284C7" stroke-width="2" />
      {media}
    """

def get_stp_treated_tank(is_filled=True):
    fluid = ""
    if is_filled:
        fluid = """
          <path d="M 2 14 Q 70 25 138 14 L 138 74 Q 70 89 2 74 Z" fill="url(#treatedWaterGrad)" />
          <ellipse cx="70" cy="14" rx="68" ry="6.0" fill="#E0F2FE" stroke="#38BDF8" stroke-width="0.8" opacity="0.95" />
        """
    return f"""
      <ellipse cx="70" cy="85" rx="66" ry="6" fill="#0B2545" opacity="0.14" />
      <path d="M 0 74 Q 70 90 140 74 L 140 14 Q 70 28 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />
      {fluid}
      <line x1="12" y1="14" x2="12" y2="60" stroke="#0284C7" stroke-width="2.5" />
      <polygon points="9,58 12,65 15,58" fill="#0284C7" />
      <ellipse cx="70" cy="14" rx="70" ry="7.0" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
    """

def get_stp_soft_tank(is_filled=True):
    fluid = ""
    if is_filled:
        fluid = """
          <path d="M 2 14 Q 70 25 138 14 L 138 74 Q 70 89 2 74 Z" fill="url(#softWaterGrad)" />
          <ellipse cx="70" cy="14" rx="68" ry="6.0" fill="#F0F9FF" stroke="#38BDF8" stroke-width="0.8" opacity="0.98" />
        """
    return f"""
      <ellipse cx="70" cy="85" rx="66" ry="6" fill="#0B2545" opacity="0.14" />
      <path d="M 0 74 Q 70 90 140 74 L 140 14 Q 70 28 0 14 Z" fill="url(#glassCylinderGrad)" stroke="#0284C7" stroke-width="2" />
      {fluid}
      <ellipse cx="70" cy="14" rx="70" ry="7.0" fill="url(#glassRimGrad)" stroke="#0284C7" stroke-width="1.5" />
    """

def get_scada_blower(is_running=True):
    color = "#16A34A" if is_running else "#F43F5E"
    fill = "#DCFCE7" if is_running else "#FCE7F3"
    blade_color = "#15803D" if is_running else "#BE123C"
    return f"""
      <g transform="translate(0, 0)">
        <circle cx="0" cy="0" r="18" fill="url(#metalRingGrad)" stroke="{color}" stroke-width="1.5" />
        <circle cx="0" cy="0" r="14" fill="{fill}" stroke="{color}" stroke-width="2.2" />
        <path d="M -7 0 L 7 0 M 0 -7 L 0 7 M -5 -5 L 5 5 M -5 5 L 5 -5" stroke="{blade_color}" stroke-width="2.2" stroke-linecap="round" />
        <circle cx="11.5" cy="-11.5" r="3.5" fill="{color}" stroke="#FFFFFF" stroke-width="0.8" />
      </g>
    """

def get_uv_light():
    return """
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="80" height="46" rx="8" fill="#FAF5FF" stroke="#9333EA" stroke-width="2" />
        <rect x="5" y="5" width="70" height="36" rx="5" fill="#C084FC" opacity="0.2" />
        <line x1="10" y1="12" x2="70" y2="12" stroke="#A855F7" stroke-width="3.5" stroke-linecap="round" />
        <line x1="10" y1="23" x2="70" y2="23" stroke="#16A34A" stroke-width="3.5" stroke-linecap="round" />
        <line x1="10" y1="34" x2="70" y2="34" stroke="#A855F7" stroke-width="3.5" stroke-linecap="round" />
      </g>
    """

def get_clarifier_valve():
    return """
      <g transform="translate(0, 0)">
        <circle cx="0" cy="0" r="16" fill="url(#metalRingGrad)" stroke="#16A34A" stroke-width="1.2" />
        <circle cx="0" cy="0" r="13" fill="#DCFCE7" stroke="#16A34A" stroke-width="2.2" />
        <circle cx="0" cy="0" r="4.5" fill="#15803D" />
        <circle cx="9" cy="-9" r="2.8" fill="#16A34A" stroke="#FFFFFF" stroke-width="0.8" />
      </g>
    """

def get_water_solenoid_valve():
    return """
      <g transform="translate(0, 0)">
        <circle cx="0" cy="0" r="17" fill="url(#metalRingGrad)" stroke="#16A34A" stroke-width="1.2" />
        <circle cx="0" cy="0" r="13.5" fill="#DCFCE7" stroke="#16A34A" stroke-width="2.2" />
        <circle cx="0" cy="0" r="5" fill="#0F172A" />
        <circle cx="9.5" cy="-9.5" r="3.0" fill="#16A34A" stroke="#FFFFFF" stroke-width="0.8" />
      </g>
    """

def get_acf_multiport_valve():
    return """
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="75" height="68" rx="6" fill="#DCFCE7" stroke="#16A34A" stroke-width="2" />
        <circle cx="37.5" cy="34" r="6" fill="#16A34A" stroke="#064E3B" stroke-width="1.5" />
        <rect x="30" y="4" width="15" height="8" rx="2" fill="#0284C7" />
        <rect x="4" y="27" width="8" height="14" rx="2" fill="#166534" />
        <rect x="63" y="27" width="8" height="14" rx="2" fill="#DC2626" />
        <rect x="30" y="56" width="15" height="8" rx="2" fill="#166534" />
      </g>
    """

def get_pressure_gauge_unit():
    return """
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="70" height="42" rx="5" fill="#FFFFFF" stroke="#0284C7" stroke-width="2" />
        <circle cx="35" cy="21" r="14" fill="#F0F9FF" stroke="#0284C7" stroke-width="1.5" />
        <line x1="35" y1="21" x2="42" y2="15" stroke="#E11D48" stroke-width="2" stroke-linecap="round" />
        <circle cx="35" cy="21" r="2.5" fill="#0369A1" />
      </g>
    """

# =========================================================================
# COMPLETE MULTI-PLANT ASSET CATALOG (STP, ETP, WTP, RO, COOLING, PUMPS)
# =========================================================================
MULTI_PLANT_ASSETS = {
    # 1. PUMPS (FLUID VS. DRY)
    "pump-centrifugal-fluid": (get_centrifugal_pump(True), "-22 -22 50 44", 300, 264),
    "pump-centrifugal-dry": (get_centrifugal_pump(False), "-22 -22 50 44", 300, 264),
    "pump-ro-high-pressure-fluid": (get_multistage_ro_pump(True), "0 0 60 106", 240, 424),
    "pump-ro-high-pressure-dry": (get_multistage_ro_pump(False), "0 0 60 106", 240, 424),
    "pump-submersible-sump-fluid": (get_submersible_sump_pump(True), "0 0 60 90", 240, 360),
    "pump-submersible-sump-dry": (get_submersible_sump_pump(False), "0 0 60 90", 240, 360),
    "pump-chemical-dosing-fluid": (get_chemical_dosing_pump(True), "-3 -2 46 78", 230, 390),
    "pump-chemical-dosing-dry": (get_chemical_dosing_pump(False), "-3 -2 46 78", 230, 390),

    # 2. WTP (WATER TREATMENT PLANT)
    "wtp-tanker-supply-fluid": (get_water_tanker_supply(True), "6 10 94 82", 376, 328),
    "wtp-tanker-supply-dry": (get_water_tanker_supply(False), "6 10 94 82", 376, 328),
    "wtp-rainwater-pond-fluid": (get_rainwater_pond(True), "-6 8 116 70", 380, 230),
    "wtp-rainwater-pond-dry": (get_rainwater_pond(False), "-6 8 116 70", 380, 230),
    "wtp-multi-grade-filter-mgf-fluid": (get_multi_grade_filter_mgf(True), "-5 0 92 128", 276, 384),
    "wtp-multi-grade-filter-mgf-empty": (get_multi_grade_filter_mgf(False), "-5 0 92 128", 276, 384),

    # 3. ETP (EFFLUENT TREATMENT PLANT)
    "etp-flash-mixer-tank-fluid": (get_etp_flash_mixer(True), "-5 0 100 106", 300, 318),
    "etp-flash-mixer-tank-empty": (get_etp_flash_mixer(False), "-5 0 100 106", 300, 318),
    "etp-flocculator-tank-fluid": (get_etp_flocculator_tank(True), "-5 0 120 106", 360, 318),
    "etp-flocculator-tank-empty": (get_etp_flocculator_tank(False), "-5 0 120 106", 360, 318),
    "etp-lamella-tube-settler-fluid": (get_etp_lamella_tube_settler(True), "-5 8 100 84", 300, 252),
    "etp-lamella-tube-settler-empty": (get_etp_lamella_tube_settler(False), "-5 8 100 84", 300, 252),
    "etp-daf-flotation-tank-fluid": (get_etp_daf_tank(True), "-2 8 104 74", 340, 240),
    "etp-daf-flotation-tank-empty": (get_etp_daf_tank(False), "-2 8 104 74", 340, 240),
    "etp-sludge-filter-press-clamped": (get_sludge_filter_press(True), "0 8 104 80", 340, 260),
    "etp-sludge-filter-press-open": (get_sludge_filter_press(False), "0 8 104 80", 340, 260),

    # 4. RO, UF & MEMBRANE SYSTEMS
    "ro-membrane-skid-fluid": (get_ro_membrane_skid(True), "0 0 100 80", 350, 280),
    "ro-membrane-skid-dry": (get_ro_membrane_skid(False), "0 0 100 80", 350, 280),
    "uf-ultrafiltration-skid-fluid": (get_uf_ultrafiltration_skid(True), "8 2 82 86", 328, 344),
    "uf-ultrafiltration-skid-dry": (get_uf_ultrafiltration_skid(False), "8 2 82 86", 328, 344),
    "micron-cartridge-filter-fluid": (get_micron_cartridge_filter(True), "0 2 68 90", 272, 360),
    "micron-cartridge-filter-empty": (get_micron_cartridge_filter(False), "0 2 68 90", 272, 360),

    # 5. HVAC, COOLING & FACILITY CONSUMERS
    "hvac-cooling-tower-fluid": (get_cooling_tower(True), "6 2 84 92", 336, 368),
    "hvac-cooling-tower-dry": (get_cooling_tower(False), "6 2 84 92", 336, 368),
    "facility-commercial-building": (get_commercial_building(), "10 2 60 92", 240, 368),

    # 6. STP (SEWAGE TREATMENT PLANT)
    "stp-collection-tank-filled": (get_stp_collection_tank(True), "-10 5 195 90", 390, 180),
    "stp-collection-tank-empty": (get_stp_collection_tank(False), "-10 5 195 90", 390, 180),
    "stp-mbbr-aeration-tank-filled": (get_stp_mbbr_tank(True), "-10 5 160 90", 320, 180),
    "stp-mbbr-aeration-tank-empty": (get_stp_mbbr_tank(False), "-10 5 160 90", 320, 180),
    "stp-secondary-clarifier-filled": (get_stp_clarifier_tank(True), "-10 5 160 96", 320, 192),
    "stp-secondary-clarifier-empty": (get_stp_clarifier_tank(False), "-10 5 160 96", 320, 192),
    "stp-sludge-holding-tank-filled": (get_stp_sludge_tank(True), "-10 5 135 74", 270, 148),
    "stp-sludge-holding-tank-empty": (get_stp_sludge_tank(False), "-10 5 135 74", 270, 148),
    "stp-filter-feed-tank-filled": (get_stp_filter_feed_tank(True), "-10 5 160 90", 320, 180),
    "stp-filter-feed-tank-empty": (get_stp_filter_feed_tank(False), "-10 5 160 90", 320, 180),
    "stp-pressure-sand-filter-filled": (get_stp_psf(True), "-5 0 92 128", 276, 384),
    "stp-pressure-sand-filter-empty": (get_stp_psf(False), "-5 0 92 128", 276, 384),
    "stp-activated-carbon-filter-filled": (get_stp_acf(True), "-5 0 92 128", 276, 384),
    "stp-activated-carbon-filter-empty": (get_stp_acf(False), "-5 0 92 128", 276, 384),
    "stp-water-softener-column-filled": (get_stp_softener(True), "-5 0 90 108", 270, 324),
    "stp-water-softener-column-empty": (get_stp_softener(False), "-5 0 90 108", 270, 324),
    "stp-treated-water-tank-filled": (get_stp_treated_tank(True), "-10 5 160 88", 320, 176),
    "stp-treated-water-tank-empty": (get_stp_treated_tank(False), "-10 5 160 88", 320, 176),
    "stp-soft-water-tank-filled": (get_stp_soft_tank(True), "-10 5 160 88", 320, 176),
    "stp-soft-water-tank-empty": (get_stp_soft_tank(False), "-10 5 160 88", 320, 176),

    # 7. BLOWERS, UV & VALVES
    "scada-blower-running": (get_scada_blower(True), "-22 -22 44 44", 264, 264),
    "scada-blower-stopped": (get_scada_blower(False), "-22 -22 44 44", 264, 264),
    "scada-uv-light": (get_uv_light(), "-3 -3 86 52", 344, 208),
    "scada-clarifier-valve": (get_clarifier_valve(), "-20 -20 40 40", 240, 240),
    "scada-water-solenoid-valve": (get_water_solenoid_valve(), "-20 -20 40 40", 240, 240),
    "scada-acf-multiport-valve-block": (get_acf_multiport_valve(), "-3 -3 81 74", 324, 296),
    "scada-pressure-gauge": (get_pressure_gauge_unit(), "-3 -3 76 48", 304, 192),
}

def main():
    print(f"Generating {len(MULTI_PLANT_ASSETS)} pure-graphic SVG files (no text, no numbers) into {SVG_DIR}...")
    svg_files = []
    for name, (content, viewbox, w, h) in MULTI_PLANT_ASSETS.items():
        svg_content = wrap_svg(content, viewbox=viewbox, width=w, height=h)
        file_path = os.path.join(SVG_DIR, f"{name}.svg")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        svg_files.append((name, file_path, w, h))
    print(f"Successfully wrote {len(svg_files)} clean SVG files.")

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    print(f"Rendering {len(svg_files)} transparent PNGs at 2x resolution into {PNG_DIR}...")
    for idx, (name, svg_path, w, h) in enumerate(svg_files, start=1):
        png_path = os.path.join(PNG_DIR, f"{name}.png")
        file_url = "file:///" + svg_path.replace("\\", "/")
        target_w = w * 2
        target_h = h * 2
        cmd = [
            edge_path,
            "--headless=new",
            f"--screenshot={png_path}",
            "--default-background-color=00000000",
            f"--window-size={target_w},{target_h}",
            file_url,
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print(f"[{idx:02d}/{len(svg_files)}] Rendered {name}.png ({target_w}x{target_h})")
        except Exception as e:
            print(f"[{idx:02d}/{len(svg_files)}] Error rendering {name}: {e}")

    print("\nAll multi-plant schematic assets successfully generated!")

if __name__ == "__main__":
    main()
