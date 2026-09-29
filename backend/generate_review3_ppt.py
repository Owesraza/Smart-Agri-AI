#!/usr/bin/env python3
"""
CropPoint (Smart Agri AI) — Review 3 Final Presentation Generator
Generates a complete, high-quality, professional 18-slide PowerPoint (.pptx)
proving 100% Implementation and Project Completion.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Paths
BASE_DIR = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI"
FIG_DIR = os.path.join(BASE_DIR, "figures")
OUTPUT_PPTX = os.path.join(BASE_DIR, "CropPoint_Review3_100_Percent_Completion_Presentation.pptx")

# Color Palette
NAVY_DARK = RGBColor(13, 27, 42)       # #0D1B2A
NAVY_PRIMARY = RGBColor(27, 38, 59)    # #1B263B
EMERALD = RGBColor(46, 125, 50)        # #2E7D32
EMERALD_LIGHT = RGBColor(232, 245, 233)# #E8F5E9
WHITE = RGBColor(255, 255, 255)        # #FFFFFF
DARK_GRAY = RGBColor(33, 37, 41)       # #212529
MUTED_GRAY = RGBColor(108, 117, 125)   # #6C757D
LIGHT_BG = RGBColor(248, 249, 250)     # #F8F9FA
CARD_BORDER = RGBColor(222, 226, 230)  # #DEE2E6
BLUE_ACCENT = RGBColor(30, 136, 229)   # #1E88E5
ORANGE_ACCENT = RGBColor(230, 81, 0)   # #E65100

def create_deck():
    prs = Presentation()
    # 16:9 widescreen slides
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="REVIEW 3: 100% IMPLEMENTATION DEFENSE"):
        # Top banner shape
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        banner.fill.solid()
        banner.fill.fore_color.rgb = NAVY_PRIMARY
        banner.line.color.rgb = NAVY_DARK

        # Accent stripe
        stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = EMERALD
        stripe.line.fill.background()

        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = EMERALD

        # Title
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

    # Emerald header bar
    hbar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.2))
    hbar.fill.solid()
    hbar.fill.fore_color.rgb = EMERALD
    hbar.line.fill.background()

    # Badge: 100% COMPLETE
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.9), Inches(4.5), Inches(0.5))
    badge.fill.solid()
    badge.fill.fore_color.rgb = EMERALD
    badge.line.fill.background()
    bp = badge.text_frame.paragraphs[0]
    bp.text = "PROJECT REVIEW 3: 100% IMPLEMENTATION DEFENSE"
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = WHITE
    bp.alignment = PP_ALIGN.CENTER

    # Title
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(1.8))
    t_frame = t_box.text_frame
    t_frame.word_wrap = True
    p1 = t_frame.paragraphs[0]
    p1.text = "CropPoint: Smart Agri AI"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    p2 = t_frame.add_paragraph()
    p2.text = "A Closed-Loop Agricultural Marketplace & Decision Support System Integrating Multi-Factor Random Forest Price Forecasting, Multilingual FAISS RAG, and Automated Ledger Synchronization"
    p2.font.size = Pt(17)
    p2.font.color.rgb = RGBColor(200, 225, 240)
    p2.space_before = Pt(8)

    # Info card 1: Authors
    acard = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.8), Inches(5.3), Inches(2.8))
    acard.fill.solid()
    acard.fill.fore_color.rgb = NAVY_PRIMARY
    acard.line.color.rgb = EMERALD
    atf = acard.text_frame
    atf.word_wrap = True
    ap0 = atf.paragraphs[0]
    ap0.text = "STUDENT PROJECT TEAM"
    ap0.font.size = Pt(12)
    ap0.font.bold = True
    ap0.font.color.rgb = EMERALD

    authors = [
        "• Owesraza Bhati  (ansarbhati92@gmail.com)",
        "• Nikhil Jaiswar   (nikhiljaiswar642@gmail.com)",
        "• Mustakim Mansuri (mjmansuri786313@gmail.com)"
    ]
    for a in authors:
        p = atf.add_paragraph()
        p.text = a
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.space_before = Pt(6)

    # Info card 2: Guide & Institution
    gcard = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.8), Inches(5.5), Inches(2.8))
    gcard.fill.solid()
    gcard.fill.fore_color.rgb = NAVY_PRIMARY
    gcard.line.color.rgb = BLUE_ACCENT
    gtf = gcard.text_frame
    gtf.word_wrap = True
    gp0 = gtf.paragraphs[0]
    gp0.text = "PROJECT GUIDE & AFFILIATION"
    gp0.font.size = Pt(12)
    gp0.font.bold = True
    gp0.font.color.rgb = BLUE_ACCENT

    guide_info = [
        "Guide: Mr. Pradeep Taware (Assistant Professor)",
        "Email: pradeep.taware@raisoni.net",
        "Department of Computer Engineering",
        "G H Raisoni College of Engineering and Management",
        "Pune, Maharashtra, India (Academic Year 2025–2026)"
    ]
    for gi in guide_info:
        p = gtf.add_paragraph()
        p.text = gi
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.space_before = Pt(4)

    # Bottom metric bar
    bbar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(6.9), Inches(13.333), Inches(0.6))
    bbar.fill.solid()
    bbar.fill.fore_color.rgb = RGBColor(18, 30, 49)
    bbar.line.fill.background()
    bp = bbar.text_frame.paragraphs[0]
    bp.text = "1,351,051 APMC Records  |  Random Forest R²: 0.9687  |  MAPE: 2.85%  |  FAISS Trilingual RAG  |  68 Live Automated Tests (98.5%)"
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = RGBColor(165, 214, 167)
    bp.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Summary: The Disconnected Agri-Supply Chain")

    add_card(s2, 0.8, 1.4, 5.6, 5.5, "The Problem in Indian Smallholder Agriculture")
    tb2_left = s2.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.7))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True
    
    prob_bullets = [
        ("Middlemen Monopsony:", "Farmers lose 30–45% of produce value to local commission agents, aggregators, and spatial cartels."),
        ("Price Asymmetry:", "Farmers lack real-time local mandi spot rates, relying on outdated word-of-mouth quotes."),
        ("Perishable Risk & Logistics:", "Centroid-less logistics lead to post-harvest distress selling before produce spoils."),
        ("Manual & Fragmented Records:", "Zero integration between market deals and farm accounting; farmers cannot track true net profits."),
        ("Hallucinatory Generic Advice:", "Standard LLMs generate unverified advice without grounding in local soil and weather.")
    ]
    for i, (title, desc) in enumerate(prob_bullets):
        p = tf2_l.paragraphs[0] if i == 0 else tf2_l.add_paragraph()
        p.text = f"• {title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(198, 40, 40)
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    add_card(s2, 6.8, 1.4, 5.7, 5.5, "The CropPoint Closed-Loop Solution", bg_color=EMERALD_LIGHT, border_color=EMERALD)
    tb2_right = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.7))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True

    sol_bullets = [
        ("Direct Farmer-to-Buyer Marketplace:", "100% disintermediation; verified B2B trade between farmers and institutional buyers."),
        ("AI Smart Pricing Engine (96.87% R²):", "Random Forest trained on 1.35M APMC records blended with live spot rates and EMA."),
        ("Haversine Road Logistics:", "Automatic geodesic distance estimation and transparent freight rate calculation per quintal."),
        ("Automated Ledger Sync:", "Physical delivery automatically posts immutable income, expense, and net profit ledger entries."),
        ("Multilingual RAG Advisory:", "Sentence-BERT + FAISS IndexFlatIP + Gemini delivering verified guidance in English, Hindi, and Marathi.")
    ]
    for i, (title, desc) in enumerate(sol_bullets):
        p = tf2_r.paragraphs[0] if i == 0 else tf2_r.add_paragraph()
        p.text = f"✓ {title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = EMERALD
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 3: REVIEW 2 COMMITMENTS VS REVIEW 3 100% DELIVERY
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Review 2 Commitments vs. Review 3 100% Completion")

    # Full table of deliverables
    rows, cols = 8, 4
    t_shape = s3.shapes.add_table(rows, cols, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))
    table = t_shape.table
    table.columns[0].width = Inches(2.8)
    table.columns[1].width = Inches(3.6)
    table.columns[2].width = Inches(3.8)
    table.columns[3].width = Inches(1.5)

    headers = ["Functional Component", "Review 2 Scope / Promise", "Review 3 Implemented Status", "Completion"]
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    data = [
        ("ML Price Prediction", "Basic model on sample data", "Trained on 1,351,051 Maharashtra APMC records (R²=0.9687, MAPE=2.85%)", "100% DONE"),
        ("Smart Price Recommendation", "Raw model output display", "6-Factor Hybrid Formula (Mandi + ML + EMA + Week Avg + Weather + Hist)", "100% DONE"),
        ("Agricultural Advisory", "Generic chatbot interface", "RAG with Sentence-BERT, FAISS IndexFlatIP & Gemini (EN, HI, MR)", "100% DONE"),
        ("B2B Direct Marketplace", "Static listing mockup", "Real-time crop listings, purchase requests, counter-bidding & offers", "100% DONE"),
        ("Order Tracking FSM", "Single-status order table", "4-Stage Finite State Machine (Confirmed -> Dispatched -> Transit -> Delivered)", "100% DONE"),
        ("Digital Ledger Sync", "Manual ledger input only", "Automatic ledger entry creation & net profit accounting upon delivery", "100% DONE"),
        ("Live Weather Integration", "Static weather forecast", "Real-time OpenWeatherMap API integrated into pricing engine & advisory", "100% DONE")
    ]

    for row_idx, row_data in enumerate(data, 1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 1 else LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(11)
            p.font.color.rgb = DARK_GRAY
            if col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = EMERALD
                p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 4: COMPLETE CLOSED-LOOP WORKFLOW ARCHITECTURE
    # =========================================================================
    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE (NATIVE POWERPOINT SHAPES - 8 LAYERS)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "System Architecture: 8-Layer Closed-Loop Workflow")

    def add_shape_s4(left, top, width, height, bg, border, lw=1.2, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
        shape = s4.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg
        shape.line.color.rgb = border
        shape.line.width = Pt(lw)
        return shape

    def add_card_s4(left, top, width, height, text, bg=WHITE, border=CARD_BORDER, 
                    font_size=9, font_color=DARK_GRAY, bold=False, align=PP_ALIGN.CENTER):
        card = add_shape_s4(left, top, width, height, bg, border, lw=1.0)
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

    def add_group_tag_s4(left, top, width, height, text, border_color):
        tag = add_shape_s4(left, top, width, height, WHITE, border_color, lw=1.0)
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

    def add_flow_badge_s4(left, top, width, height, text, color):
        badge = add_shape_s4(left, top, width, height, WHITE, color, lw=1.0)
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
    add_shape_s4(0.5, 1.35, 2.45, 4.05, BG_BLUE, BORDER_BLUE, lw=1.6)
    add_group_tag_s4(0.6, 1.45, 1.7, 0.28, "Presentation Layer", BORDER_BLUE)
    add_card_s4(0.6, 1.80, 2.25, 0.35, "React.js + Tailwind", bg=RGBColor(248, 250, 252), border=BORDER_BLUE, font_size=9.5, font_color=RGBColor(30, 58, 138), bold=True)
    pres_items = [
        "Farmer Login/ Register", "Dashboard", "Market Intelligence",
        "AI Assistant", "Workflow Manager", "Ledger", "Analytics Dashboard"
    ]
    y_p = 2.22
    for item in pres_items:
        add_card_s4(0.6, y_p, 2.25, 0.38, item, font_size=8.5)
        y_p += 0.43

    # 2. Backend Layer
    add_shape_s4(3.10, 1.35, 2.45, 4.05, BG_GREEN, BORDER_GREEN, lw=1.6)
    add_group_tag_s4(3.20, 1.45, 1.5, 0.28, "Backend Layer", BORDER_GREEN)
    add_card_s4(3.20, 1.80, 2.25, 0.35, "Python FastAPI", bg=RGBColor(248, 250, 252), border=BORDER_GREEN, font_size=9.5, font_color=RGBColor(21, 128, 61), bold=True)
    back_items = [
        "Authentication", "User Management", "Market Data Processing",
        "Workflow Management", "Ledger Management", "AI Request Handling"
    ]
    y_b = 2.22
    for item in back_items:
        add_card_s4(3.20, y_b, 2.25, 0.38, item, font_size=8.5)
        y_b += 0.43
    add_card_s4(3.30, 4.88, 2.05, 0.38, "API Integration", bg=RGBColor(241, 245, 249), border=RGBColor(148, 163, 184), font_size=8.5, bold=True)

    # 3. Data Collection Layer
    add_shape_s4(5.70, 1.35, 3.45, 2.0, BG_BLUE, BORDER_BLUE, lw=1.6)
    add_group_tag_s4(5.80, 1.45, 1.7, 0.28, "Data Collection Layer", BORDER_BLUE)
    add_card_s4(5.82, 1.80, 1.55, 0.42, "Agmarknet API", font_size=8.5)
    add_card_s4(7.48, 1.80, 1.55, 0.42, "OpenWeatherMap", font_size=8.5)
    add_card_s4(5.82, 2.30, 1.55, 0.42, "Historical Dataset", font_size=8.5)
    add_card_s4(7.48, 2.30, 1.55, 0.42, "Farmer Info", font_size=8.5)
    add_card_s4(6.65, 2.80, 1.55, 0.42, "Agri News", font_size=8.5)

    # 4. Database Layer
    add_shape_s4(5.70, 3.45, 3.45, 1.95, BG_GREEN, BORDER_GREEN, lw=1.6)
    add_group_tag_s4(5.80, 3.55, 1.5, 0.28, "Database Layer", BORDER_GREEN)
    add_card_s4(5.95, 3.90, 2.95, 0.48, "MongoDB Atlas", bg=RGBColor(220, 252, 231), border=BORDER_GREEN, font_size=10.5, font_color=RGBColor(22, 101, 52), bold=True)
    add_card_s4(5.95, 4.45, 2.95, 0.82, "Users, Crops, Transactions,\nWorkflows, Ledger, Recommendations", bg=WHITE, border=CARD_BORDER, font_size=8.5, font_color=RGBColor(21, 128, 61), bold=True)

    # 5. AI & Analytics Layer
    add_shape_s4(9.30, 1.35, 3.50, 2.65, BG_PURPLE, BORDER_PURPLE, lw=1.6)
    add_group_tag_s4(9.40, 1.45, 1.7, 0.28, "AI & Analytics Layer", BORDER_PURPLE)
    ai_items = [
        "Gemini 2.5 Flash", "LangChain", "FAISS Vector DB",
        "Sentence Transformers", "EMA-7, 14, 30"
    ]
    y_a = 1.80
    for item in ai_items:
        add_card_s4(9.45, y_a, 3.20, 0.38, item, font_size=8.5)
        y_a += 0.42

    # 6. Decision Layer
    add_shape_s4(9.30, 4.10, 3.50, 1.30, BG_ORANGE, BORDER_ORANGE, lw=1.6)
    add_group_tag_s4(9.40, 4.20, 1.4, 0.28, "Decision Layer", BORDER_ORANGE)
    add_card_s4(9.55, 4.52, 3.0, 0.36, "Decision Engine", bg=RGBColor(255, 237, 213), border=BORDER_ORANGE, font_size=9, font_color=RGBColor(154, 52, 18), bold=True)
    add_card_s4(9.55, 4.93, 3.0, 0.36, "SELL  |  WAIT  |  STORE", bg=WHITE, border=BORDER_ORANGE, font_size=9, font_color=RGBColor(194, 65, 12), bold=True)

    # 7. Workflow Layer
    add_shape_s4(0.5, 5.50, 4.95, 1.60, BG_BLUE, BORDER_BLUE, lw=1.6)
    add_group_tag_s4(0.6, 5.60, 1.4, 0.28, "Workflow Layer", BORDER_BLUE)
    days = [("Day 1:\nHarvest", 0.65), ("Day 2:\nTransport", 1.82), ("Day 3:\nSell Crop", 2.99), ("Day 4:\nLedger", 4.16)]
    for txt, x in days:
        add_card_s4(x, 5.95, 1.05, 0.85, txt, font_size=8)
        if x < 4.0:
            arr = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 1.08), Inches(6.30), Inches(0.08), Inches(0.15))
            arr.fill.solid()
            arr.fill.fore_color.rgb = BORDER_BLUE
            arr.line.fill.background()

    # 8. Feedback Layer (Closed Loop)
    add_shape_s4(5.60, 5.50, 7.20, 1.60, BG_GREEN, BORDER_GREEN, lw=1.6)
    add_group_tag_s4(5.70, 5.60, 2.4, 0.28, "Feedback Layer (Closed Loop)", BORDER_GREEN)
    fb_cards = [
        ("Price, Transport,\nLabour", 5.80, 2.10),
        ("Revenue,\nExpenses, Profit", 8.10, 2.10),
        ("Store in MongoDB", 10.40, 2.15)
    ]
    for txt, x, w in fb_cards:
        add_card_s4(x, 5.95, w, 0.85, txt, font_size=8.5)
        if x < 10.0:
            arr = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + w + 0.05), Inches(6.30), Inches(0.12), Inches(0.15))
            arr.fill.solid()
            arr.fill.fore_color.rgb = BORDER_GREEN
            arr.line.fill.background()

    # Data Flow Badges
    add_flow_badge_s4(2.55, 1.83, 0.90, 0.28, "HTTP/JSON ➔", DARK_GRAY)
    add_flow_badge_s4(4.45, 1.48, 1.05, 0.26, "Fetch Weather ➔", RGBColor(29, 78, 216))
    add_flow_badge_s4(4.55, 2.45, 0.95, 0.26, "Fetch Prices ➔", RGBColor(29, 78, 216))
    add_flow_badge_s4(4.55, 3.85, 0.85, 0.26, "CRUD ➔", RGBColor(22, 163, 74))
    add_flow_badge_s4(4.55, 4.30, 0.85, 0.26, "Prompt ➔", RGBColor(147, 51, 234))
    add_flow_badge_s4(11.35, 3.85, 0.90, 0.26, "Analysis ➔", RGBColor(234, 88, 12))
    add_flow_badge_s4(4.85, 5.80, 0.80, 0.26, "Actuals ➔", RGBColor(22, 163, 74))
    add_flow_badge_s4(8.85, 5.25, 1.55, 0.26, "⮝ Update History (DB)", RGBColor(22, 163, 74))
    add_flow_badge_s4(10.80, 5.25, 1.70, 0.26, "⮝ Retrain/Improve (AI)", RGBColor(147, 51, 234))

    # =========================================================================
    # SLIDE 5: DATASET & FEATURE ENGINEERING
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Dataset Engineering: 1,351,051 Records & 25 Features")

    fig4_path = os.path.join(FIG_DIR, "fig4_feature_importance.png")
    if os.path.exists(fig4_path):
        s5.shapes.add_picture(fig4_path, Inches(5.8), Inches(1.4), Inches(6.7), Inches(5.6))

    add_card(s5, 0.8, 1.4, 4.7, 5.6, "Empirical Training Dataset Details")
    tb5 = s5.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(4.3), Inches(4.9))
    tf5 = tb5.text_frame
    tf5.word_wrap = True

    ds_bullets = [
        ("Source:", "Government of India AGMARKNET national portal."),
        ("Coverage:", "358 APMC Mandis across Maharashtra (2001–2024)."),
        ("Volume:", "1,351,051 longitudinal daily market records."),
        ("Commodities (8):", "Soyabean, Wheat, Onion, Cotton, Maize, Tomato, Rice, Potato."),
        ("Temporal Split:", "Strict Chronological Partitioning (Zero Leakage):\n  • Train (2001–2021): 76.1% (1.03M records)\n  • Validation (2022–2023): 14.1% (190k records)\n  • Unseen Test (2024): 9.8% (132k records)"),
        ("25 Features Extracted:", "Categorical (3), Calendar & Season (9), Autoregressive Lags (5), Rolling Momentum & Log-Arrivals (8).")
    ]
    for i, (title, desc) in enumerate(ds_bullets):
        p = tf5.paragraphs[0] if i == 0 else tf5.add_paragraph()
        p.text = f"• {title} "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = NAVY_PRIMARY
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 6: MODEL ACCURACY & BENCHMARK COMPARISONS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Model Performance Benchmarks: Random Forest Superiority")

    fig1_path = os.path.join(FIG_DIR, "fig1_model_benchmarks.png")
    if os.path.exists(fig1_path):
        s6.shapes.add_picture(fig1_path, Inches(0.8), Inches(1.4), Inches(11.7), Inches(3.2))

    # Benchmark summary card
    add_card(s6, 0.8, 4.8, 11.7, 2.2, "Comparative Evaluation on Unseen 2024 APMC Test Set")
    tb6 = s6.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.5))
    tf6 = tb6.text_frame
    tf6.word_wrap = True

    eval_summary = (
        "1. Random Forest achieved R² = 0.9687, outperforming Linear Regression (0.8124) and PyTorch LSTM (0.9412).\n"
        "2. Mean Absolute Error (MAE): ₹68.40 per quintal — an exceptional accuracy margin for ₹2,500–₹3,500 produce.\n"
        "3. Mean Absolute Percentage Error (MAPE): 2.85% (Equivalent to 97.15% predictive accuracy on test data).\n"
        "4. Why Random Forest Won: On tabular datasets with mixed categorical, discrete seasonal, and lag features, ensemble decision trees eliminate vanishing gradient issues and train in 38 seconds vs. 482 seconds for LSTM."
    )
    p = tf6.paragraphs[0]
    p.text = eval_summary
    p.font.size = Pt(11.5)
    p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 7: 24-YEAR WALK-FORWARD STABILITY PROOF
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Generalization Proof: 5-Fold Walk-Forward Cross-Validation")

    fig5_path = os.path.join(FIG_DIR, "fig5_walk_forward_stability.png")
    if os.path.exists(fig5_path):
        s7.shapes.add_picture(fig5_path, Inches(0.8), Inches(1.4), Inches(7.5), Inches(4.2))

    add_card(s7, 8.6, 1.4, 3.9, 5.5, "Stability Analysis Across 24 Years")
    tb7 = s7.shapes.add_textbox(Inches(8.8), Inches(1.9), Inches(3.5), Inches(4.8))
    tf7 = tb7.text_frame
    tf7.word_wrap = True

    stab_bullets = [
        ("No Lookahead Bias:", "Standard K-fold randomly shuffles data, leaking future prices to past training. We used Expanding-Window Time-Series Validation."),
        ("Mean R² = 0.9489 ± 0.0118:", "Coefficient of Variation (CV) is only 1.24%, proving extraordinary stability across economic regimes."),
        ("Mean MAPE = 7.84%:", "Average predictive accuracy of 92.16% sustained across 2011 to 2024."),
        ("Zero Outlier Folds:", "All folds achieved R² > 0.935, confirming the model never collapses under market shocks.")
    ]
    for i, (title, desc) in enumerate(stab_bullets):
        p = tf7.paragraphs[0] if i == 0 else tf7.add_paragraph()
        p.text = f"• {title} "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = EMERALD
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 8: TIME-SERIES PRICE FORECASTING & RESIDUALS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Time-Series Analytics: Actual vs. Predicted Price Trajectory")

    fig2_path = os.path.join(FIG_DIR, "fig2_price_forecast_actual_vs_predicted.png")
    if os.path.exists(fig2_path):
        s8.shapes.add_picture(fig2_path, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.5))

    # =========================================================================
    # SLIDE 9: 6-FACTOR HYBRID PRICING RECOMMENDATION ENGINE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Smart Pricing Engine: The 6-Factor Hybrid Formula")

    add_card(s9, 0.8, 1.4, 11.7, 1.6, "The Mathematical Hybrid Pricing Formulation", bg_color=EMERALD_LIGHT, border_color=EMERALD)
    tb9_form = s9.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(0.9))
    p = tb9_form.text_frame.paragraphs[0]
    p.text = "P_rec = 0.35 * P_mandi + 0.25 * P_ML + 0.20 * P_EMA + 0.10 * P_week + 0.05 * P_weather + 0.05 * P_hist\nP_final = P_rec * Quality_Multiplier (Grade A: 1.02, Grade B: 1.00, Grade C: 0.95)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    factors = [
        ("35% Mandi Spot Price", "Real-time modal price fetched directly from AGMARKNET API/DB for the specific district and commodity."),
        ("25% Machine Learning", "Random Forest Regressor prediction utilizing 25 engineered lag, arrival, and seasonal features."),
        ("20% EMA Momentum", "Exponential Moving Average trend (EMA-7/14/30). Applies 1.02x multiplier for upward and 0.98x for downward trends."),
        ("10% 7-Day Average", "Trailing 7-day rolling window mean price to smooth out short-term weekend and holiday volatility."),
        ("5% Weather Risk Factor", "Live OpenWeatherMap integration. Discounts price by 0.97x if forecast rain probability exceeds 60%."),
        ("5% Historical Baseline", "24-year longitudinal monthly historical average for long-term price anchorage.")
    ]

    for i, (title, desc) in enumerate(factors):
        col = i % 3
        row = i // 3
        left = 0.8 + col * 4.0
        top = 3.2 + row * 1.9
        add_card(s9, left, top, 3.7, 1.7, title)
        tb = s9.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.5), Inches(3.3), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 10: MULTILINGUAL RAG ADVISORY ENGINE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Multilingual Advisory: Retrieval-Augmented Generation (RAG)")

    rag_cards = [
        ("1. Vector Embedding", "Sentence-BERT\n(all-MiniLM-L6-v2)", "Transforms user query into a 384-dimensional dense semantic vector in <8 ms.", BLUE_ACCENT),
        ("2. Dense Similarity Index", "FAISS Vector Database\n(IndexFlatIP)", "Cosine similarity search over curated agronomic chunks. Retrieves Top-3 relevant passages.", EMERALD),
        ("3. Anti-Hallucination Guard", "Threshold Filter\n(Cosine Sim >= 0.45)", "Queries below 0.45 trigger automatic fallback to prevent false agronomic advice.", ORANGE_ACCENT),
        ("4. Context Generation", "Google Gemini LLM\n(Trilingual Support)", "Generates grounded answers in English, Hindi, and Marathi (Devanagari script).", NAVY_PRIMARY)
    ]

    for i, (stage, tech, desc, colr) in enumerate(rag_cards):
        left = 0.8 + i * 3.0
        add_card(s10, left, 1.4, 2.7, 3.8, stage, border_color=colr)
        tb = s10.shapes.add_textbox(Inches(left + 0.2), Inches(2.0), Inches(2.3), Inches(3.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = tech
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = colr
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = DARK_GRAY
        p2.space_before = Pt(8)

    add_card(s10, 0.8, 5.4, 11.7, 1.6, "Live Agricultural Advisory Verification")
    tb10 = s10.shapes.add_textbox(Inches(1.0), Inches(5.8), Inches(11.3), Inches(1.1))
    tf10 = tb10.text_frame
    p = tf10.paragraphs[0]
    p.text = "• English Query: 'What is the best fertilizer for Onion in Nashik?' -> Retrieves NPK 100:50:50 schedule.\n• Hindi Query: 'कांद्यासाठी खत व्यवस्थापन कसे करावे?' -> Responds directly in Devanagari script with verified APMC dosage.\n• Marathi Query: 'सोयाबीन वरील कीड नियंत्रण उपाय सांगा.' -> Provides integrated pest management advice from local KVK guidelines."
    p.font.size = Pt(11)
    p.font.color.rgb = NAVY_PRIMARY

    # =========================================================================
    # SLIDE 11: DIRECT B2B MARKETPLACE & 4-STAGE FULFILLMENT
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Direct B2B Marketplace & 4-Stage Fulfillment FSM")

    add_card(s11, 0.8, 1.4, 5.6, 5.5, "Direct B2B Marketplace Mechanics")
    tb11_l = s11.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.2), Inches(4.8))
    tf11_l = tb11_l.text_frame
    tf11_l.word_wrap = True

    mkt_bullets = [
        ("100% Disintermediation:", "Farmers post crop listings directly specifying commodity, quintals, expected price, and quality grade."),
        ("Buyer Procurement Requirements:", "Wholesale buyers post bulk demand requirements; the platform matches listings automatically."),
        ("Interactive Counter-Bids:", "Integrated buyer offer negotiation with AI recommended floor price protection for farmers."),
        ("Haversine Road Distance Calculation:", "Approximates inter-district transit distance:\nd = 2R * arcsin(sqrt(sin²(Δφ/2) + cos φ1 cos φ2 sin²(Δλ/2)))\nRoad Distance = 1.25 * d (with empirical circuity factor)."),
        ("Dynamic Freight Slabs:", "Transparent logistics cost: Freight = Road Distance * ₹0.50/km * Quantity.")
    ]
    for i, (title, desc) in enumerate(mkt_bullets):
        p = tf11_l.paragraphs[0] if i == 0 else tf11_l.add_paragraph()
        p.text = f"• {title} "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = NAVY_PRIMARY
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    add_card(s11, 6.8, 1.4, 5.7, 5.5, "The 4-Stage Order State Machine", bg_color=EMERALD_LIGHT, border_color=EMERALD)
    fsm_steps = [
        ("STAGE 1: Order Confirmed", "Farmer accepts buyer purchase request. Deal record created with locked quantity & price.", BLUE_ACCENT),
        ("STAGE 2: Dispatched", "Farmer packages produce and dispatches consignment. Timestamped status update sent to buyer.", ORANGE_ACCENT),
        ("STAGE 3: Out for Delivery", "Consignment in transit. Estimated delivery date derived from distance slabs (1 to 5 days).", RGBColor(123, 31, 162)),
        ("STAGE 4: Delivered (Terminal)", "Buyer verifies and accepts delivery. Instantly triggers automated ledger synchronization.", EMERALD)
    ]
    for i, (stitle, sdesc, scol) in enumerate(fsm_steps):
        top = 2.0 + i * 1.2
        c = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.0), Inches(top), Inches(5.3), Inches(1.05))
        c.fill.solid()
        c.fill.fore_color.rgb = WHITE
        c.line.color.rgb = scol
        c.line.width = Pt(1.5)
        tf = c.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = stitle
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = scol
        p2 = tf.add_paragraph()
        p2.text = sdesc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 12: AUTOMATED DIGITAL LEDGER SYNCHRONIZATION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Core Innovation: Automated Digital Ledger Synchronization")

    add_card(s12, 0.8, 1.4, 11.7, 1.6, "Autonomous Accounting Event Flow Upon Delivery", bg_color=EMERALD_LIGHT, border_color=EMERALD)
    tb12_flow = s12.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(0.9))
    p = tb12_flow.text_frame.paragraphs[0]
    p.text = "[Deal Reaches 'Delivered']  --->  [Create Transaction Record]  --->  [Generate Tax Invoice PDF]  --->  [Post Ledger Entry]\nNet Farm Profit = Total Sale Amount - (Freight Transportation + Packaging + Platform Fee)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    ledger_cards = [
        ("Zero Manual Bookkeeping", "Traditional farmers rarely record sales, preventing access to bank credit. CropPoint automatically writes an immutable ledger entry as soon as the deal is marked delivered."),
        ("Categorized Financials", "Ledger automatically logs credit as 'Crop Sale (Marketplace)' and debits transportation and input expenses into distinct accounts."),
        ("Audit-Ready Invoicing", "Generates downloadable PDF tax invoices with deal ID, GST/PAN metadata, quantity, rate, and delivery timestamps for accounting."),
        ("Real-Time Analytics", "Aggregates daily, monthly, and yearly net profit trends, giving farmers clear visibility of their true agricultural ROI.")
    ]
    for i, (title, desc) in enumerate(ledger_cards):
        col = i % 2
        row = i // 2
        left = 0.8 + col * 6.0
        top = 3.2 + row * 1.9
        add_card(s12, left, top, 5.7, 1.7, title)
        tb = s12.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.5), Inches(5.3), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 13: FULL STACK TECHNICAL IMPLEMENTATION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Technical Implementation: Full-Stack Architecture")

    tech_cards = [
        ("Frontend Architecture", "React 18.3 + Vite + Tailwind CSS", "Role-based dashboards (Farmer, Buyer, Admin). Responsive UI, Lucide icons, Chart.js financial charts, and trilingual i18n context."),
        ("Backend REST Gateway", "FastAPI (Python 3.12) + Pydantic", "Asynchronous endpoints under /api/v1/. Centralized exception handling, CORS middleware, Pydantic validation, and Swagger UI docs."),
        ("Database & ORM", "SQLite + SQLAlchemy 2.0 (Async)", "22 relational tables with foreign-key cascade integrity: users, listings, requests, deals, ledger, ratings, notifications."),
        ("Security & Auth", "JWT Bearer (HS256) + BCrypt", "Role-based access control (RBAC), Insecure Direct Object Reference (IDOR) ownership validation guards on all mutations, and SQL injection prevention.")
    ]
    for i, (title, tech, desc) in enumerate(tech_cards):
        col = i % 2
        row = i // 2
        left = 0.8 + col * 6.0
        top = 1.4 + row * 2.7
        add_card(s13, left, top, 5.7, 2.5, title)
        tb = s13.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.5), Inches(5.3), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = tech
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = BLUE_ACCENT
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = DARK_GRAY
        p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 14: EMPIRICAL TESTING AUDIT (68 TEST CASES)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Quality Assurance: 68-Case Comprehensive Test Suite (98.5%)")

    # Table of modules
    rows, cols = 8, 3
    t_shape = s14.shapes.add_table(rows, cols, Inches(0.8), Inches(1.4), Inches(7.5), Inches(5.5))
    table = t_shape.table
    table.columns[0].width = Inches(3.8)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(1.9)

    m_headers = ["Functional Module Audited", "Test Cases", "Pass Status"]
    for c_idx, text in enumerate(m_headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE

    modules_data = [
        ("Authentication & JWT Token Security", "7 Tests", "100% (7/7) PASSED"),
        ("Security, Roles & IDOR Guards", "4 Tests", "100% (4/4) PASSED"),
        ("AGMARKNET Live Mandi Intelligence", "8 Tests", "100% (8/8) PASSED"),
        ("OpenWeatherMap Weather Engine", "3 Tests", "100% (3/3) PASSED"),
        ("AI Price Forecasting & 6-Factor Engine", "8 Tests", "100% (8/8) PASSED"),
        ("B2B Deals Lifecycle & Fulfillment", "2 Tests", "100% (2/2) PASSED"),
        ("Digital Ledger & Financial Invoicing", "7 Tests", "100% (7/7) PASSED")
    ]
    for r_idx, (m_name, m_cases, m_stat) in enumerate(modules_data, 1):
        table.cell(r_idx, 0).text_frame.paragraphs[0].text = m_name
        table.cell(r_idx, 1).text_frame.paragraphs[0].text = m_cases
        p_stat = table.cell(r_idx, 2).text_frame.paragraphs[0]
        p_stat.text = m_stat
        p_stat.font.bold = True
        p_stat.font.color.rgb = EMERALD
        for c in range(3):
            table.cell(r_idx, c).text_frame.paragraphs[0].font.size = Pt(10)

    add_card(s14, 8.6, 1.4, 3.9, 5.5, "Live Verification Summary", bg_color=EMERALD_LIGHT, border_color=EMERALD)
    tb14_r = s14.shapes.add_textbox(Inches(8.8), Inches(1.9), Inches(3.5), Inches(4.8))
    tf14_r = tb14_r.text_frame
    tf14_r.word_wrap = True

    audit_pts = [
        ("Total Tests:", "68 automated test cases executed across 13 modules."),
        ("Passed:", "67 / 68 test cases (98.5% Pass Rate)."),
        ("Zero Mock Data:", "All endpoints query real SQLite production tables and trained pkl models."),
        ("Frontend Build:", "Vite production build passes with 0 errors."),
        ("Swagger Coverage:", "24 routers with interactive documentation at /docs.")
    ]
    for i, (title, desc) in enumerate(audit_pts):
        p = tf14_r.paragraphs[0] if i == 0 else tf14_r.add_paragraph()
        p.text = f"• {title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = NAVY_PRIMARY
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 15: SOFTWARE & HARDWARE REQUIREMENTS
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Software & Hardware Requirements", "REVIEW 3: SYSTEM INFRASTRUCTURE")

    # Left: Software Requirements
    add_card(s15, 0.5, 1.4, 6.0, 5.6, "Software Requirements", bg_color=EMERALD_LIGHT, border_color=EMERALD)
    tb15_sw = s15.shapes.add_textbox(Inches(0.7), Inches(2.0), Inches(5.6), Inches(4.8))
    tf15_sw = tb15_sw.text_frame
    tf15_sw.word_wrap = True

    sw_items = [
        ("OS:", "Ubuntu 22.04 LTS / macOS 13+ / Windows 11"),
        ("Backend Language:", "Python 3.12"),
        ("Web Framework:", "FastAPI (Uvicorn ASGI Server)"),
        ("Frontend:", "React 18.3 + Vite 5.x + Tailwind CSS 3.x"),
        ("Database:", "SQLite 3 + SQLAlchemy 2.0 (Async ORM)"),
        ("ML Framework:", "Scikit-learn 1.4 + PyTorch 2.2"),
        ("AI / NLP:", "Sentence-Transformers (all-MiniLM-L6-v2) + FAISS"),
        ("LLM Integration:", "Google Gemini API (Generative Language API)"),
        ("Weather API:", "OpenWeatherMap Current Weather & Forecast API"),
        ("Market Data:", "AGMARKNET Portal (Govt. of India APMC Data)"),
        ("Auth & Security:", "PyJWT (HS256) + BCrypt Password Hashing"),
    ]
    for i, (title, desc) in enumerate(sw_items):
        p = tf15_sw.paragraphs[0] if i == 0 else tf15_sw.add_paragraph()
        p.text = f"✓ {title} "
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = EMERALD
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # Right: Hardware Requirements
    add_card(s15, 6.8, 1.4, 5.7, 5.6, "Hardware Requirements", bg_color=RGBColor(227, 242, 253), border_color=BLUE_ACCENT)
    tb15_hw = s15.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.8))
    tf15_hw = tb15_hw.text_frame
    tf15_hw.word_wrap = True

    hw_items = [
        ("RAM (Minimum):", "8 GB RAM (16 GB Recommended for ML Training)"),
        ("Storage:", "500 GB Disk Space (ML Model = 419 MB; Dataset = ~1.4 GB)"),
        ("Processor:", "Intel Core i5 / AMD Ryzen 5 (8th Gen+) or equivalent"),
        ("GPU (Optional):", "NVIDIA GTX 1060+ CUDA-enabled (Accelerates PyTorch LSTM training)"),
        ("Internet:", "Stable broadband for Gemini API, OpenWeatherMap & AGMARKNET live calls"),
        ("Browser:", "Google Chrome 120+ / Firefox 121+ (Frontend UI)"),
        ("Ports Required:", "Backend: 8000 | Frontend Dev: 5173 | HTTP Server: 8080"),
    ]
    for i, (title, desc) in enumerate(hw_items):
        p = tf15_hw.paragraphs[0] if i == 0 else tf15_hw.add_paragraph()
        p.text = f"• {title} "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = BLUE_ACCENT
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 16: EXPECTED RESULTS → ACHIEVED RESULTS
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Expected Results → ✅ Achieved Results (Review 3)", "REVIEW 3: RESULTS VERIFICATION")

    # Top achievement metrics bar
    metric_cards = [
        ("R² = 0.9687", "Price Prediction Accuracy", EMERALD),
        ("MAPE = 2.85%", "Mean Abs % Error on 2024 Test Data", BLUE_ACCENT),
        ("MAE = ₹68.40/Qtl", "Avg Price Error Per Quintal", ORANGE_ACCENT),
        ("98.5% Test Pass", "68 Automated Test Cases (67/68)", RGBColor(123, 31, 162)),
    ]
    for i, (val, label, colr) in enumerate(metric_cards):
        left = 0.5 + i * 3.1
        card = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(1.35), Inches(2.8), Inches(1.3))
        card.fill.solid()
        card.fill.fore_color.rgb = NAVY_PRIMARY
        card.line.color.rgb = colr
        card.line.width = Pt(2)
        tf = card.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = colr
        p1.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(9)
        p2.font.color.rgb = RGBColor(200, 225, 240)
        p2.alignment = PP_ALIGN.CENTER

    # Comparison table: Expected vs Achieved
    rows2, cols2 = 8, 3
    t2 = s16.shapes.add_table(rows2, cols2, Inches(0.5), Inches(2.9), Inches(12.3), Inches(4.2))
    tbl2 = t2.table
    tbl2.columns[0].width = Inches(3.8)
    tbl2.columns[1].width = Inches(3.7)
    tbl2.columns[2].width = Inches(4.8)

    hdrs2 = ["Deliverable / Metric", "Expected (Review 2 Plan)", "✅ Achieved (Review 3 — 100%)"]
    for c, h in enumerate(hdrs2):
        cell = tbl2.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    expected_vs_achieved = [
        ("ML Price Prediction R²", "Target: R² ≥ 0.90", "✅ R² = 0.9687 on 132K unseen 2024 records"),
        ("Prediction Error (MAPE)", "Target: MAPE < 10%", "✅ MAPE = 2.85% (97.15% accuracy)"),
        ("B2B Marketplace", "Design & basic listing module", "✅ Full FSM: Counter-bids, Freight calc, Delivery"),
        ("Advisory (RAG)", "Chatbot prototype with generic LLM", "✅ FAISS + Sentence-BERT + Gemini Trilingual"),
        ("Digital Ledger", "Manual entry interface", "✅ Auto-sync on delivery; PDF invoice generation"),
        ("Live Weather Integration", "Static local weather", "✅ OpenWeatherMap API integrated into 6-Factor pricing"),
        ("Test Coverage", "Unit tests for core modules", "✅ 68 test cases, 98.5% pass rate, zero mock data"),
    ]
    for r, (item, exp, ach) in enumerate(expected_vs_achieved, 1):
        for c, txt in enumerate([item, exp, ach]):
            cell = tbl2.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r % 2 == 1 else LIGHT_BG
            p = cell.text_frame.paragraphs[0]
            p.text = txt
            p.font.size = Pt(10)
            p.font.color.rgb = EMERALD if c == 2 else DARK_GRAY
            if c == 2:
                p.font.bold = True

    # =========================================================================
    # SLIDE 17: IMPLEMENTATION PROGRESS (REVIEW 3 — 100% COMPLETE)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Implementation Progress — Review 3: 100% Complete", "REVIEW 3: PROGRESS DASHBOARD")

    # Background
    bg17 = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.2), Inches(13.333), Inches(6.3))
    bg17.fill.solid()
    bg17.fill.fore_color.rgb = LIGHT_BG
    bg17.line.fill.background()

    modules_progress = [
        ("ML Price Forecasting Engine", "Random Forest trained on 1.35M records • R²=0.9687 • 25 features", 100, EMERALD),
        ("6-Factor Smart Pricing Recommendation", "Hybrid formula: Mandi+ML+EMA+Weekly+Weather+Historical", 100, EMERALD),
        ("Multilingual RAG Advisory (FAISS + Gemini)", "Trilingual EN/HI/MR • Cosine similarity threshold 0.45 guard", 100, EMERALD),
        ("B2B Direct Marketplace + Negotiations", "Live listings • Counter-bids • Haversine freight calculation", 100, BLUE_ACCENT),
        ("4-Stage Order Fulfillment FSM", "Confirmed → Dispatched → Transit → Delivered (State Machine)", 100, BLUE_ACCENT),
        ("Automated Digital Ledger + PDF Invoicing", "Auto-sync on delivery • Net profit calculation • PDF generation", 100, BLUE_ACCENT),
        ("Live Weather & Risk Engine", "OpenWeatherMap API • Real-time precipitation risk calculation", 100, ORANGE_ACCENT),
        ("Authentication, Security & RBAC", "JWT HS256 • BCrypt • IDOR guards • 24 routers • 22 DB tables", 100, ORANGE_ACCENT),
    ]

    bar_bg_color = RGBColor(229, 231, 235)
    for i, (mod_name, mod_detail, pct, bar_color) in enumerate(modules_progress):
        top = 1.45 + i * 0.74
        # Module label
        tb_mod = s17.shapes.add_textbox(Inches(0.5), Inches(top), Inches(4.5), Inches(0.35))
        p_mod = tb_mod.text_frame.paragraphs[0]
        p_mod.text = mod_name
        p_mod.font.size = Pt(10)
        p_mod.font.bold = True
        p_mod.font.color.rgb = NAVY_PRIMARY

        # Sub-detail
        tb_det = s17.shapes.add_textbox(Inches(0.5), Inches(top + 0.33), Inches(4.4), Inches(0.28))
        p_det = tb_det.text_frame.paragraphs[0]
        p_det.text = mod_detail
        p_det.font.size = Pt(7.5)
        p_det.font.color.rgb = MUTED_GRAY

        # Progress bar background
        bg_bar = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.1), Inches(top + 0.15), Inches(6.8), Inches(0.35))
        bg_bar.fill.solid()
        bg_bar.fill.fore_color.rgb = bar_bg_color
        bg_bar.line.fill.background()

        # Progress bar fill (100%)
        fill_bar = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.1), Inches(top + 0.15), Inches(6.8), Inches(0.35))
        fill_bar.fill.solid()
        fill_bar.fill.fore_color.rgb = bar_color
        fill_bar.line.fill.background()

        # Percentage label
        tb_pct = s17.shapes.add_textbox(Inches(12.05), Inches(top + 0.13), Inches(0.8), Inches(0.35))
        p_pct = tb_pct.text_frame.paragraphs[0]
        p_pct.text = f"{pct}%"
        p_pct.font.size = Pt(10)
        p_pct.font.bold = True
        p_pct.font.color.rgb = bar_color

    # Overall completion badge
    badge17 = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.5), Inches(7.08), Inches(6.3), Inches(0.32))
    badge17.fill.solid()
    badge17.fill.fore_color.rgb = EMERALD
    badge17.line.fill.background()
    bp17 = badge17.text_frame.paragraphs[0]
    bp17.text = "🎉  OVERALL PROJECT COMPLETION: 100%  —  ALL 8 MODULES DEPLOYED & VERIFIED"
    bp17.font.size = Pt(10)
    bp17.font.bold = True
    bp17.font.color.rgb = WHITE
    bp17.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 18: COMPLETED WORK PLAN (TIMELINE)
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Work Plan — All Milestones Completed ✅", "REVIEW 3: PROJECT TIMELINE SUMMARY")

    # Timeline milestones
    milestones = [
        ("Phase 1\n(Jun–Jul 2025)", "Project Initiation & Research",
         "• Problem statement finalization & literature survey (20 papers)\n• Technology stack selection: FastAPI, React, SQLite, Scikit-learn\n• ER diagram design for 22 relational tables",
         BLUE_ACCENT, "COMPLETED ✅"),
        ("Phase 2\n(Aug 2025)", "Backend & Data Engineering",
         "• AGMARKNET dataset acquisition: 1,351,051 Maharashtra APMC records\n• 25-feature engineering pipeline (lags, EMA, calendar, arrivals)\n• FastAPI skeleton with JWT auth, RBAC, and 24 routers",
         EMERALD, "COMPLETED ✅"),
        ("Phase 3\n(Sep 2025)", "ML Model Training & Validation",
         "• Random Forest Regressor training (38 sec) vs LSTM (482 sec)\n• 5-Fold Walk-Forward CV: Mean R²=0.9489, CV=1.24%\n• Final test on 2024 unseen data: R²=0.9687, MAPE=2.85%",
         ORANGE_ACCENT, "COMPLETED ✅"),
        ("Phase 4\n(Oct–Nov 2025)", "Full-Stack Integration & RAG",
         "• React 18.3 frontend: role-based dashboards, Chart.js analytics\n• FAISS trilingual RAG advisory + Gemini API integration\n• B2B Marketplace, 4-Stage FSM, Automated Ledger sync",
         RGBColor(123, 31, 162), "COMPLETED ✅"),
        ("Phase 5\n(Dec 2025–Jan 2026)", "Testing, QA & Documentation",
         "• 68 automated test cases, 98.5% pass rate\n• IEEE research paper (20 citations, 6 figures, LaTeX)\n• Review 3 presentation, demo guide, and final submission",
         NAVY_PRIMARY, "COMPLETED ✅"),
    ]

    for i, (phase, phase_title, phase_desc, colr, status) in enumerate(milestones):
        top = 1.42 + i * 1.2
        # Phase label box
        phase_box = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(top), Inches(1.7), Inches(1.05))
        phase_box.fill.solid()
        phase_box.fill.fore_color.rgb = colr
        phase_box.line.fill.background()
        ptf = phase_box.text_frame
        ptf.word_wrap = True
        pp = ptf.paragraphs[0]
        pp.text = phase
        pp.font.size = Pt(9.5)
        pp.font.bold = True
        pp.font.color.rgb = WHITE
        pp.alignment = PP_ALIGN.CENTER

        # Connector arrow
        arr = s18.shapes.add_textbox(Inches(2.15), Inches(top + 0.3), Inches(0.3), Inches(0.4))
        arr.text_frame.paragraphs[0].text = "→"
        arr.text_frame.paragraphs[0].font.size = Pt(18)
        arr.text_frame.paragraphs[0].font.color.rgb = colr

        # Title + description card
        detail_card = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.5), Inches(top), Inches(8.8), Inches(1.05))
        detail_card.fill.solid()
        detail_card.fill.fore_color.rgb = WHITE
        detail_card.line.color.rgb = colr
        detail_card.line.width = Pt(1)
        dtf = detail_card.text_frame
        dtf.word_wrap = True
        dp1 = dtf.paragraphs[0]
        dp1.text = phase_title
        dp1.font.size = Pt(11)
        dp1.font.bold = True
        dp1.font.color.rgb = colr
        dp2 = dtf.add_paragraph()
        dp2.text = phase_desc
        dp2.font.size = Pt(8.5)
        dp2.font.color.rgb = DARK_GRAY

        # Status badge
        stat_box = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.45), Inches(top + 0.27), Inches(1.45), Inches(0.45))
        stat_box.fill.solid()
        stat_box.fill.fore_color.rgb = EMERALD
        stat_box.line.fill.background()
        stf = stat_box.text_frame
        sp = stf.paragraphs[0]
        sp.text = status
        sp.font.size = Pt(8)
        sp.font.bold = True
        sp.font.color.rgb = WHITE
        sp.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 19: IEEE RESEARCH PAPER DEFENSE
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Research Publication: Submission-Ready IEEE Conference Paper")

    add_card(s19, 0.8, 1.4, 11.7, 5.5, "Paper Title: CropPoint: An AI-Enhanced Agricultural Marketplace & Decision Support System")
    tb19 = s19.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(4.7))
    tf19 = tb19.text_frame
    tf19.word_wrap = True

    paper_pts = [
        ("IEEE Template Conformity:", "Formatted in official IEEEtran two-column conference layout. Includes abstract, keywords, 6 Roman-numeral sections, algorithms, and LaTeX equations."),
        ("Empirical Rigor:", "Documents Random Forest vs. PyTorch LSTM vs. Linear Regression on 1,351,051 records with expanding walk-forward cross-validation."),
        ("20 Verified Downloaded References:", "Cites peer-reviewed papers: Breiman (Random Forests), Lewis et al. (RAG NeurIPS), Johnson et al. (FAISS IEEE TBD), Hochreiter (LSTM), Liakos et al. (Sensors), and Wolfert et al. (Agri Systems). All 20 corresponding PDFs downloaded and verified in references/ folder."),
        ("6 Publication-Grade Figures:", "High-resolution (300 DPI) scientific charts and visual figures covering benchmarks, time-series forecasting with confidence intervals, residual error histograms, feature importance, and system architecture.")
    ]
    for i, (title, desc) in enumerate(paper_pts):
        p = tf19.paragraphs[0] if i == 0 else tf19.add_paragraph()
        p.text = f"• {title} "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = NAVY_PRIMARY
        p.space_before = Pt(12)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 20: STEP-BY-STEP LIVE DEMO GUIDE FOR EVALUATORS
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Live Demonstration Walkthrough (Review 3 Demo Flow)")

    demo_steps = [
        ("Step 1: Terminal Accuracy Audit", "Run: python backend/show_accuracy.py in VS Code. Displays instant R²=0.9687, MAE=₹68.40, and 24-year CV table live to the committee."),
        ("Step 2: AI Price Recommendation", "Navigate to AI Recommendation on localhost:5173. Select Onion (Nashik). Shows live 6-factor hybrid rate (₹3,801/Qtl) with 92% confidence."),
        ("Step 3: Multilingual RAG Chat", "Ask advisory queries in English and Marathi ('कांद्यासाठी खत व्यवस्थापन'). Demonstrates FAISS vector retrieval and Devanagari script output."),
        ("Step 4: B2B Order & FSM Workflow", "Farmer lists crop -> Buyer sends purchase request -> Accept request. Progress order through Confirmed -> Dispatched -> Transit -> Delivered."),
        ("Step 5: Automatic Ledger Sync", "Open Digital Ledger. As soon as Delivered is clicked, show the new ₹2,38,000 credit entry, freight deduction, and downloadable PDF invoice.")
    ]
    for i, (title, desc) in enumerate(demo_steps):
        top = 1.4 + i * 1.1
        c = s20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(top), Inches(11.7), Inches(0.95))
        c.fill.solid()
        c.fill.fore_color.rgb = WHITE
        c.line.color.rgb = EMERALD
        c.line.width = Pt(1.2)
        tf = c.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = EMERALD
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = DARK_GRAY

    # =========================================================================
    # SLIDE 21: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "Conclusion & Future Enhancements")

    add_card(s21, 0.8, 1.4, 5.6, 5.5, "Review 3 Conclusion: 100% Realized")
    tb21_l = s21.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(5.2), Inches(4.8))
    tf21_l = tb21_l.text_frame
    tf21_l.word_wrap = True
    c_pts = [
        ("Unified Ecosystem:", "Successfully proved that price forecasting, advisory, marketplace, and bookkeeping operate best as a single closed loop."),
        ("High Predictive Accuracy:", "Trained Random Forest model achieves R² = 0.9687 and MAPE = 2.85% across 1.35M records."),
        ("Production Readiness:", "24 routers, 22 database tables, 68 test cases (98.5% pass rate), and zero mock data dependencies."),
        ("Real Impact for Smallholders:", "Empowers farmers with transparent pricing, direct wholesale buyers, and automatic accounting records.")
    ]
    for i, (title, desc) in enumerate(c_pts):
        p = tf21_l.paragraphs[0] if i == 0 else tf21_l.add_paragraph()
        p.text = f"✓ {title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = EMERALD
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    add_card(s21, 6.8, 1.4, 5.7, 5.5, "Future Research & Engineering Scope")
    tb21_r = s21.shapes.add_textbox(Inches(7.0), Inches(1.9), Inches(5.3), Inches(4.8))
    tf21_r = tb21_r.text_frame
    tf21_r.word_wrap = True
    f_pts = [
        ("Smart Contract Payment Escrow:", "Integrating blockchain smart contracts to hold buyer funds in escrow and release payment upon IoT-sensor-verified delivery."),
        ("Computer Vision Disease Diagnosis:", "Integrating a MobileNet/EfficientNet CNN to diagnose crop diseases from leaf photos directly in the RAG context."),
        ("Satellite NDVI Monitoring:", "Sentinel-2 satellite imagery integration for regional vegetation health and yield forecasting."),
        ("Reinforcement Learning (RLHF):", "Fine-tuning recommendation weights based on continuous farmer negotiation feedback.")
    ]
    for i, (title, desc) in enumerate(f_pts):
        p = tf21_r.paragraphs[0] if i == 0 else tf21_r.add_paragraph()
        p.text = f"• {title} "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = BLUE_ACCENT
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = DARK_GRAY

    # Save presentation
    prs.save(OUTPUT_PPTX)
    print(f"✅ Presentation successfully generated: {OUTPUT_PPTX}")

if __name__ == "__main__":
    create_deck()
