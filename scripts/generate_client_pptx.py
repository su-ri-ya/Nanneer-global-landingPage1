import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions (13.33 x 7.5 inches)
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    NAVY = RGBColor(11, 37, 69)
    CYAN = RGBColor(2, 132, 199)
    SLATE = RGBColor(51, 65, 85)
    LIGHT_BG = RGBColor(248, 250, 252)
    WHITE = RGBColor(255, 255, 255)
    GRAY = RGBColor(100, 116, 139)

    prestige_logo = os.path.abspath("public/images/prestige-group-logo.png")
    ppms_logo = os.path.abspath("public/images/ppms-logo.jpg")
    video_path = os.path.abspath("Prestige_STP_950KLD_Live_Fluid_Flow.mp4")
    poster_frame = os.path.abspath("public/images/schematic_screenshot.png")

    # =============================================================
    # SLIDE 1: EXECUTIVE TITLE & BRANDING SLIDE
    # =============================================================
    s1 = prs.slides.add_slide(blank_layout)

    # Background
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = LIGHT_BG
    bg1.line.fill.background()

    # Top Brand Bar
    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.33), Inches(0.18))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = CYAN
    bar1.line.fill.background()

    # Logos
    if os.path.exists(prestige_logo):
        s1.shapes.add_picture(prestige_logo, Inches(1.0), Inches(0.8), width=Inches(2.5))
    if os.path.exists(ppms_logo):
        s1.shapes.add_picture(ppms_logo, Inches(10.0), Inches(0.8), width=Inches(2.2))

    # Title Box
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(11.33), Inches(2.8))
    tf = t_box.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "CLIENT TECHNICAL PRESENTATION & OPERATIONAL SPECIFICATION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = CYAN
    p0.space_after = Pt(10)

    p1 = tf.add_paragraph()
    p1.text = "Prestige Tranquility — 950 KLD STP"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    p1.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "Real-Time SCADA Digital Twin & Process Automation Flow Schematic"
    p2.font.size = Pt(18)
    p2.font.color.rgb = SLATE
    p2.space_after = Pt(16)

    p3 = tf.add_paragraph()
    p3.text = "Facility: Prestige Tranquility, Budigere Cross, Bengaluru  |  Design Capacity: 950,000 Liters / Day (100% Recycled Water)"
    p3.font.size = Pt(12)
    p3.font.color.rgb = GRAY

    # Metric Cards
    metrics = [
        ("950 KLD", "Daily Design Capacity"),
        ("100% RECYCLED", "Flushing & Gardening"),
        ("11 PUMPS & 2 BLOWERS", "Dual Redundancy SCADA"),
        ("CPCB COMPLIANT", "BOD < 5 mg/L | TSS < 2 mg/L")
    ]
    for i, (val, lbl) in enumerate(metrics):
        x = Inches(1.0 + i * 2.85)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(5.4), Inches(2.65), Inches(1.2))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = RGBColor(203, 213, 225)
        
        c_tf = card.text_frame
        c_tf.word_wrap = True
        cp1 = c_tf.paragraphs[0]
        cp1.text = val
        cp1.font.size = Pt(15)
        cp1.font.bold = True
        cp1.font.color.rgb = NAVY
        cp1.alignment = PP_ALIGN.CENTER
        
        cp2 = c_tf.add_paragraph()
        cp2.text = lbl
        cp2.font.size = Pt(9.5)
        cp2.font.color.rgb = CYAN
        cp2.alignment = PP_ALIGN.CENTER

    # =============================================================
    # SLIDE 2: FULL ANIMATED PROCESS SCHEMATIC (EMBEDDED VIDEO)
    # =============================================================
    s2 = prs.slides.add_slide(blank_layout)

    # Header
    h2_box = s2.shapes.add_textbox(Inches(0.6), Inches(0.2), Inches(12.13), Inches(0.9))
    h2_tf = h2_box.text_frame
    h2_p = h2_tf.paragraphs[0]
    h2_p.text = "Prestige Tranquility 950 KLD STP — Full Animated Process Schematic"
    h2_p.font.size = Pt(20)
    h2_p.font.bold = True
    h2_p.font.color.rgb = NAVY

    h2_sub = h2_tf.add_paragraph()
    h2_sub.text = "Live SCADA Fluid Flow: Equalization ➔ MBBR Aeration ➔ Clarifier ➔ Filter Feed ➔ PSF/ACF/Softener ➔ Flushing & Gardening (Click Video to Play)"
    h2_sub.font.size = Pt(10)
    h2_sub.font.color.rgb = SLATE

    # Embed Video with Poster Frame
    if os.path.exists(video_path):
        s2.shapes.add_movie(
            video_path,
            Inches(0.6), Inches(1.15), Inches(12.13), Inches(6.0),
            poster_frame_image=poster_frame if os.path.exists(poster_frame) else None,
            mime_type='video/mp4'
        )

    # =============================================================
    # SLIDE 3: STAGE-BY-STAGE PROCESS TREATMENT TRAIN
    # =============================================================
    s3 = prs.slides.add_slide(blank_layout)
    h3_box = s3.shapes.add_textbox(Inches(0.8), Inches(0.3), Inches(11.73), Inches(0.8))
    h3_tf = h3_box.text_frame
    h3_p = h3_tf.paragraphs[0]
    h3_p.text = "Stage-by-Stage Process Treatment Train"
    h3_p.font.size = Pt(20)
    h3_p.font.bold = True
    h3_p.font.color.rgb = NAVY

    stages_data = [
        ("STAGE 1: PRIMARY EQUALIZATION", "Bar screen chamber removes gross debris. Equalization basin buffers hydraulic peaks. Raw sewage transfer pumps (M1 Duty, M2/M3 Standby) feed biological aeration.", CYAN),
        ("STAGE 2: BIOLOGICAL AERATION (MBBR)", "Twin aeration basins with fine-bubble diffused aeration. Blower BL2 (Duty, 45 Hz) maintains DO at 2.4 mg/L. Heterotrophic biomass digests soluble organic pollutants.", NAVY),
        ("STAGE 3: SECONDARY CLARIFICATION", "Conical hopper clarifier with slow-speed bridge scraper. Clear supernatant overflows to filter feed basin. RAS returns active biomass; excess sludge WAS goes to filter press.", CYAN),
        ("STAGE 4: TERTIARY MEDIA FILTRATION", "Filter feed pumps (M10 Duty, M11 Standby) pressurize multi-grade sand filter (PSF), activated carbon filter (ACF), and water softener for polishing.", NAVY),
        ("STAGE 5: TREATED DUAL DISTRIBUTION", "Ultra-polished water receives sodium hypochlorite disinfection and splits into two dedicated sumps: Flushing Water (3.8 bar) and Gardening Irrigation (3.2 bar).", CYAN)
    ]

    for i, (st_title, st_desc, color) in enumerate(stages_data):
        y = Inches(1.2 + i * 1.15)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.73), Inches(1.0))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = RGBColor(226, 232, 240)
        
        b_tf = box.text_frame
        b_tf.word_wrap = True
        bp1 = b_tf.paragraphs[0]
        bp1.text = st_title
        bp1.font.size = Pt(11)
        bp1.font.bold = True
        bp1.font.color.rgb = color
        bp1.space_after = Pt(2)
        
        bp2 = b_tf.add_paragraph()
        bp2.text = st_desc
        bp2.font.size = Pt(9.5)
        bp2.font.color.rgb = SLATE

    # =============================================================
    # SLIDE 4: EQUIPMENT SCHEDULE & MOTOR TELEMETRY
    # =============================================================
    s4 = prs.slides.add_slide(blank_layout)
    h4_box = s4.shapes.add_textbox(Inches(0.8), Inches(0.3), Inches(11.73), Inches(0.8))
    h4_tf = h4_box.text_frame
    h4_p = h4_tf.paragraphs[0]
    h4_p.text = "Equipment Schedule & Operational Duty/Standby Designation"
    h4_p.font.size = Pt(20)
    h4_p.font.bold = True
    h4_p.font.color.rgb = NAVY

    table_shape = s4.shapes.add_table(11, 5, Inches(0.8), Inches(1.25), Inches(11.73), Inches(5.6))
    t = table_shape.table
    t.columns[0].width = Inches(1.2)
    t.columns[1].width = Inches(3.6)
    t.columns[2].width = Inches(1.8)
    t.columns[3].width = Inches(2.5)
    t.columns[4].width = Inches(2.63)

    eq_headers = ["Tag ID", "Equipment Name", "Role", "Rating / Flow", "SCADA Operating Mode"]
    for j, val in enumerate(eq_headers):
        cell = t.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE

    eq_rows = [
        ("M1", "Raw Sewage Feed Pump 1", "DUTY", "45 m³/hr, 5.5 kW", "RUNNING (48 Hz)"),
        ("M2", "Raw Sewage Feed Pump 2", "STANDBY", "45 m³/hr, 5.5 kW", "READY (0 Hz)"),
        ("M3", "MBBR Feed Pump 3", "STANDBY", "45 m³/hr, 5.5 kW", "READY (0 Hz)"),
        ("M4", "MBBR Feed Pump 4", "DUTY", "45 m³/hr, 5.5 kW", "RUNNING (48 Hz)"),
        ("BL1", "Fine Bubble Air Blower 1", "STANDBY", "1,450 CFM, 22 kW", "STANDBY (0 RPM)"),
        ("BL2", "Fine Bubble Air Blower 2", "DUTY", "1,450 CFM, 22 kW", "RUNNING (1,450 RPM)"),
        ("CLR", "Clarifier Bridge Scraper", "DUTY", "0.75 kW, 2 RPM", "ACTIVE ROTATION"),
        ("M10", "Filter Feed Pump 1", "DUTY", "50 m³/hr, 7.5 kW", "RUNNING (50 Hz)"),
        ("M11", "Filter Feed Pump 2", "STANDBY", "50 m³/hr, 7.5 kW", "READY (0 Hz)"),
        ("M12", "Flushing & Gardening Booster", "DUTY", "30 m³/hr, 3.8 bar", "RUNNING (3.8 Bar)")
    ]

    for i, row in enumerate(eq_rows):
        for j, val in enumerate(row):
            cell = t.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            if j == 2:
                p.font.bold = True
                p.font.color.rgb = RGBColor(16, 185, 129) if "DUTY" in val else RGBColor(239, 68, 68)
            elif j == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY
            else:
                p.font.color.rgb = SLATE

    # =============================================================
    # SLIDE 5: WATER QUALITY BALANCE & COMPLIANCE
    # =============================================================
    s5 = prs.slides.add_slide(blank_layout)
    h5_box = s5.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.73), Inches(0.8))
    h5_tf = h5_box.text_frame
    h5_p = h5_tf.paragraphs[0]
    h5_p.text = "Water Quality Balance & Compliance Norms (CPCB / KSPCB Standards)"
    h5_p.font.size = Pt(20)
    h5_p.font.bold = True
    h5_p.font.color.rgb = NAVY

    t5_shape = s5.shapes.add_table(6, 4, Inches(0.8), Inches(1.5), Inches(11.73), Inches(5.0))
    t5 = t5_shape.table
    t5.columns[0].width = Inches(2.93)
    t5.columns[1].width = Inches(2.93)
    t5.columns[2].width = Inches(2.93)
    t5.columns[3].width = Inches(2.94)

    q_headers = ["Water Quality Parameter", "Raw Influent Sewage", "Treated Output Water", "CPCB / KSPCB Reuse Norms"]
    for j, val in enumerate(q_headers):
        cell = t5.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE

    q_rows = [
        ("pH Value", "6.8 – 7.8", "7.3 – 7.5", "6.5 – 8.5"),
        ("Biochemical Oxygen Demand (BOD₅)", "250 – 350 mg/L", "< 5.0 mg/L (98.5% Removal)", "< 10.0 mg/L"),
        ("Chemical Oxygen Demand (COD)", "450 – 600 mg/L", "< 30.0 mg/L (95.0% Removal)", "< 50.0 mg/L"),
        ("Total Suspended Solids (TSS)", "200 – 300 mg/L", "< 2.0 mg/L (99.3% Removal)", "< 10.0 mg/L"),
        ("Turbidity", "150 – 250 NTU", "< 1.0 NTU (Ultra-Clear)", "< 2.0 NTU")
    ]

    for i, row in enumerate(q_rows):
        for j, val in enumerate(row):
            cell = t5.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if i % 2 == 0 else LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            if j == 2:
                p.font.bold = True
                p.font.color.rgb = RGBColor(16, 185, 129)
            elif j == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY
            else:
                p.font.color.rgb = SLATE

    # Save
    out_pptx = os.path.abspath("Prestige_STP_950KLD_Client_Presentation.pptx")
    out_pptx_pub = os.path.abspath("public/Prestige_STP_950KLD_Client_Presentation.pptx")
    prs.save(out_pptx)
    prs.save(out_pptx_pub)
    print("SUCCESS: Generated 5-Slide Executive PPTX with Embedded Video:")
    print("1.", out_pptx)
    print("2.", out_pptx_pub)

if __name__ == "__main__":
    create_presentation()
