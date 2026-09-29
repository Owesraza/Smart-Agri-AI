#!/usr/bin/env python3
"""
Test building the complete 8-layer architecture diagram natively in PowerPoint shapes.
"""

import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_architecture_slide(s4):
    # Palette
    NAVY_PRIMARY = RGBColor(27, 38, 59)
    EMERALD = RGBColor(46, 125, 50)
    WHITE = RGBColor(255, 255, 255)
    DARK_GRAY = RGBColor(33, 37, 41)
    
    # Layer Backgrounds and Borders
    BG_BLUE = RGBColor(235, 244, 254)
    BORDER_BLUE = RGBColor(59, 130, 246)
    
    BG_GREEN = RGBColor(238, 251, 243)
    BORDER_GREEN = RGBColor(34, 197, 94)
    
    BG_PURPLE = RGBColor(251, 242, 254)
    BORDER_PURPLE = RGBColor(192, 132, 252)
    
    BG_ORANGE = RGBColor(255, 247, 237)
    BORDER_ORANGE = RGBColor(251, 146, 60)
    
    BORDER_CARD = RGBColor(203, 213, 225)

    def add_shape(left, top, width, height, bg, border, lw=1.2, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
        shape = s4.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg
        shape.line.color.rgb = border
        shape.line.width = Pt(lw)
        return shape

    def add_card(left, top, width, height, text, bg=WHITE, border=BORDER_CARD, 
                 font_size=9, font_color=DARK_GRAY, bold=False, align=PP_ALIGN.CENTER):
        card = add_shape(left, top, width, height, bg, border, lw=1.0)
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

    def add_group_tag(left, top, width, height, text, border_color):
        tag = add_shape(left, top, width, height, WHITE, border_color, lw=1.0)
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

    def add_flow_badge(left, top, width, height, text, color):
        badge = add_shape(left, top, width, height, WHITE, color, lw=1.0)
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

    # =========================================================================
    # 1. PRESENTATION LAYER (left=0.5, top=1.35, width=2.45, height=4.05)
    # =========================================================================
    add_shape(0.5, 1.35, 2.45, 4.05, BG_BLUE, BORDER_BLUE, lw=1.6)
    add_group_tag(0.6, 1.45, 1.7, 0.28, "Presentation Layer", BORDER_BLUE)
    add_card(0.6, 1.80, 2.25, 0.35, "React.js + Tailwind", bg=RGBColor(248, 250, 252), border=BORDER_BLUE, font_size=9.5, font_color=RGBColor(30, 58, 138), bold=True)
    
    pres_items = [
        "Farmer Login/ Register",
        "Dashboard",
        "Market Intelligence",
        "AI Assistant",
        "Workflow Manager",
        "Ledger",
        "Analytics Dashboard"
    ]
    y_p = 2.22
    for item in pres_items:
        add_card(0.6, y_p, 2.25, 0.38, item, font_size=8.5)
        y_p += 0.43

    # =========================================================================
    # 2. BACKEND LAYER (left=3.10, top=1.35, width=2.45, height=4.05)
    # =========================================================================
    add_shape(3.10, 1.35, 2.45, 4.05, BG_GREEN, BORDER_GREEN, lw=1.6)
    add_group_tag(3.20, 1.45, 1.5, 0.28, "Backend Layer", BORDER_GREEN)
    add_card(3.20, 1.80, 2.25, 0.35, "Python FastAPI", bg=RGBColor(248, 250, 252), border=BORDER_GREEN, font_size=9.5, font_color=RGBColor(21, 128, 61), bold=True)

    back_items = [
        "Authentication",
        "User Management",
        "Market Data Processing",
        "Workflow Management",
        "Ledger Management",
        "AI Request Handling"
    ]
    y_b = 2.22
    for item in back_items:
        add_card(3.20, y_b, 2.25, 0.38, item, font_size=8.5)
        y_b += 0.43
    add_card(3.30, 4.88, 2.05, 0.38, "API Integration", bg=RGBColor(241, 245, 249), border=RGBColor(148, 163, 184), font_size=8.5, bold=True)

    # =========================================================================
    # 3. DATA COLLECTION LAYER (left=5.70, top=1.35, width=3.45, height=2.0)
    # =========================================================================
    add_shape(5.70, 1.35, 3.45, 2.0, BG_BLUE, BORDER_BLUE, lw=1.6)
    add_group_tag(5.80, 1.45, 1.7, 0.28, "Data Collection Layer", BORDER_BLUE)
    
    add_card(5.82, 1.80, 1.55, 0.42, "Agmarknet API", font_size=8.5)
    add_card(7.48, 1.80, 1.55, 0.42, "OpenWeatherMap", font_size=8.5)
    add_card(5.82, 2.30, 1.55, 0.42, "Historical Dataset", font_size=8.5)
    add_card(7.48, 2.30, 1.55, 0.42, "Farmer Info", font_size=8.5)
    add_card(6.65, 2.80, 1.55, 0.42, "Agri News", font_size=8.5)

    # =========================================================================
    # 4. DATABASE LAYER (left=5.70, top=3.45, width=3.45, height=1.95)
    # =========================================================================
    add_shape(5.70, 3.45, 3.45, 1.95, BG_GREEN, BORDER_GREEN, lw=1.6)
    add_group_tag(5.80, 3.55, 1.5, 0.28, "Database Layer", BORDER_GREEN)
    
    add_card(5.95, 3.90, 2.95, 0.48, "MongoDB Atlas", bg=RGBColor(220, 252, 231), border=BORDER_GREEN, font_size=10.5, font_color=RGBColor(22, 101, 52), bold=True)
    add_card(5.95, 4.45, 2.95, 0.82, "Users, Crops, Transactions,\nWorkflows, Ledger, Recommendations", bg=WHITE, border=BORDER_CARD, font_size=8.5, font_color=RGBColor(21, 128, 61), bold=True)

    # =========================================================================
    # 5. AI & ANALYTICS LAYER (left=9.30, top=1.35, width=3.50, height=2.65)
    # =========================================================================
    add_shape(9.30, 1.35, 3.50, 2.65, BG_PURPLE, BORDER_PURPLE, lw=1.6)
    add_group_tag(9.40, 1.45, 1.7, 0.28, "AI & Analytics Layer", BORDER_PURPLE)
    
    ai_items = [
        "Gemini 2.5 Flash",
        "LangChain",
        "FAISS Vector DB",
        "Sentence Transformers",
        "EMA-7, 14, 30"
    ]
    y_a = 1.80
    for item in ai_items:
        add_card(9.45, y_a, 3.20, 0.38, item, font_size=8.5)
        y_a += 0.42

    # =========================================================================
    # 6. DECISION LAYER (left=9.30, top=4.10, width=3.50, height=1.30)
    # =========================================================================
    add_shape(9.30, 4.10, 3.50, 1.30, BG_ORANGE, BORDER_ORANGE, lw=1.6)
    add_group_tag(9.40, 4.20, 1.4, 0.28, "Decision Layer", BORDER_ORANGE)
    
    add_card(9.55, 4.52, 3.0, 0.36, "Decision Engine", bg=RGBColor(255, 237, 213), border=BORDER_ORANGE, font_size=9, font_color=RGBColor(154, 52, 18), bold=True)
    add_card(9.55, 4.93, 3.0, 0.36, "SELL  |  WAIT  |  STORE", bg=WHITE, border=BORDER_ORANGE, font_size=9, font_color=RGBColor(194, 65, 12), bold=True)

    # =========================================================================
    # 7. WORKFLOW LAYER (left=0.5, top=5.50, width=4.95, height=1.60)
    # =========================================================================
    add_shape(0.5, 5.50, 4.95, 1.60, BG_BLUE, BORDER_BLUE, lw=1.6)
    add_group_tag(0.6, 5.60, 1.4, 0.28, "Workflow Layer", BORDER_BLUE)
    
    days = [("Day 1:\nHarvest", 0.65), ("Day 2:\nTransport", 1.82), ("Day 3:\nSell Crop", 2.99), ("Day 4:\nLedger", 4.16)]
    for txt, x in days:
        add_card(x, 5.95, 1.05, 0.85, txt, font_size=8)
        if x < 4.0:
            arr = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 1.08), Inches(6.30), Inches(0.08), Inches(0.15))
            arr.fill.solid()
            arr.fill.fore_color.rgb = BORDER_BLUE
            arr.line.fill.background()

    # =========================================================================
    # 8. FEEDBACK LAYER (CLOSED LOOP) (left=5.60, top=5.50, width=7.20, height=1.60)
    # =========================================================================
    add_shape(5.60, 5.50, 7.20, 1.60, BG_GREEN, BORDER_GREEN, lw=1.6)
    add_group_tag(5.70, 5.60, 2.4, 0.28, "Feedback Layer (Closed Loop)", BORDER_GREEN)
    
    fb_cards = [
        ("Price, Transport,\nLabour", 5.80, 2.10),
        ("Revenue,\nExpenses, Profit", 8.10, 2.10),
        ("Store in MongoDB", 10.40, 2.15)
    ]
    for txt, x, w in fb_cards:
        add_card(x, 5.95, w, 0.85, txt, font_size=8.5)
        if x < 10.0:
            arr = s4.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + w + 0.05), Inches(6.30), Inches(0.12), Inches(0.15))
            arr.fill.solid()
            arr.fill.fore_color.rgb = BORDER_GREEN
            arr.line.fill.background()

    # =========================================================================
    # DATA FLOW CONNECTING BADGES
    # =========================================================================
    add_flow_badge(2.55, 1.83, 0.90, 0.28, "HTTP/JSON ➔", DARK_GRAY)
    add_flow_badge(4.45, 1.48, 1.05, 0.26, "Fetch Weather ➔", RGBColor(29, 78, 216))
    add_flow_badge(4.55, 2.45, 0.95, 0.26, "Fetch Prices ➔", RGBColor(29, 78, 216))
    add_flow_badge(4.55, 3.85, 0.85, 0.26, "CRUD ➔", RGBColor(22, 163, 74))
    add_flow_badge(4.55, 4.30, 0.85, 0.26, "Prompt ➔", RGBColor(147, 51, 234))
    add_flow_badge(11.35, 3.85, 0.90, 0.26, "Analysis ➔", RGBColor(234, 88, 12))
    add_flow_badge(4.85, 5.80, 0.80, 0.26, "Actuals ➔", RGBColor(22, 163, 74))
    add_flow_badge(8.85, 5.25, 1.55, 0.26, "⮝ Update History (DB)", RGBColor(22, 163, 74))
    add_flow_badge(10.80, 5.25, 1.70, 0.26, "⮝ Retrain/Improve (AI)", RGBColor(147, 51, 234))

prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
s = prs.slides.add_slide(prs.slide_layouts[6])
build_architecture_slide(s)
prs.save('/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI/test_arch_slide.pptx')
print('✅ Successfully built test_arch_slide.pptx!')
