import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    DARK_NAVY = RGBColor(11, 30, 46)     # #0B1E2E
    TEAL_PRIMARY = RGBColor(13, 148, 136) # #0D9488
    TEAL_DARK = RGBColor(15, 118, 110)    # #0F766E
    EMERALD = RGBColor(16, 185, 129)      # #10B981
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252)    # #F8FAFC
    SLATE_TEXT = RGBColor(15, 23, 42)     # #0F172A
    MUTED_TEXT = RGBColor(100, 116, 139)  # #64748B
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0

    def add_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text, dark_mode=False):
        # Top Accent Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = TEAL_PRIMARY if not dark_mode else RGBColor(45, 212, 191)

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = WHITE if dark_mode else SLATE_TEXT

    # -------------------------------------------------------------
    # SLIDE 1: COVER
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, DARK_NAVY)

    # Accent line
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(1.2), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL_PRIMARY
    bar.line.fill.background()

    tag_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(11), Inches(0.4))
    p = tag_box.text_frame.paragraphs[0]
    p.text = "STP OPERATIONS & MAINTENANCE FOR COMMERCIAL BUILDINGS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(45, 212, 191)

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(11.5), Inches(1.8))
    tf = t_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Your STP Is Running.\nBut Is It Delivering?"
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = WHITE

    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(10), Inches(1.2))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p = tf_sub.paragraphs[0]
    p.text = "We manage your STP 24×7 to maximize sewage treatment, recover reusable water, prevent operational failures, and keep every activity documented."
    p.font.size = Pt(17)
    p.font.color.rgb = RGBColor(203, 213, 225)

    p2 = tf_sub.add_paragraph()
    p2.text = "Not just manpower. Complete operational accountability."
    p2.font.size = Pt(17)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(52, 211, 153)
    p2.space_before = Pt(10)

    brand_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(6), Inches(0.5))
    p_b = brand_box.text_frame.paragraphs[0]
    p_b.text = "NANNEER GLOBAL · CLIENT STRATEGY SPECIFICATION"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------
    # SLIDE 2: THE PROBLEM
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2, LIGHT_BG)
    add_header(s2, "The Industry Problem", "Managing an STP Shouldn't Be a Daily Headache.")

    desc_box = s2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(0.8))
    p = desc_box.text_frame.paragraphs[0]
    p.text = "You have enough responsibilities managing your building. Your STP should not require constant follow-ups, unexpected interventions, or last-minute preparation for inspections."
    p.font.size = Pt(15)
    p.font.color.rgb = MUTED_TEXT

    cards = [
        ("Water Wastage", "Treated water not fully utilized.", "Treated water overflows into drains while expensive fresh water tankers are purchased."),
        ("Unexpected Incidents", "Overflows, breakdowns and complaints.", "Sludge bulking, septic odors, and pump breakdowns that disrupt tenant operations."),
        ("Poor Documentation", "Incomplete logs and missing records.", "Handwritten, unverified operator log sheets that create serious regulatory exposure."),
        ("Manpower Dependency", "Constant supervision and follow-ups.", "High operator turnover and missing shifts requiring non-technical facility teams to step in.")
    ]

    for i, (title, highlight, details) in enumerate(cards):
        left = Inches(0.8 + i * 2.95)
        top = Inches(2.7)
        width = Inches(2.75)
        height = Inches(3.9)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.3), width - Inches(0.4), height - Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"0{i+1}"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = SLATE_TEXT
        p2.space_before = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = highlight
        p3.font.size = Pt(13)
        p3.font.bold = True
        p3.font.color.rgb = TEAL_DARK
        p3.space_before = Pt(8)

        p4 = tf.add_paragraph()
        p4.text = details
        p4.font.size = Pt(12)
        p4.font.color.rgb = MUTED_TEXT
        p4.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 3: THE SOLUTION (3 PILLARS)
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3, LIGHT_BG)
    add_header(s3, "The Solution", "One Partner. Complete STP Responsibility.")

    desc_box = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(0.7))
    p = desc_box.text_frame.paragraphs[0]
    p.text = "From operator deployment to water recovery and monthly reporting, we bring the essential elements of STP operations under one accountable service."
    p.font.size = Pt(15)
    p.font.color.rgb = MUTED_TEXT

    solutions = [
        ("24×7 Plant Operations",
         "Trained operators across three shifts, supported by defined SOPs, supervision, and preventive maintenance.",
         ["• Certified 3-shift 24×7 plant coverage", "• Strict SOPs for dosing, backwash & aeration", "• Weekly mechanical & electrical checklists"]),
        ("Maximum Water Recovery",
         "Measure, treat, and maximize safe reuse of wastewater for cooling towers, toilet flushing, and gardening.",
         ["• High-volume cooling tower makeup reuse", "• Clean effluent for dual-plumbing flushing", "• Zero liquid wastage with landscape balancing"]),
        ("Digital Monitoring & Accountability",
         "Track water quantity, quality, tank levels, equipment health, and scheduled activities with documented evidence.",
         ["• Digital daily flow & parameter logging", "• Fortnightly NABL-certified lab test audits", "• Daily timestamped WhatsApp video proof"])
    ]

    for i, (title, sub, bullets) in enumerate(solutions):
        left = Inches(0.8 + i * 3.95)
        top = Inches(2.7)
        width = Inches(3.75)
        height = Inches(4.0)

        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = TEAL_PRIMARY
        card.line.width = Pt(1.5)

        tb = s3.shapes.add_textbox(left + Inches(0.25), top + Inches(0.3), width - Inches(0.5), height - Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"PILLAR 0{i+1}"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(19)
        p2.font.bold = True
        p2.font.color.rgb = SLATE_TEXT
        p2.space_before = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = sub
        p3.font.size = Pt(12)
        p3.font.color.rgb = MUTED_TEXT
        p3.space_before = Pt(8)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = b
            pb.font.size = Pt(12)
            pb.font.color.rgb = SLATE_TEXT
            pb.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 4: PERFORMANCE SLA & TARGETS
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4, LIGHT_BG)
    add_header(s4, "Operations You Can Verify", "Performance You Can Measure. Operations You Can Verify.")

    # 3 Big Badges
    targets = [
        ("≥99%", "Sewage Treatment Target", "Zero bypass guarantee with daily flow balancing"),
        ("≥99%", "STP Availability Target", "Preventive lubrication and instant backup pump switchover"),
        ("≥99%", "Manpower Coverage Target", "3 certified shifts with guaranteed reliever deployment")
    ]

    for i, (metric, label, expl) in enumerate(targets):
        left = Inches(0.8 + i * 3.95)
        top = Inches(1.8)
        width = Inches(3.75)
        height = Inches(1.8)

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(240, 253, 250)
        card.line.color.rgb = RGBColor(153, 246, 228)
        card.line.width = Pt(1.5)

        tb = s4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = metric
        p1.font.size = Pt(36)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = SLATE_TEXT

        p3 = tf.add_paragraph()
        p3.text = expl
        p3.font.size = Pt(11)
        p3.font.color.rgb = MUTED_TEXT

    # Lower summary card: Monthly Management Report Details
    rpt_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.9), Inches(11.65), Inches(2.9))
    rpt_card.fill.solid()
    rpt_card.fill.fore_color.rgb = DARK_NAVY
    rpt_card.line.fill.background()

    tb = s4.shapes.add_textbox(Inches(1.1), Inches(4.1), Inches(11.0), Inches(2.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Monthly Management Report & Client Dashboard Metrics"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p_sub = tf.add_paragraph()
    p_sub.text = "Delivered every 1st of the month with timestamped logs, water balance sheets, and laboratory certificates."
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(4)

    # 4 Highlights inside the navy card
    modules = [
        "1. Water Balance (KLD): 14,850 Inflow · 14,713 Treated · 14,566 Reused (99.0% Recovery)",
        "2. Water Quality: pH 7.2 · BOD 6 mg/L (Std ≤10) · COD 28 mg/L (Std ≤50) · TSS 8 mg/L",
        "3. Equipment Availability: Feed Pumps 99.6% · Blowers 99.2% · Overall Uptime 99.4%",
        "4. Documented Evidence: Shift A, B, C 100% Manned · WhatsApp video updates daily"
    ]
    for m in modules:
        pm = tf.add_paragraph()
        pm.text = f"✔  {m}"
        pm.font.size = Pt(13)
        pm.font.color.rgb = RGBColor(167, 243, 208)
        pm.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 5: ASSESSMENT & ACTION
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5, LIGHT_BG)
    add_header(s5, "Facility Assessment", "Is Your STP Performing at Its Best?")

    desc_box = s5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(0.8))
    p = desc_box.text_frame.paragraphs[0]
    p.text = "Let's discuss your existing STP operations, water recovery potential, and opportunities to improve reliability. No detailed technical information is required to start the conversation."
    p.font.size = Pt(15)
    p.font.color.rgb = MUTED_TEXT

    # 3 Step Next Actions
    actions = [
        ("Step 1: Facility Profile", "Commercial office / IT park, Hotel, Shopping mall, or mixed-use development with capacity from 50 to 2,000+ KLD."),
        ("Step 2: Rapid Site Diagnostic", "Free 48-hour assessment of existing blower efficiency, sludge volume index, and treated water reuse avenues."),
        ("Step 3: Outcome-Guaranteed Contract", "Transition to Nanneer Global 24×7 O&M with measurable SLA targets, digital reporting, and zero headache.")
    ]

    for i, (title, text) in enumerate(actions):
        left = Inches(0.8 + i * 3.95)
        top = Inches(2.8)
        width = Inches(3.75)
        height = Inches(3.5)

        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tb = s5.shapes.add_textbox(left + Inches(0.25), top + Inches(0.3), width - Inches(0.5), height - Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = SLATE_TEXT

        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.size = Pt(13)
        p2.font.color.rgb = MUTED_TEXT
        p2.space_before = Pt(10)

    # Output file paths
    prs.save("C:/Nanneer global/draft 3/public/Nanneer_Global_STP_Operations_Presentation.pptx")
    prs.save("C:/Nanneer global/draft 3/Nanneer_Global_STP_Operations_Presentation.pptx")
    print("Successfully generated 16:9 Presentation in draft 3 and public folder!")

if __name__ == "__main__":
    create_deck()

