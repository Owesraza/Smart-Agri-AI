#!/usr/bin/env python3
"""
Generates the exact, publication-quality 8-layer System Architecture Diagram
matching the user's uploaded diagram, with 'Plot Management' 100% removed.
Saves to figures/fig6_closed_loop_workflow.png and CropPoint_Architecture_Diagram.png.
Clean typography without missing glyph warnings.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI"
FIG_DIR = os.path.join(BASE_DIR, "figures")
OUT_PATHS = [
    os.path.join(FIG_DIR, "fig6_closed_loop_workflow.png"),
    os.path.join(BASE_DIR, "CropPoint_Architecture_Diagram.png")
]

def draw_architecture():
    fig, ax = plt.subplots(figsize=(18, 10.2), dpi=300)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10.2)
    ax.axis('off')

    # Color palette matching user's original image
    BG_BLUE = "#EBF4FE"
    BORDER_BLUE = "#3B82F6"
    TITLE_BLUE = "#1D4ED8"

    BG_GREEN = "#EEFBF3"
    BORDER_GREEN = "#22C55E"
    TITLE_GREEN = "#15803D"

    BG_PURPLE = "#FBF2FE"
    BORDER_PURPLE = "#C084FC"
    TITLE_PURPLE = "#7E22CE"

    BG_ORANGE = "#FFF7ED"
    BORDER_ORANGE = "#FB923C"
    TITLE_ORANGE = "#C2410C"

    CARD_WHITE = "#FFFFFF"
    BORDER_CARD = "#CBD5E1"
    TEXT_DARK = "#1E293B"

    def draw_group(x, y, w, h, bg, border, title):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor=bg, edgecolor=border, linewidth=1.8, zorder=1)
        ax.add_patch(rect)
        tag_w = min(w * 0.55, 2.7)
        tag = patches.FancyBboxPatch((x + 0.12, y + h - 0.38), tag_w, 0.3, boxstyle="round,pad=0.04,rounding_size=0.08",
                                     facecolor=bg, edgecolor=border, linewidth=1.2, zorder=2)
        ax.add_patch(tag)
        ax.text(x + 0.22, y + h - 0.23, title, fontsize=9.5, fontweight='bold', color=border, va='center', zorder=3)

    def draw_card(x, y, w, h, text, is_header=False, font_size=9.0, border_color=BORDER_CARD):
        fc = "#F8FAFC" if is_header else CARD_WHITE
        ec = BORDER_BLUE if is_header else border_color
        lw = 1.3 if is_header else 1.0
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.1",
                                      facecolor=fc, edgecolor=ec, linewidth=lw, zorder=4)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, fontsize=font_size, fontweight='bold' if is_header else 'medium',
                color=TEXT_DARK, ha='center', va='center', zorder=5)

    # =========================================================================
    # 1. PRESENTATION LAYER (x=0.4, y=2.4, w=3.4, h=7.5)
    # =========================================================================
    draw_group(0.4, 2.4, 3.4, 7.5, BG_BLUE, BORDER_BLUE, "Presentation Layer")
    draw_card(0.7, 9.0, 2.8, 0.55, "React.js + Tailwind", is_header=True, font_size=9.5)
    
    # 7 Items (Plot Management removed)
    pres_items = [
        "Farmer Login/ Register",
        "Dashboard",
        "Market Intelligence",
        "AI Assistant",
        "Workflow Manager",
        "Ledger",
        "Analytics Dashboard"
    ]
    card_h = 0.52
    spacing = 0.68
    start_y = 8.1
    for i, txt in enumerate(pres_items):
        draw_card(0.7, start_y - i * spacing, 2.8, card_h, txt, font_size=9.0)

    # =========================================================================
    # 2. BACKEND LAYER (x=4.2, y=2.4, w=3.6, h=7.5)
    # =========================================================================
    draw_group(4.2, 2.4, 3.6, 7.5, BG_GREEN, BORDER_GREEN, "Backend Layer")
    draw_card(4.6, 9.0, 2.8, 0.55, "Python FastAPI", is_header=True, font_size=9.5)

    # 6 Items (Plot Management removed)
    back_items = [
        "Authentication",
        "User Management",
        "Market Data Processing",
        "Workflow Management",
        "Ledger Management",
        "AI Request Handling"
    ]
    for i, txt in enumerate(back_items):
        draw_card(4.6, start_y - i * spacing, 2.8, card_h, txt, font_size=9.0)

    draw_card(4.8, 2.7, 2.4, 0.5, "API Integration", font_size=9.0)

    # =========================================================================
    # 3. DATA COLLECTION LAYER (x=8.2, y=6.2, w=4.6, h=3.7)
    # =========================================================================
    draw_group(8.2, 6.2, 4.6, 3.7, BG_BLUE, BORDER_BLUE, "Data Collection Layer")
    
    draw_card(8.6, 8.4, 1.7, 0.75, "Agmarknet\nAPI", font_size=8.5)
    draw_card(10.7, 8.4, 1.7, 0.75, "OpenWea-\ntherMap", font_size=8.5)
    draw_card(8.6, 7.2, 1.7, 0.75, "Historical\nDataset", font_size=8.5)
    draw_card(10.7, 7.2, 1.7, 0.75, "Farmer Info", font_size=8.5)
    draw_card(9.65, 6.4, 1.7, 0.65, "Agri News", font_size=8.5)

    # =========================================================================
    # 4. DATABASE LAYER (x=8.2, y=2.4, w=4.6, h=3.4)
    # =========================================================================
    draw_group(8.2, 2.4, 4.6, 3.4, BG_GREEN, BORDER_GREEN, "Database Layer")
    
    # Cylinder-style representation of MongoDB Atlas
    db_card = patches.FancyBboxPatch((8.7, 4.2), 3.6, 0.8, boxstyle="round,pad=0.05,rounding_size=0.15",
                                     facecolor="#DCFCE7", edgecolor=BORDER_GREEN, linewidth=1.5, zorder=4)
    ax.add_patch(db_card)
    ax.text(10.5, 4.6, "MongoDB Atlas", fontsize=11, fontweight='bold', color="#166534", ha='center', va='center', zorder=5)

    ax.text(10.5, 3.4, "Users, Crops, Transactions,\nWorkflows, Ledger, Recommendations", 
            fontsize=9.0, color="#15803D", ha='center', va='center', fontweight='bold', zorder=5)

    # =========================================================================
    # 5. AI & ANALYTICS LAYER (x=13.2, y=5.0, w=4.4, h=4.9)
    # =========================================================================
    draw_group(13.2, 5.0, 4.4, 4.9, BG_PURPLE, BORDER_PURPLE, "AI & Analytics Layer")
    
    ai_items = [
        "Gemini 2.5 Flash",
        "LangChain",
        "FAISS Vector DB",
        "Sentence Transformers",
        "EMA-7, 14, 30"
    ]
    ai_y = 8.8
    for i, txt in enumerate(ai_items):
        draw_card(13.7, ai_y, 3.4, 0.52, txt, font_size=9.0)
        ai_y -= 0.72

    # =========================================================================
    # 6. DECISION LAYER (x=13.2, y=2.4, w=4.4, h=2.3)
    # =========================================================================
    draw_group(13.2, 2.4, 4.4, 2.3, BG_ORANGE, BORDER_ORANGE, "Decision Layer")
    
    # Diamond shape for Decision Engine
    diamond = patches.Polygon([[15.4, 4.15], [16.25, 3.6], [15.4, 3.05], [14.55, 3.6]], 
                              closed=True, facecolor="#FFEDD5", edgecolor=BORDER_ORANGE, linewidth=1.6, zorder=4)
    ax.add_patch(diamond)
    ax.text(15.4, 3.6, "Decision\nEngine", fontsize=8.0, fontweight='bold', color="#9A3412", ha='center', va='center', zorder=5)
    
    ax.text(15.4, 2.68, "SELL | WAIT | STORE", fontsize=9.5, fontweight='bold', color="#C2410C", ha='center', va='center', zorder=5)

    # =========================================================================
    # 7. WORKFLOW LAYER (x=0.4, y=0.3, w=6.6, h=1.8)
    # =========================================================================
    draw_group(0.4, 0.3, 6.6, 1.8, BG_BLUE, BORDER_BLUE, "Workflow Layer")
    
    wf_days = ["Day 1:\nHarvest", "Day 2:\nTransport", "Day 3:\nSell Crop", "Day 4:\nLedger"]
    wf_x = 0.7
    for i, day in enumerate(wf_days):
        draw_card(wf_x, 0.65, 1.2, 0.85, day, font_size=8.5)
        if i < 3:
            ax.annotate('', xy=(wf_x + 1.45, 1.07), xytext=(wf_x + 1.25, 1.07),
                        arrowprops=dict(facecolor=BORDER_BLUE, edgecolor=BORDER_BLUE, width=1.5, headwidth=5, zorder=6))
        wf_x += 1.5

    # =========================================================================
    # 8. FEEDBACK LAYER (CLOSED LOOP) (x=7.4, y=0.3, w=10.2, h=1.8)
    # =========================================================================
    draw_group(7.4, 0.3, 10.2, 1.8, BG_GREEN, BORDER_GREEN, "Feedback Layer (Closed Loop)")
    
    draw_card(8.0, 0.65, 2.5, 0.85, "Price, Transport,\nLabour", font_size=8.5)
    draw_card(11.2, 0.65, 2.5, 0.85, "Revenue,\nExpenses, Profit", font_size=8.5)
    draw_card(14.4, 0.65, 2.5, 0.85, "Store in MongoDB", font_size=8.5)

    # =========================================================================
    # CONNECTING ARROWS & LABELS (Exact routing from user's image)
    # =========================================================================
    # 1. HTTP/JSON (Presentation -> Backend)
    ax.annotate('', xy=(4.6, 9.27), xytext=(3.5, 9.27),
                arrowprops=dict(facecolor=TEXT_DARK, edgecolor=TEXT_DARK, width=1.2, headwidth=4.5, zorder=7))
    ax.text(4.05, 9.4, "HTTP/JSON", fontsize=7.5, color=TEXT_DARK, ha='center', va='bottom', fontweight='bold', zorder=8)

    # 2. Fetch Weather (FastAPI -> OpenWeatherMap)
    ax.plot([6.0, 6.0, 11.55, 11.55], [9.55, 9.9, 9.9, 9.15], color="#1D4ED8", linewidth=1.4, zorder=6)
    ax.annotate('', xy=(11.55, 9.15), xytext=(11.55, 9.25),
                arrowprops=dict(facecolor="#1D4ED8", edgecolor="#1D4ED8", width=1.2, headwidth=4.5, zorder=7))
    ax.text(8.8, 10.0, "Fetch Weather", fontsize=8.0, color="#1D4ED8", fontweight='bold', ha='center', zorder=8)

    # 3. Fetch Prices (Market Data Processing -> Agmarknet API)
    ax.plot([7.4, 9.45, 9.45], [6.75, 6.75, 8.4], color="#1D4ED8", linewidth=1.4, zorder=6)
    ax.annotate('', xy=(9.45, 8.4), xytext=(9.45, 8.3),
                arrowprops=dict(facecolor="#1D4ED8", edgecolor="#1D4ED8", width=1.2, headwidth=4.5, zorder=7))
    ax.text(8.9, 7.6, "Fetch Prices", fontsize=8.0, color="#1D4ED8", fontweight='bold', ha='center', zorder=8)

    # 4. Load Data (Market Data Processing -> Historical Dataset)
    ax.annotate('', xy=(8.6, 7.55), xytext=(7.4, 6.75),
                arrowprops=dict(facecolor="#1D4ED8", edgecolor="#1D4ED8", width=1.2, headwidth=4.5, zorder=7))
    ax.text(8.0, 7.3, "Load Data", fontsize=8.0, color="#1D4ED8", fontweight='bold', ha='center', zorder=8)

    # 5. CRUD (Backend -> MongoDB Atlas)
    ax.plot([7.4, 8.2, 8.7], [5.4, 5.4, 4.6], color="#16A34A", linewidth=1.4, zorder=6)
    ax.annotate('', xy=(8.7, 4.6), xytext=(8.5, 4.8),
                arrowprops=dict(facecolor="#16A34A", edgecolor="#16A34A", width=1.2, headwidth=4.5, zorder=7))
    ax.text(7.9, 5.55, "CRUD", fontsize=8.0, color="#16A34A", fontweight='bold', ha='center', zorder=8)

    # 6. Prompt (AI Request Handling -> Gemini 2.5 Flash)
    ax.plot([7.4, 7.8, 13.0, 13.7], [4.7, 4.7, 9.08, 9.08], color="#9333EA", linewidth=1.4, zorder=6)
    ax.annotate('', xy=(13.7, 9.08), xytext=(13.5, 9.08),
                arrowprops=dict(facecolor="#9333EA", edgecolor="#9333EA", width=1.2, headwidth=4.5, zorder=7))
    ax.text(9.8, 4.85, "Prompt", fontsize=8.0, color="#9333EA", fontweight='bold', ha='center', zorder=8)

    # 7. Query (FAISS / AI Layer -> MongoDB Atlas)
    ax.plot([13.7, 12.8, 12.8, 12.3], [7.6, 7.6, 4.6, 4.6], color="#9333EA", linewidth=1.4, zorder=6)
    ax.annotate('', xy=(12.3, 4.6), xytext=(12.5, 4.6),
                arrowprops=dict(facecolor="#9333EA", edgecolor="#9333EA", width=1.2, headwidth=4.5, zorder=7))
    ax.text(12.6, 6.2, "Query", fontsize=8.0, color="#9333EA", fontweight='bold', ha='center', zorder=8)

    # 8. Analysis (AI Layer -> Decision Engine)
    ax.plot([17.1, 17.5, 17.5, 16.25], [7.0, 7.0, 3.6, 3.6], color="#EA580C", linewidth=1.4, zorder=6)
    ax.annotate('', xy=(16.25, 3.6), xytext=(16.45, 3.6),
                arrowprops=dict(facecolor="#EA580C", edgecolor="#EA580C", width=1.2, headwidth=4.5, zorder=7))
    ax.text(17.7, 5.3, "Analysis", fontsize=8.0, color="#EA580C", fontweight='bold', va='center', rotation=-90, zorder=8)

    # 9. Trigger (Decision Engine -> Workflow Manager in Presentation Layer)
    ax.plot([14.55, 13.0, 13.0, 3.8, 3.8, 3.5], [3.6, 3.6, 2.1, 2.1, 5.38, 5.38], color="#64748B", linewidth=1.3, zorder=6)
    ax.annotate('', xy=(3.5, 5.38), xytext=(3.7, 5.38),
                arrowprops=dict(facecolor="#64748B", edgecolor="#64748B", width=1.2, headwidth=4.5, zorder=7))
    ax.text(8.0, 2.22, "Trigger", fontsize=8.0, color="#64748B", fontweight='bold', ha='center', zorder=8)

    # 10. Actuals (Day 4: Ledger -> Feedback Layer)
    ax.annotate('', xy=(8.0, 1.07), xytext=(6.4, 1.07),
                arrowprops=dict(facecolor="#16A34A", edgecolor="#16A34A", width=1.2, headwidth=4.5, zorder=7))
    ax.text(7.2, 1.2, "Actuals", fontsize=8.0, color="#16A34A", fontweight='bold', ha='center', zorder=8)

    # 11. Update History (Store in MongoDB -> MongoDB Atlas, Dotted Green)
    ax.plot([15.65, 15.65, 10.5, 10.5], [1.5, 2.0, 2.0, 3.0], color="#16A34A", linestyle='--', linewidth=1.5, zorder=6)
    ax.annotate('', xy=(10.5, 3.0), xytext=(10.5, 2.8),
                arrowprops=dict(facecolor="#16A34A", edgecolor="#16A34A", width=1.2, headwidth=4.5, linestyle='--', zorder=7))
    ax.text(12.8, 2.15, "Update History", fontsize=8.0, color="#16A34A", fontweight='bold', ha='center', zorder=8)

    # 12. Retrain/Improve (Store in MongoDB -> AI Layer, Dotted Purple)
    ax.plot([15.65, 15.65], [1.5, 5.0], color="#9333EA", linestyle='--', linewidth=1.5, zorder=6)
    ax.annotate('', xy=(15.65, 5.0), xytext=(15.65, 4.8),
                arrowprops=dict(facecolor="#9333EA", edgecolor="#9333EA", width=1.2, headwidth=4.5, linestyle='--', zorder=7))
    ax.text(15.65, 4.8, "Retrain/Improve", fontsize=8.0, color="#9333EA", fontweight='bold', ha='center', va='bottom', zorder=8)

    plt.tight_layout()
    for path in OUT_PATHS:
        plt.savefig(path, dpi=300, bbox_inches='tight')
        print(f"✅ Generated: {path}")
    plt.close()

if __name__ == "__main__":
    draw_architecture()
