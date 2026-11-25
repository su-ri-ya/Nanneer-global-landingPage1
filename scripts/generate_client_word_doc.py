import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def create_document():
    doc = Document()

    # Set 0.7 inch margins for spacious corporate presentation
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Base Colors
    NAVY_HEX = "0B2545"
    CYAN_HEX = "0284C7"
    SLATE_HEX = "334155"
    LIGHT_BG = "F8FAFC"
    BORDER_HEX = "E2E8F0"

    NAVY = RGBColor(11, 37, 69)
    CYAN = RGBColor(2, 132, 199)
    SLATE = RGBColor(51, 65, 85)
    GRAY = RGBColor(100, 116, 139)

    # -------------------------------------------------------------
    # 1. HEADER WITH LOGOS
    # -------------------------------------------------------------
    header_table = doc.add_table(rows=1, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False

    header_table.columns[0].width = Inches(3.5)
    header_table.columns[1].width = Inches(3.5)

    cell_left = header_table.cell(0, 0)
    cell_right = header_table.cell(0, 1)

    p_left = cell_left.paragraphs[0]
    p_left.alignment = WD_ALIGN_PARAGRAPH.LEFT
    prestige_logo = os.path.abspath("public/images/prestige-group-logo.png")
    if os.path.exists(prestige_logo):
        p_left.add_run().add_picture(prestige_logo, width=Inches(1.8))

    p_right = cell_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    ppms_logo = os.path.abspath("public/images/ppms-logo.jpg")
    if os.path.exists(ppms_logo):
        p_right.add_run().add_picture(ppms_logo, width=Inches(1.5))

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # 2. DOCUMENT TITLE & METADATA
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_after = Pt(2)
    r_kicker = title_p.add_run("CLIENT TECHNICAL PRESENTATION & SPECIFICATION MANUAL\n")
    r_kicker.font.size = Pt(9.5)
    r_kicker.font.bold = True
    r_kicker.font.color.rgb = CYAN

    r_title = title_p.add_run("PRESTIGE TRANQUILITY — 950 KLD STP\n")
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY

    r_sub = title_p.add_run("SCADA Process Architecture & Real-Time Flow Schematic")
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = SLATE

    # Metadata Strip Box
    meta_table = doc.add_table(rows=1, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_widths = [Inches(1.75), Inches(1.75), Inches(1.75), Inches(1.75)]
    meta_data = [
        ("PROJECT", "Prestige Tranquility"),
        ("PLANT CAPACITY", "950 KLD (950 m³/day)"),
        ("OPERATION", "24/7 Automated SCADA"),
        ("LOCATION", "Budigere Cross, BLR")
    ]
    for i, (label, val) in enumerate(meta_data):
        c = meta_table.cell(0, i)
        c.width = meta_widths[i]
        set_cell_background(c, "F1F5F9")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r1 = p.add_run(f"{label}\n")
        r1.font.size = Pt(7.5)
        r1.font.bold = True
        r1.font.color.rgb = GRAY
        r2 = p.add_run(val)
        r2.font.size = Pt(9.5)
        r2.font.bold = True
        r2.font.color.rgb = NAVY

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # 3. EXECUTIVE PROCESS SCHEMATIC (FULL WIDTH HIGH-RES GRAPHIC)
    # -------------------------------------------------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(10)
    h1.paragraph_format.space_after = Pt(4)
    r_h1 = h1.add_run("1. Executive SCADA Process Schematic Overview")
    r_h1.font.size = Pt(13)
    r_h1.font.bold = True
    r_h1.font.color.rgb = NAVY

    p_desc = doc.add_paragraph()
    p_desc.paragraph_format.space_after = Pt(8)
    r_desc = p_desc.add_run(
        "The following diagram illustrates the complete hydraulic and mechanical process train engineered for Prestige Tranquility's "
        "950 KLD Sewage Treatment Plant. All pipelines, transfer pumps (M1–M11), air blowers (BL1–BL2), clarification units, and "
        "dual distribution headers (Flushing & Gardening) are monitored via real-time SCADA telemetry."
    )
    r_desc.font.size = Pt(9.5)
    r_desc.font.color.rgb = SLATE

    # Embed Animated GIF
    schematic_gif = os.path.abspath("public/images/schematic_animated.gif")
    schematic_png = os.path.abspath("public/images/schematic_screenshot.png")
    image_to_use = schematic_gif if os.path.exists(schematic_gif) else schematic_png

    if os.path.exists(image_to_use):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(image_to_use, width=Inches(7.0))
        
        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_caption.paragraph_format.space_after = Pt(14)
        r_cap = p_caption.add_run("Figure 1.0: Real-Time SCADA Animated Process Mimic — Live Fluid Flow & Mechanical Rotation Loop\n")
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = GRAY
        r_subcap = p_caption.add_run("(In modern Microsoft Word & Office 365, the graphic above continuously loops the fluid motion)")
        r_subcap.font.size = Pt(8.0)
        r_subcap.font.bold = True
        r_subcap.font.color.rgb = CYAN

    # -------------------------------------------------------------
    # 4. COLOR CODING & PIPELINE CONVENTIONS
    # -------------------------------------------------------------
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(8)
    h2.paragraph_format.space_after = Pt(4)
    r_h2 = h2.add_run("2. Pipeline Fluid Media & SCADA Color Designations")
    r_h2.font.size = Pt(12)
    r_h2.font.bold = True
    r_h2.font.color.rgb = NAVY

    color_table = doc.add_table(rows=5, cols=3)
    color_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    color_widths = [Inches(1.8), Inches(1.8), Inches(3.4)]
    
    headers = ["Fluid / Media Stream", "Color Code", "Process Description & Target Stage"]
    for j, h in enumerate(headers):
        c = color_table.cell(0, j)
        c.width = color_widths[j]
        set_cell_background(c, "0B2545")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    color_rows = [
        ("Raw Sewage / Influent", "Amber / Brown (#F59E0B)", "Screening & Equalization to Aeration Tanks 1 & 2"),
        ("Mixed Liquor Suspended Solids", "Violet / Indigo (#818CF8)", "Biological oxidation & Secondary Clarifier settling"),
        ("Clarified Water & Filtrate", "Teal / Cyan (#06B6D4)", "Filter Feed Sump through MGF & ACF filters"),
        ("Treated Recycled Water", "Emerald Green (#10B981)", "Ultrafiltration permeate to Flushing & Gardening distribution")
    ]

    for i, row in enumerate(color_rows):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            c = color_table.cell(i + 1, j)
            c.width = color_widths[j]
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            r.font.color.rgb = NAVY if j == 0 else SLATE
            if j == 0:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # 5. STAGE-BY-STAGE PROCESS ARCHITECTURE
    # -------------------------------------------------------------
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(8)
    h3.paragraph_format.space_after = Pt(4)
    r_h3 = h3.add_run("3. Stage-by-Stage Process Treatment Train")
    r_h3.font.size = Pt(12)
    r_h3.font.bold = True
    r_h3.font.color.rgb = NAVY

    stages = [
        ("Stage 1: Primary Screening & Equalization",
         "Raw sewage from residential blocks enters the Bar Screen Chamber to remove gross suspended solids, plastics, and debris. "
         "The screened effluent flows by gravity into the Raw Sewage Sump (Equalization Basin), which balances hydraulic fluctuations "
         "and chemical load. Raw Sewage Transfer Pumps (M1 Duty, M2 Standby, M3 Standby) transfer sewage at controlled rates to biological aeration."),
        
        ("Stage 2: Aeration Basins 1 & 2 (Extended Aeration ASP)",
         "Biological digestion occurs in two interconnected aeration basins equipped with fine bubble membrane diffusers. "
         "Twin Air Blowers (BL2 Duty operating at 45 Hz; BL1 Standby) deliver 1,450 CFM of air, maintaining Dissolved Oxygen (DO) at 2.4 mg/L. "
         "Heterotrophic microorganisms digest carbonaceous BOD and nitrify ammonia into nitrates under continuous agitation."),

        ("Stage 3: Secondary Clarifier & Sludge Handling",
         "The mixed liquor overflows into the Secondary Clarifier where bio-solids settle gently by gravity aided by a slow-speed bridge scraper. "
         "Clear supernatant overflows the peripheral V-notch weirs into the Clarified Water Sump. Settled biological sludge is continuously "
         "recirculated (RAS) to Aeration Tank 1 to maintain MLSS at 3,800 mg/L, with excess sludge (WAS) pumped to the Sludge Holding Tank and Filter Press."),

        ("Stage 4: Dual Media Filtration & Ultrafiltration (UF) Polishing",
         "Clarified water is pressurized by Filter Feed Pumps (M4, M5) and routed sequentially through a Multi-Grade Sand Filter (MGF) to eliminate "
         "suspended solids (>25 microns) and an Activated Carbon Filter (ACF) for dechlorination and color/odor adsorption. "
         "Water then passes through the Ultrafiltration Skid (M6 Duty, M7 Backwash) equipped with 0.02-micron hollow fiber membranes, ensuring complete pathogen and colloidal removal."),

        ("Stage 5: Disinfection & Dual Distribution (Flushing & Gardening)",
         "Ultrafiltration permeate receives final sodium hypochlorite dosing in the Chlorine Contact Tank before splitting into two dedicated sumps:\n"
         "• Flushing Water Sump: Pressurized by hydro-pneumatic pumps (M8 Duty, M9 Duty) delivering continuous 3.8 bar pressure for residential toilet flushing.\n"
         "• Gardening Water Sump: Fed by irrigation booster pumps (M10 Duty, M11 Standby) providing automated landscape irrigation.")
    ]

    for title, desc in stages:
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(4)
        sp.paragraph_format.space_after = Pt(2)
        r_st = sp.add_run(f"• {title}")
        r_st.font.size = Pt(10)
        r_st.font.bold = True
        r_st.font.color.rgb = CYAN

        sd = doc.add_paragraph()
        sd.paragraph_format.left_indent = Inches(0.2)
        sd.paragraph_format.space_after = Pt(6)
        r_sd = sd.add_run(desc)
        r_sd.font.size = Pt(9)
        r_sd.font.color.rgb = SLATE

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # -------------------------------------------------------------
    # 6. EQUIPMENT SCHEDULE & PUMP TELEMETRY REGISTER
    # -------------------------------------------------------------
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(8)
    h4.paragraph_format.space_after = Pt(4)
    r_h4 = h4.add_run("4. Comprehensive Equipment Schedule & Motor Telemetry")
    r_h4.font.size = Pt(12)
    r_h4.font.bold = True
    r_h4.font.color.rgb = NAVY

    equip_data = [
        ("M1", "Raw Sewage Feed Pump 1", "DUTY", "45 m³/hr, 5.5 kW", "RUNNING (48 Hz)"),
        ("M2", "Raw Sewage Feed Pump 2", "STANDBY", "45 m³/hr, 5.5 kW", "READY (0 Hz)"),
        ("M3", "Raw Sewage Feed Pump 3", "STANDBY", "45 m³/hr, 5.5 kW", "READY (0 Hz)"),
        ("BL1", "Fine Bubble Air Blower 1", "STANDBY", "1,450 CFM, 22 kW", "STANDBY (0 RPM)"),
        ("BL2", "Fine Bubble Air Blower 2", "DUTY", "1,450 CFM, 22 kW", "RUNNING (1,450 RPM)"),
        ("CLR", "Clarifier Central Scraper", "DUTY", "0.75 kW, 2 RPM", "ACTIVE ROTATION"),
        ("M4", "Filter Feed Pump 1", "DUTY", "50 m³/hr, 7.5 kW", "RUNNING (50 Hz)"),
        ("M5", "Filter Feed Pump 2", "DUTY", "50 m³/hr, 7.5 kW", "RUNNING (50 Hz)"),
        ("M6", "Ultrafiltration Feed Pump", "DUTY", "45 m³/hr, 5.5 kW", "RUNNING (45 Hz)"),
        ("M7", "UF Membrane Backwash Pump", "STANDBY", "60 m³/hr, 7.5 kW", "INTERMITTENT"),
        ("M8", "Flushing Distribution Pump 1", "DUTY", "30 m³/hr, 3.8 bar", "RUNNING (3.8 Bar)"),
        ("M9", "Flushing Distribution Pump 2", "DUTY", "30 m³/hr, 3.8 bar", "RUNNING (3.8 Bar)"),
        ("M10", "Gardening Irrigation Pump 1", "DUTY", "25 m³/hr, 3.2 bar", "RUNNING (3.2 Bar)"),
        ("M11", "Gardening Irrigation Pump 2", "STANDBY", "25 m³/hr, 3.2 bar", "READY (0 Bar)")
    ]

    equip_table = doc.add_table(rows=len(equip_data) + 1, cols=5)
    equip_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    eq_widths = [Inches(1.0), Inches(2.2), Inches(1.1), Inches(1.2), Inches(1.5)]
    eq_headers = ["Tag ID", "Equipment Designation", "Role", "Rating / Flow", "SCADA Status"]

    for j, h in enumerate(eq_headers):
        c = equip_table.cell(0, j)
        c.width = eq_widths[j]
        set_cell_background(c, "0B2545")
        set_cell_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for i, row in enumerate(equip_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            c = equip_table.cell(i + 1, j)
            c.width = eq_widths[j]
            set_cell_background(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            
            if j == 2:  # Duty / Standby
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129) if "DUTY" in val else RGBColor(239, 68, 68)
            elif j == 0:
                r.font.bold = True
                r.font.color.rgb = NAVY
            else:
                r.font.color.rgb = SLATE

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # 7. WATER QUALITY STANDARDS & EFFLUENT DISCHARGE NORMS
    # -------------------------------------------------------------
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(8)
    h5.paragraph_format.space_after = Pt(4)
    r_h5 = h5.add_run("5. Water Quality Balance & Compliance Norms (CPCB / KSPCB)")
    r_h5.font.size = Pt(12)
    r_h5.font.bold = True
    r_h5.font.color.rgb = NAVY

    qual_table = doc.add_table(rows=6, cols=4)
    qual_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    q_widths = [Inches(1.8), Inches(1.7), Inches(1.7), Inches(1.8)]
    q_headers = ["Water Quality Parameter", "Raw Influent Sewage", "Treated Output Water", "Reuse Compliance Standard"]

    for j, h in enumerate(q_headers):
        c = qual_table.cell(0, j)
        c.width = q_widths[j]
        set_cell_background(c, "0B2545")
        set_cell_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    qual_data = [
        ("pH Value", "6.8 – 7.8", "7.3 – 7.5", "6.5 – 8.5"),
        ("Biochemical Oxygen Demand (BOD₅)", "250 – 350 mg/L", "< 5.0 mg/L", "< 10 mg/L"),
        ("Chemical Oxygen Demand (COD)", "450 – 600 mg/L", "< 30 mg/L", "< 50 mg/L"),
        ("Total Suspended Solids (TSS)", "200 – 300 mg/L", "< 2.0 mg/L", "< 10 mg/L"),
        ("Turbidity", "150 – 250 NTU", "< 1.0 NTU", "< 2.0 NTU")
    ]

    for i, row in enumerate(qual_data):
        bg = "FFFFFF" if i % 2 == 0 else "F8FAFC"
        for j, val in enumerate(row):
            c = qual_table.cell(i + 1, j)
            c.width = q_widths[j]
            set_cell_background(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if j == 2:
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)
            elif j == 0:
                r.font.bold = True
                r.font.color.rgb = NAVY
            else:
                r.font.color.rgb = SLATE

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # -------------------------------------------------------------
    # 8. HOW TO ACCESS LIVE INTERACTIVE ANIMATED SIMULATION
    # -------------------------------------------------------------
    sim_box = doc.add_table(rows=1, cols=1)
    sim_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_box = sim_box.cell(0, 0)
    c_box.width = Inches(7.0)
    set_cell_background(c_box, "EFF6FF")
    set_cell_margins(c_box, top=140, bottom=140, left=180, right=180)
    
    p_box = c_box.paragraphs[0]
    p_box.paragraph_format.space_after = Pt(4)
    r_bt = p_box.add_run("⚡ Accessing the Live Animated SCADA Simulation\n")
    r_bt.font.size = Pt(11)
    r_bt.font.bold = True
    r_bt.font.color.rgb = CYAN

    r_bd = p_box.add_run(
        "For the complete animated visual presentation featuring continuous fluid flows, active vortex agitation, rotating clarifier bridges, "
        "and live telemetry clocks, open the accompanying standalone document:\n\n"
        "• Offline Document File: STP_SCADA_Process_Schematic_Client_Presentation.html\n"
        "• Features: 115 live SVG flow paths, 20 rotating mechanical drives, Fullscreen presentation mode, and zero internet requirement.\n"
        "• Recommended for client meetings, projector presentations, and WhatsApp/Email dispatch."
    )
    r_bd.font.size = Pt(9)
    r_bd.font.color.rgb = NAVY

    # Save Document
    out_docx_1 = os.path.abspath("Prestige_Tranquility_950KLD_STP_SCADA_Process_Manual.docx")
    out_docx_2 = os.path.abspath("public/Prestige_Tranquility_950KLD_STP_SCADA_Process_Manual.docx")

    doc.save(out_docx_1)
    doc.save(out_docx_2)

    print("SUCCESS: Generated Client Word Document:")
    print("1.", out_docx_1)
    print("2.", out_docx_2)

if __name__ == "__main__":
    create_document()
