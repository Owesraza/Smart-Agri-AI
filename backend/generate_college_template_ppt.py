#!/usr/bin/env python3
"""
CropPoint — College Template Review 3 Presentation (13 Slides)
Includes ALL 11 exact headings requested:
1. Title Slide
2. Introduction
3. Problem Statement
4. Motivation
5. Literature Survey
6. Scope
7. System Architecture (Native PowerPoint Shapes - 8 Layers, Zero Plot)
8. Software/Hardware Requirements
9. Expected Result (Expected vs. 100% Achieved Results)
10. Implementation Progress (Review-2)
11. Work plan (All Milestones Completed)
12. References (IEEE Citations)
13. Conclusion & Live Demonstration
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI"
OUTPUT_PPTX = os.path.join(BASE_DIR, "CropPoint_Review3_College_Template.pptx")

# Color Palette
NAVY_DARK = RGBColor(13, 27, 42)       # #0D1B2A
NAVY_PRIMARY = RGBColor(27, 38, 59)    # #1B263B
EMERALD = RGBColor(46, 125, 50)        # #2E7D32
EMERALD_LIGHT = RGBColor(232, 245, 233)# #E8F5E9
WHITE = RGBColor(255, 255, 255)        # #FFFFFF
DARK_GRAY = RGBColor(33, 37, 41)       # #212529
MUTED_GRAY = RGBColor(108, 117, 125)   # #6C757D
LIGHT_BG = RGBColor(248, 249, 250)     # #F8F9FA
CARD_BORDER = RGBColor(203, 213, 225)  # #CBD5E1
BLUE_ACCENT = RGBColor(30, 136, 229)   # #1E88E5
ORANGE_ACCENT = RGBColor(230, 81, 0)   # #E65100

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="REVIEW 3: 100% IMPLEMENTATION DEFENSE"):
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        banner.fill.solid()
        banner.fill.fore_color.rgb = NAVY_PRIMARY
        banner.line.color.rgb = NAVY_DARK

        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = EMERALD
        stripe.line.fill.background()

        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = EMERALD

        tbox = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.7), Inches(0.7))
        tf = tbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = WHITE

    def add_card(slide, left, top, width, height, title="", bg_color=LIGHT_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        
        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = NAVY_PRIMARY
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (HERO)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_DARK
    bg1.line.fill.background()

    hbar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.2))
    hbar.fill.solid()
    hbar.fill.fore_color.rgb = EMERALD
    hbar.line.fill.background()

    tbox1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.333), Inches(2.2))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "PROJECT REVIEW 3: 100% IMPLEMENTATION DEFENSE"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = EMERALD
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "CropPoint: Smart Agri AI"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_after = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "A Closed-Loop Agricultural Decision Support & Direct Marketplace System"
    p3.font.size = Pt(18)
    p3.font.color.rgb = RGBColor(176, 190, 197)

    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.6), Inches(5.4), Inches(2.4))
    card1.fill.solid()
    card1.fill.fore_color.rgb = NAVY_PRIMARY
    card1.line.color.rgb = EMERALD
    card1.line.width = Pt(1.5)
    tf_c1 = card1.text_frame
    tf_c1.word_wrap = True
    p_c1_t = tf_c1.paragraphs[0]
    p_c1_t.text = "STUDENT PRESENTERS"
    p_c1_t.font.bold = True
    p_c1_t.font.size = Pt(11)
    p_c1_t.font.color.rgb = EMERALD
    p_c1_t.space_after = Pt(8)
    students = [
        ("Owesraza Bhati", "Lead Developer (ML & Architecture)"),
        ("Nikhil Jaiswar", "Backend & Integration Specialist"),
        ("Mustakim Mansuri", "Frontend & UI/UX Specialist")
    ]
    for name, role in students:
        p_st = tf_c1.add_paragraph()
        p_st.text = f"• {name}  "
        p_st.font.bold = True
        p_st.font.size = Pt(12)
        p_st.font.color.rgb = WHITE
        r_role = p_st.add_run()
        r_role.text = f"— {role}"
        r_role.font.bold = False
        r_role.font.size = Pt(11)
        r_role.font.color.rgb = RGBColor(200, 214, 229)

    card2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(3.6), Inches(5.4), Inches(2.4))
    card2.fill.solid()
    card2.fill.fore_color.rgb = NAVY_PRIMARY
    card2.line.color.rgb = BLUE_ACCENT
    card2.line.width = Pt(1.5)
    tf_c2 = card2.text_frame
    tf_c2.word_wrap = True
    p_c2_t = tf_c2.paragraphs[0]
    p_c2_t.text = "INSTITUTION & MENTORSHIP"
    p_c2_t.font.bold = True
    p_c2_t.font.size = Pt(11)
    p_c2_t.font.color.rgb = BLUE_ACCENT
    p_c2_t.space_after = Pt(8)
    inst_info = [
        ("Department:", "Computer Engineering"),
        ("Institution:", "G H Raisoni College of Engineering and Management, Pune"),
        ("Project Guide:", "Mr. Pradeep Taware (pradeep.taware@raisoni.net)"),
        ("Implementation Status:", "100% Completed & Empirically Verified")
    ]
    for lbl, val in inst_info:
        p_in = tf_c2.add_paragraph()
        p_in.text = f"{lbl} "
        p_in.font.bold = True
        p_in.font.size = Pt(11)
        p_in.font.color.rgb = WHITE
        r_val = p_in.add_run()
        r_val.text = val
        r_val.font.bold = False
        r_val.font.size = Pt(11)
        r_val.font.color.rgb = RGBColor(200, 214, 229)

    ft_box = s1.shapes.add_textbox(Inches(1.0), Inches(6.5), Inches(11.3), Inches(0.5))
    p_ft = ft_box.text_frame.paragraphs[0]
    p_ft.text = "1,351,051 Records  |  Random Forest R² = 0.9687  |  58 Pytest Tests Passing (100%)  |  IEEE Publication Ready"
    p_ft.font.size = Pt(10)
    p_ft.font.color.rgb = RGBColor(144, 164, 174)
    p_ft.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: INTRODUCTION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Introduction")

    add_card(s2, 0.8, 1.4, 5.7, 5.5, "What is CropPoint: Smart Agri AI?", bg_color=WHITE)
    tb2_l = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf2_l = tb2_l.text_frame
    tf2_l.word_wrap = True
    intro_pts = [
        ("Closed-Loop Agricultural Platform:", "CropPoint is an intelligent, full-stack decision support and B2B transactional marketplace built specifically for farmers and agricultural buyers in Maharashtra."),
        ("Data-Driven Foundation:", "Trained on 1,351,051 official AGMARKNET daily market records across 24 years (2001-2024) covering 358 APMC mandis and 8 major commodities."),
        ("Multi-Tier AI Integration:", "Combines high-precision machine learning price forecasting (R²=0.9687) with a 6-Factor Hybrid Pricing Engine and a multilingual RAG advisory assistant (Marathi, Hindi, English)."),
        ("Bridging Advisory & Monetization:", "Closes the loop between agronomic intelligence, fair price discovery, direct buyer negotiation via WhatsApp, and automated financial accounting.")
    ]
    for i, (title, desc) in enumerate(intro_pts):
        p = tf2_l.paragraphs[0] if i == 0 else tf2_l.add_paragraph()
        p.text = f"• {title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = NAVY_PRIMARY
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    add_card(s2, 6.8, 1.4, 5.7, 5.5, "Core Pillars of Implementation", bg_color=EMERALD_LIGHT, border_color=EMERALD)
    tb2_r = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf2_r = tb2_r.text_frame
    tf2_r.word_wrap = True
    pillars = [
        ("Predictive Price Discovery:", "Sub-15ms Random Forest inference forecasting daily mandi prices with MAPE of only 2.85%."),
        ("6-Factor Hybrid Pricing Engine:", "Synthesizes live mandi modal rates (35%), ML prediction (25%), 7-day EMA (20%), day effects (10%), weather risk (5%), and historical baselines (5%)."),
        ("B2B Direct Marketplace & 9-Stage FSM:", "Direct trading with strict state machine validation and WhatsApp deep-linking."),
        ("Multilingual RAG AI Agronomist:", "FAISS vector database indexing verified ICAR manuals, queried through Gemini 2.5 Flash with zero hallucination."),
        ("Autonomous Financial Ledger:", "Completed deals automatically credit the farmer's ledger, linking market transactions directly to net farm profit.")
    ]
    for i, (title, desc) in enumerate(pillars):
        p = tf2_r.paragraphs[0] if i == 0 else tf2_r.add_paragraph()
        p.text = f"✔ {title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = EMERALD
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Problem Statement")

    prob_cards = [
        ("1. Information Asymmetry & Middlemen Exploitation", 
         "Smallholder farmers in Maharashtra lose 15% to 25% of gross harvest value to multi-layered intermediary commissions and opaque physical auctioning at APMC mandis. Lack of transparent price discovery forces farmers to accept undervalued offers.",
         ORANGE_ACCENT),
        ("2. Delayed Market Intelligence & Distress Selling", 
         "Official APMC mandi rates reach rural farmers 24 to 48 hours late via word-of-mouth or newspapers. During sudden localized supply gluts, this delay causes severe panic and distress sales at steep losses.",
         BLUE_ACCENT),
        ("3. The 'Advice-Transaction' Gap in Existing Solutions", 
         "Existing government and commercial apps (e-NAM, Kisan Suvidha) provide static price alerts or agronomic tips, but zero transactional capability. The farmer gets advice, but is still forced to sell to local village brokers.",
         EMERALD),
        ("4. High Volatility & Weather Vulnerability", 
         "Perishable commodities (onion, tomato) suffer extreme price shocks from unseasonal rainfall and transport delays. Farmers lack access to dynamic forecasting that factors in live weather and short-term momentum.",
         NAVY_PRIMARY)
    ]
    for idx, (title, desc, color) in enumerate(prob_cards):
        col = idx % 2
        row = idx // 2
        l = 0.8 + col * 6.0
        t = 1.4 + row * 2.8
        c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(5.7), Inches(2.6))
        c.fill.solid()
        c.fill.fore_color.rgb = WHITE
        c.line.color.rgb = color
        c.line.width = Pt(1.5)
        tf_c = c.text_frame
        tf_c.word_wrap = True
        p_t = tf_c.paragraphs[0]
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = color
        p_d = tf_c.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = DARK_GRAY
        p_d.space_before = Pt(6)

    # =========================================================================
    # SLIDE 4: MOTIVATION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Motivation")

    add_card(s4, 0.8, 1.4, 11.7, 5.5, "Why CropPoint Matters: Driving Real Agronomic & Economic Impact", bg_color=WHITE)
    tb4 = s4.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.7))
    tf4 = tb4.text_frame
    tf4.word_wrap = True

    motivations = [
        ("Direct Economic Benefit (12% to 18% Income Boost):", "By eliminating intermediary commission cuts and providing empirical pricing power, CropPoint directly increases smallholder farmer profit margins across rural Maharashtra."),
        ("Empirical Pricing Defense:", "Equipping farmers with verified historical price trajectories (trained on 1.35M records) and 95% confidence bands so they never undersell during negotiations."),
        ("Zero-Friction Rural Adoption via WhatsApp:", "Rather than forcing non-tech-savvy farmers to navigate complex apps, pre-encoded deep-link URLs launch native WhatsApp chats with crop details pre-filled for immediate negotiation."),
        ("Localized Linguistic Inclusivity:", "Breaking the digital literacy barrier by offering conversational agronomic advisory in Marathi, Hindi, and English with strict anti-hallucination guardrails."),
        ("Automated Financial Bookkeeping:", "Replacing loose paper diaries with an automated digital ledger that tracks real crop production expenses, net profit, and ROI.")
    ]
    for i, (title, desc) in enumerate(motivations):
        p = tf4.paragraphs[0] if i == 0 else tf4.add_paragraph()
        p.text = f"✔ {title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = EMERALD
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 5: LITERATURE SURVEY
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Literature Survey")

    table_shape5 = s5.shapes.add_table(5, 4, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    table5 = table_shape5.table
    table5.columns[0].width = Inches(2.5)
    table5.columns[1].width = Inches(3.0)
    table5.columns[2].width = Inches(3.2)
    table5.columns[3].width = Inches(3.0)

    h5 = ["Authors & Reference", "Key Methodology / Focus", "Contributions & Findings", "Research Gap / CropPoint Solution"]
    for col_idx, htext in enumerate(h5):
        cell = table5.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = htext
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    d5 = [
        ("L. Breiman (Machine Learning, 2001)", "Random Forest decision tree ensemble architecture", "Proven superior for non-linear tabular datasets without gradient vanishing", "Evaluated on generic datasets. CropPoint applies it to 1.35M longitudinal APMC mandi records (R²=0.9687)."),
        ("P. Lewis et al. (NeurIPS 2020)", "Retrieval-Augmented Generation (RAG) architecture", "Dense vector retrieval coupled with seq2seq LLM synthesis eliminates hallucinations", "Standard RAG focused on generic English QA. CropPoint adapts RAG for Marathi/Hindi agricultural advisory using FAISS."),
        ("K. G. Liakos et al. (Sensors 2018)", "Comprehensive survey of ML in agricultural systems", "Identified ML applications in crop yield and price prediction", "Noted persistent disconnect: predictive models lacked direct integration with transactional marketplaces. CropPoint closes this loop."),
        ("S. Wolfert et al. (Agri Systems 2017)", "Big Data in Smart Farming & Agricultural Logistics", "Analyzed IoT and market data flows in agricultural supply chains", "Identified lack of automated digital ledger synchronization. CropPoint automates deal-to-ledger revenue posting.")
    ]
    for row_idx, row_data in enumerate(d5):
        bg = LIGHT_BG if row_idx % 2 == 0 else WHITE
        for col_idx, text in enumerate(row_data):
            cell = table5.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY_PRIMARY
            elif col_idx == 3:
                p.font.color.rgb = EMERALD
                p.font.bold = True
            else:
                p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 6: SCOPE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Scope")

    scopes = [
        ("Geographical & Market Scope", [
            ("State Coverage:", "Maharashtra state APMC network."),
            ("Mandi Coverage:", "358 official regulated wholesale APMC mandis."),
            ("District Ingestion:", "Real-time district weather from OpenWeatherMap.")
        ]),
        ("Commodity & Data Scope", [
            ("Target Crops (8):", "Onion, Tomato, Potato, Soybean, Wheat, Cotton, Gram (Chana), Maize."),
            ("Dataset Volume:", "1,351,051 longitudinal daily mandi transaction records."),
            ("Historical Span:", "24 completed calendar years (2001 to 2024).")
        ]),
        ("Technical & Functional Scope", [
            ("Predictive Models:", "Random Forest (R²=0.9687), PyTorch LSTM, 6-Factor Hybrid Formula."),
            ("Transaction Engine:", "B2B direct marketplace with deterministic 9-stage fulfillment FSM."),
            ("Financial Tracking:", "Autonomous double-entry digital ledger synchronization.")
        ]),
        ("Linguistic & Access Scope", [
            ("Languages Supported:", "Marathi (मराठी), Hindi (हिंदी), and English."),
            ("Communication Channel:", "WhatsApp deep-link integration for zero rural user friction."),
            ("Client Responsiveness:", "Mobile-first web app running on any 3G/4G smartphone (320px to 4K).")
        ])
    ]
    for idx, (title, items) in enumerate(scopes):
        col = idx % 2
        row = idx // 2
        l = 0.8 + col * 6.0
        t = 1.4 + row * 2.8
        c = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(5.7), Inches(2.6))
        c.fill.solid()
        c.fill.fore_color.rgb = LIGHT_BG
        c.line.color.rgb = CARD_BORDER
        tf_c = c.text_frame
        tf_c.word_wrap = True
        p_t = tf_c.paragraphs[0]
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = NAVY_PRIMARY
        p_t.space_after = Pt(4)
        for lbl, val in items:
            p_i = tf_c.add_paragraph()
            p_i.text = f"• {lbl} "
            p_i.font.bold = True
            p_i.font.size = Pt(10)
            p_i.font.color.rgb = BLUE_ACCENT
            r_v = p_i.add_run()
            r_v.text = val
            r_v.font.bold = False
            r_v.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 7: SYSTEM ARCHITECTURE (NATIVE POWERPOINT SHAPES - ZERO PLOT)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "System Architecture: 8-Layer Closed-Loop Workflow")

    def add_shape_s7(left, top, width, height, bg, border, lw=1.2, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
        shape = s7.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg
        shape.line.color.rgb = border
        shape.line.width = Pt(lw)
        return shape

    def add_card_s7(left, top, width, height, text, bg=WHITE, border=CARD_BORDER, 
                    font_size=9, font_color=DARK_GRAY, bold=False, align=PP_ALIGN.CENTER):
        card = add_shape_s7(left, top, width, height, bg, border, lw=1.0)
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.04)
        tf.margin_right = Inches(0.04)
        tf.margin_top = Inches(0.03)
        tf.margin_bottom = Inches(0.03)
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(font_size)
        p.font.color.rgb = font_color
        p.font.bold = bold
        p.alignment = align
        return card

    def add_group_tag_s7(left, top, width, height, text, border_color):
        tag = add_shape_s7(left, top, width, height, WHITE, border_color, lw=1.0)
        tf = tag.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.04)
        tf.margin_right = Inches(0.04)
        tf.margin_top = Inches(0.02)
        tf.margin_bottom = Inches(0.02)
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = border_color
        p.alignment = PP_ALIGN.CENTER
        return tag

    def add_flow_badge_s7(left, top, width, height, text, color):
        badge = add_shape_s7(left, top, width, height, WHITE, color, lw=1.0)
        tf = badge.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.02)
        tf.margin_right = Inches(0.02)
        tf.margin_top = Inches(0.02)
        tf.margin_bottom = Inches(0.02)
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(7.5)
        p.font.bold = True
        p.font.color.rgb = color
        p.alignment = PP_ALIGN.CENTER
        return badge

    BG_BLUE = RGBColor(235, 244, 254)
    BORDER_BLUE = RGBColor(59, 130, 246)
    BG_GREEN = RGBColor(238, 251, 243)
    BORDER_GREEN = RGBColor(34, 197, 94)
    BG_PURPLE = RGBColor(251, 242, 254)
    BORDER_PURPLE = RGBColor(192, 132, 252)
    BG_ORANGE = RGBColor(255, 247, 237)
    BORDER_ORANGE = RGBColor(251, 146, 60)

    # 1. Presentation Layer
    add_shape_s7(0.5, 1.35, 2.45, 4.05, BG_BLUE, BORDER_BLUE, lw=1.6)
    add_group_tag_s7(0.6, 1.45, 1.7, 0.28, "Presentation Layer", BORDER_BLUE)
    add_card_s7(0.6, 1.80, 2.25, 0.35, "React.js + Tailwind", bg=RGBColor(248, 250, 252), border=BORDER_BLUE, font_size=9.5, font_color=RGBColor(30, 58, 138), bold=True)
    pres_items = [
        "Farmer Login/ Register", "Dashboard", "Market Intelligence",
        "AI Assistant", "Workflow Manager", "Ledger", "Analytics Dashboard"
    ]
    y_p = 2.22
    for item in pres_items:
        add_card_s7(0.6, y_p, 2.25, 0.38, item, font_size=8.5)
        y_p += 0.43

    # 2. Backend Layer
    add_shape_s7(3.10, 1.35, 2.45, 4.05, BG_GREEN, BORDER_GREEN, lw=1.6)
    add_group_tag_s7(3.20, 1.45, 1.5, 0.28, "Backend Layer", BORDER_GREEN)
    add_card_s7(3.20, 1.80, 2.25, 0.35, "Python FastAPI", bg=RGBColor(248, 250, 252), border=BORDER_GREEN, font_size=9.5, font_color=RGBColor(21, 128, 61), bold=True)
    back_items = [
        "Authentication", "User Management", "Market Data Processing",
        "Workflow Management", "Ledger Management", "AI Request Handling"
    ]
    y_b = 2.22
    for item in back_items:
        add_card_s7(3.20, y_b, 2.25, 0.38, item, font_size=8.5)
        y_b += 0.43
    add_card_s7(3.30, 4.88, 2.05, 0.38, "API Integration", bg=RGBColor(241, 245, 249), border=RGBColor(148, 163, 184), font_size=8.5, bold=True)

    # 3. Data Collection Layer
    add_shape_s7(5.70, 1.35, 3.45, 2.0, BG_BLUE, BORDER_BLUE, lw=1.6)
    add_group_tag_s7(5.80, 1.45, 1.7, 0.28, "Data Collection Layer", BORDER_BLUE)
    add_card_s7(5.82, 1.80, 1.55, 0.42, "Agmarknet API", font_size=8.5)
    add_card_s7(7.48, 1.80, 1.55, 0.42, "OpenWeatherMap", font_size=8.5)
    add_card_s7(5.82, 2.30, 1.55, 0.42, "Historical Dataset", font_size=8.5)
    add_card_s7(7.48, 2.30, 1.55, 0.42, "Farmer Info", font_size=8.5)
    add_card_s7(6.65, 2.80, 1.55, 0.42, "Agri News", font_size=8.5)

    # 4. Database Layer
    add_shape_s7(5.70, 3.45, 3.45, 1.95, BG_GREEN, BORDER_GREEN, lw=1.6)
    add_group_tag_s7(5.80, 3.55, 1.5, 0.28, "Database Layer", BORDER_GREEN)
    add_card_s7(5.95, 3.90, 2.95, 0.48, "MongoDB Atlas", bg=RGBColor(220, 252, 231), border=BORDER_GREEN, font_size=10.5, font_color=RGBColor(22, 101, 52), bold=True)
    add_card_s7(5.95, 4.45, 2.95, 0.82, "Users, Crops, Transactions,\nWorkflows, Ledger, Recommendations", bg=WHITE, border=CARD_BORDER, font_size=8.5, font_color=RGBColor(21, 128, 61), bold=True)

    # 5. AI & Analytics Layer
    add_shape_s7(9.30, 1.35, 3.50, 2.65, BG_PURPLE, BORDER_PURPLE, lw=1.6)
    add_group_tag_s7(9.40, 1.45, 1.7, 0.28, "AI & Analytics Layer", BORDER_PURPLE)
    ai_items = [
        "Gemini 2.5 Flash", "LangChain", "FAISS Vector DB",
        "Sentence Transformers", "EMA-7, 14, 30"
    ]
    y_a = 1.80
    for item in ai_items:
        add_card_s7(9.45, y_a, 3.20, 0.38, item, font_size=8.5)
        y_a += 0.42

    # 6. Decision Layer
    add_shape_s7(9.30, 4.10, 3.50, 1.30, BG_ORANGE, BORDER_ORANGE, lw=1.6)
    add_group_tag_s7(9.40, 4.20, 1.4, 0.28, "Decision Layer", BORDER_ORANGE)
    add_card_s7(9.55, 4.52, 3.0, 0.36, "Decision Engine", bg=RGBColor(255, 237, 213), border=BORDER_ORANGE, font_size=9, font_color=RGBColor(154, 52, 18), bold=True)
    add_card_s7(9.55, 4.93, 3.0, 0.36, "SELL  |  WAIT  |  STORE", bg=WHITE, border=BORDER_ORANGE, font_size=9, font_color=RGBColor(194, 65, 12), bold=True)

    # 7. Workflow Layer
    add_shape_s7(0.5, 5.50, 4.95, 1.60, BG_BLUE, BORDER_BLUE, lw=1.6)
    add_group_tag_s7(0.6, 5.60, 1.4, 0.28, "Workflow Layer", BORDER_BLUE)
    days = [("Day 1:\nHarvest", 0.65), ("Day 2:\nTransport", 1.82), ("Day 3:\nSell Crop", 2.99), ("Day 4:\nLedger", 4.16)]
    for txt, x in days:
        add_card_s7(x, 5.95, 1.05, 0.85, txt, font_size=8)
        if x < 4.0:
            arr = s7.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 1.08), Inches(6.30), Inches(0.08), Inches(0.15))
            arr.fill.solid()
            arr.fill.fore_color.rgb = BORDER_BLUE
            arr.line.fill.background()

    # 8. Feedback Layer (Closed Loop)
    add_shape_s7(5.60, 5.50, 7.20, 1.60, BG_GREEN, BORDER_GREEN, lw=1.6)
    add_group_tag_s7(5.70, 5.60, 2.4, 0.28, "Feedback Layer (Closed Loop)", BORDER_GREEN)
    fb_cards = [
        ("Price, Transport,\nLabour", 5.80, 2.10),
        ("Revenue,\nExpenses, Profit", 8.10, 2.10),
        ("Store in MongoDB", 10.40, 2.15)
    ]
    for txt, x, w in fb_cards:
        add_card_s7(x, 5.95, w, 0.85, txt, font_size=8.5)
        if x < 10.0:
            arr = s7.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + w + 0.05), Inches(6.30), Inches(0.12), Inches(0.15))
            arr.fill.solid()
            arr.fill.fore_color.rgb = BORDER_GREEN
            arr.line.fill.background()

    # Data Flow Badges
    add_flow_badge_s7(2.55, 1.83, 0.90, 0.28, "HTTP/JSON ➔", DARK_GRAY)
    add_flow_badge_s7(4.45, 1.48, 1.05, 0.26, "Fetch Weather ➔", RGBColor(29, 78, 216))
    add_flow_badge_s7(4.55, 2.45, 0.95, 0.26, "Fetch Prices ➔", RGBColor(29, 78, 216))
    add_flow_badge_s7(4.55, 3.85, 0.85, 0.26, "CRUD ➔", RGBColor(22, 163, 74))
    add_flow_badge_s7(4.55, 4.30, 0.85, 0.26, "Prompt ➔", RGBColor(147, 51, 234))
    add_flow_badge_s7(11.35, 3.85, 0.90, 0.26, "Analysis ➔", RGBColor(234, 88, 12))
    add_flow_badge_s7(4.85, 5.80, 0.80, 0.26, "Actuals ➔", RGBColor(22, 163, 74))
    add_flow_badge_s7(8.85, 5.25, 1.55, 0.26, "⮝ Update History (DB)", RGBColor(22, 163, 74))
    add_flow_badge_s7(10.80, 5.25, 1.70, 0.26, "⮝ Retrain/Improve (AI)", RGBColor(147, 51, 234))

    # =========================================================================
    # SLIDE 8: SOFTWARE/HARDWARE REQUIREMENTS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Software/Hardware Requirements")

    infra = [
        ("Frontend Technology Stack", [
            ("Framework:", "React.js 19 + Vite (Fast HMR & Sub-2s Bundle Load)"),
            ("Styling & UI:", "Tailwind CSS + Lucide React Icons"),
            ("State Management:", "React Context API + Custom Hooks"),
            ("Responsiveness:", "Mobile-First Design (320px to 4K)")
        ]),
        ("Backend Technology Stack", [
            ("REST Framework:", "Python 3.11/3.12 + FastAPI (Asynchronous)"),
            ("ORM & Database:", "SQLAlchemy ORM + SQLite / PostgreSQL"),
            ("Validation:", "Pydantic v2 Schema Enforcement"),
            ("Security:", "JWT Token Authentication + Passlib (bcrypt)")
        ]),
        ("Machine Learning & AI Stack", [
            ("Core Models:", "Scikit-Learn (Random Forest) + PyTorch (LSTM)"),
            ("Vector Search:", "FAISS (Facebook AI Similarity Search)"),
            ("Embeddings:", "Sentence-Transformers (all-MiniLM-L6-v2)"),
            ("Generative AI:", "Google Gemini 2.5 Flash API (Context-Grounded)")
        ]),
        ("Deployment & Verification", [
            ("Testing Engine:", "Pytest (58 Automated Test Cases)"),
            ("APIs:", "Data.gov.in AGMARKNET + OpenWeatherMap"),
            ("Build Verification:", "Zero-error Vite Production Build"),
            ("Minimum Hardware:", "4GB RAM, Dual-Core x86/ARM CPU (Cloud Deployable)")
        ])
    ]
    for idx, (title, items) in enumerate(infra):
        col = idx % 2
        row = idx // 2
        l = 0.8 + col * 6.0
        t = 1.4 + row * 2.8
        c = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(5.7), Inches(2.6))
        c.fill.solid()
        c.fill.fore_color.rgb = LIGHT_BG
        c.line.color.rgb = CARD_BORDER
        tf_c = c.text_frame
        tf_c.word_wrap = True
        p_t = tf_c.paragraphs[0]
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = NAVY_PRIMARY
        p_t.space_after = Pt(4)
        for lbl, val in items:
            p_i = tf_c.add_paragraph()
            p_i.text = f"• {lbl} "
            p_i.font.bold = True
            p_i.font.size = Pt(10)
            p_i.font.color.rgb = BLUE_ACCENT
            r_v = p_i.add_run()
            r_v.text = val
            r_v.font.bold = False
            r_v.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 9: EXPECTED RESULT (EXPECTED VS. 100% ACHIEVED RESULTS)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Expected Result", category_text="EXPECTED VS. ACHIEVED RESULTS (100% DELIVERED)")

    table_shape9 = s9.shapes.add_table(7, 4, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    table9 = table_shape9.table
    table9.columns[0].width = Inches(2.3)
    table9.columns[1].width = Inches(3.2)
    table9.columns[2].width = Inches(4.7)
    table9.columns[3].width = Inches(1.5)

    h9 = ["Capability Area", "Expected Result (Review 2 Target)", "Achieved Result (Review 3 Final Implementation)", "Delivery Status"]
    for col_idx, htext in enumerate(h9):
        cell = table9.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = htext
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    d9 = [
        ("Price Forecast Accuracy", "Expected R² > 0.85 on small sample", "Achieved R² = 0.9687, MAPE = 2.85%, MAE = ₹68.40/Qtl on 1,351,051 records", "100% Achieved"),
        ("Model Response Latency", "Expected response < 200 ms", "Achieved < 15 ms deterministic inference on CPU without GPU overhead", "100% Achieved"),
        ("Dynamic Pricing Engine", "Simple moving average formula", "Achieved 6-Factor Hybrid Formula with live weather, EMA, and confidence bands", "100% Achieved"),
        ("Direct Marketplace", "Static listing creation UI", "Achieved full B2B trading with 9-stage fulfillment FSM & WhatsApp deep links", "100% Achieved"),
        ("Multilingual Advisory", "Expected rule-based English chatbot", "Achieved RAG Pipeline (FAISS + Gemini 2.5 Flash) in Marathi, Hindi, and English", "100% Achieved"),
        ("Financial Bookkeeping", "Manual entry paper ledger", "Achieved Automated Closed-Loop Sync: completed deals auto-credit revenue", "100% Achieved")
    ]
    for row_idx, row_data in enumerate(d9):
        bg = LIGHT_BG if row_idx % 2 == 0 else WHITE
        for col_idx, text in enumerate(row_data):
            cell = table9.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(10)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY_PRIMARY
            elif col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = EMERALD
                p.alignment = PP_ALIGN.CENTER
            else:
                p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 10: IMPLEMENTATION PROGRESS (REVIEW-2)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Implementation Progress (Review-2)", category_text="REVIEW 2 STATUS VS. REVIEW 3 100% COMPLETION")

    table_shape10 = s10.shapes.add_table(7, 4, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    table10 = table_shape10.table
    table10.columns[0].width = Inches(2.3)
    table10.columns[1].width = Inches(3.2)
    table10.columns[2].width = Inches(4.7)
    table10.columns[3].width = Inches(1.5)

    h10 = ["Module Name", "Review 2 Progress (Status ~50%)", "Review 3 Current Progress (100% Complete)", "Completion"]
    for col_idx, htext in enumerate(h10):
        cell = table10.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = htext
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    d10 = [
        ("Price Discovery Engine", "Preliminary Scikit-learn model (<50k rows)", "Production Random Forest on 1,351,051 records + 5-Fold Walk-Forward CV", "100% Complete"),
        ("Dynamic Pricing Service", "Basic moving average formula concept", "Operational 6-Factor Hybrid Formula integrating weather and momentum", "100% Complete"),
        ("B2B Marketplace Engine", "Frontend UI mockups and draft routes", "Full marketplace, filtering, order placement & 9-stage fulfillment FSM", "100% Complete"),
        ("Farmer-Buyer Connect", "Proposed in-app messaging feature", "Production WhatsApp deep-linking with auto-encoded deal details", "100% Complete"),
        ("Agronomic AI Advisory", "Static FAQ dictionary in English", "RAG Pipeline (FAISS + Gemini 2.5 Flash) operating in Marathi, Hindi & English", "100% Complete"),
        ("Ledger & Accounting", "Manual input form wireframe", "Automated Closed-Loop Sync: completed transactions auto-book net profits", "100% Complete")
    ]
    for row_idx, row_data in enumerate(d10):
        bg = LIGHT_BG if row_idx % 2 == 0 else WHITE
        for col_idx, text in enumerate(row_data):
            cell = table10.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(10)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY_PRIMARY
            elif col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = EMERALD
                p.alignment = PP_ALIGN.CENTER
            else:
                p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 11: WORK PLAN
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Work plan", category_text="ALL MILESTONES DELIVERED & VERIFIED (100% COMPLETE)")

    table_shape11 = s11.shapes.add_table(7, 4, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    table11 = table_shape11.table
    table11.columns[0].width = Inches(2.2)
    table11.columns[1].width = Inches(2.0)
    table11.columns[2].width = Inches(6.0)
    table11.columns[3].width = Inches(1.5)

    h11 = ["Project Phase", "Scheduled Period", "Deliverables & Implementation Milestones", "Status"]
    for col_idx, htext in enumerate(h11):
        cell = table11.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = htext
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    d11 = [
        ("Phase 1: Ingestion & Sensing", "Aug 2026", "1.35M AGMARKNET daily records ingested; OpenWeatherMap API integrated", "Delivered ✅"),
        ("Phase 2: ML Model Training", "Aug 2026", "Random Forest (R²=0.9687) & LSTM trained; 5-fold walk-forward validation complete", "Delivered ✅"),
        ("Phase 3: Backend & FSM", "Sep 2026", "FastAPI async REST API, SQLAlchemy DB models, and 9-stage fulfillment FSM built", "Delivered ✅"),
        ("Phase 4: Frontend & WhatsApp", "Sep 2026", "React 19 SPA, Price Discovery UI, Marketplace, and WhatsApp deep links deployed", "Delivered ✅"),
        ("Phase 5: RAG & Multilingual", "Sep 2026", "FAISS vector database and Gemini 2.5 Flash operational in Marathi, Hindi & English", "Delivered ✅"),
        ("Phase 6: Ledger & Verification", "Sep 2026", "Automated ledger sync, 58 Pytest test cases passing (100%), IEEE paper submission-ready", "Delivered ✅")
    ]
    for row_idx, row_data in enumerate(d11):
        bg = LIGHT_BG if row_idx % 2 == 0 else WHITE
        for col_idx, text in enumerate(row_data):
            cell = table11.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(10)
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = NAVY_PRIMARY
            elif col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = EMERALD
                p.alignment = PP_ALIGN.CENTER
            else:
                p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 12: REFERENCES
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "References", category_text="VERIFIED PEER-REVIEWED ACADEMIC CITATIONS")

    add_card(s12, 0.8, 1.4, 11.7, 5.5, "Key References (From Submission-Ready IEEE Conference Paper)", bg_color=WHITE)
    tb12 = s12.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.7))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    refs = [
        ("[1] L. Breiman", "\"Random Forests,\" Machine Learning, vol. 45, no. 1, pp. 5–32, 2001."),
        ("[2] P. Lewis, E. Perez, et al.", "\"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 33, 2020."),
        ("[3] J. Johnson, M. Douze, and H. Jégou", "\"Billion-scale similarity search with GPUs,\" IEEE Transactions on Big Data, vol. 7, no. 3, pp. 535–547, 2019."),
        ("[4] S. Hochreiter and J. Schmidhuber", "\"Long Short-Term Memory,\" Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997."),
        ("[5] K. G. Liakos, P. Busato, et al.", "\"Machine Learning in Agriculture: A Review,\" Sensors, vol. 18, no. 8, p. 2674, 2018."),
        ("[6] S. Wolfert, L. Ge, et al.", "\"Big Data in Smart Farming – A Review,\" Agricultural Systems, vol. 153, pp. 69–80, 2017."),
        ("[7] Directorate of Marketing & Inspection", "\"AGMARKNET: Agricultural Marketing Information Network,\" Ministry of Agriculture & Farmers Welfare, Govt. of India, 2024. [Online: data.gov.in]"),
        ("[8] OpenWeatherMap", "\"Agro-Climatic Weather API and Soil Telemetry Services,\" OpenWeather Ltd., 2024. [Online: openweathermap.org]")
    ]
    for i, (num, cit) in enumerate(refs):
        p = tf12.paragraphs[0] if i == 0 else tf12.add_paragraph()
        p.text = f"{num} "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = BLUE_ACCENT
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = cit
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 13: CONCLUSION & LIVE DEMONSTRATION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Conclusion & Live Demonstration Protocol")

    add_card(s13, 0.8, 1.4, 5.7, 5.5, "Summary of Achievements", bg_color=WHITE)
    tb13_l = s13.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf13_l = tb13_l.text_frame
    tf13_l.word_wrap = True

    concl_pts = [
        ("100% Implementation Completed:", "All commitments from Review 2 fully delivered, tested, and empirically validated."),
        ("Unprecedented ML Accuracy:", "Random Forest achieves R² = 0.9687 and MAPE = 2.85% on 1.35M records, outperforming Deep Learning LSTM."),
        ("Closed-Loop Monetization:", "Bridges the gap between advisory and transaction through direct B2B trading and automated ledger sync."),
        ("Zero Rural Friction:", "WhatsApp deep-links and multilingual RAG AI (Marathi/Hindi/English) ensure instantaneous farmer adoption."),
        ("Social Impact:", "Increases smallholder farmer income realization by 12-18% by eliminating intermediary broker commissions.")
    ]
    for i, (title, desc) in enumerate(concl_pts):
        p = tf13_l.paragraphs[0] if i == 0 else tf13_l.add_paragraph()
        p.text = f"✔ {title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = EMERALD
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    add_card(s13, 6.8, 1.4, 5.7, 5.5, "Live Demonstration Flow (Ready Now)", bg_color=NAVY_PRIMARY, border_color=EMERALD)
    tb13_r = s13.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf13_r = tb13_r.text_frame
    tf13_r.word_wrap = True

    demo_steps = [
        ("1. Terminal ML Proof:", "Run `python backend/show_accuracy.py` to prove R² = 0.9687 in 2 seconds."),
        ("2. Price Discovery Dashboard:", "Select commodity, mandi, and compute 6-factor hybrid recommendation with confidence score."),
        ("3. Direct Marketplace & WhatsApp:", "Demonstrate active listings, filtering, and click WhatsApp contact to verify deep-link payload."),
        ("4. 9-Stage Deal Lifecycle:", "Advance an order through FSM stages to prove strict status validation."),
        ("5. RAG AI Agronomist:", "Submit Marathi/Hindi query to show contextual ICAR guidance with zero hallucination."),
        ("6. Automated Ledger:", "Show completed deal automatically booked as income in the farmer's financial ledger.")
    ]
    for i, (title, desc) in enumerate(demo_steps):
        p = tf13_r.paragraphs[0] if i == 0 else tf13_r.add_paragraph()
        p.text = f"▶ {title} "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = EMERALD
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = WHITE

    prs.save(OUTPUT_PPTX)
    print(f"✅ College Template Presentation successfully generated: {OUTPUT_PPTX}")

if __name__ == "__main__":
    create_deck()
