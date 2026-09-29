#!/usr/bin/env python3
"""
Generates an ultra-clean, minimalist, executive-level Architecture & Workflow Diagram
for CropPoint (Smart Agri AI).
Features:
- 6 Big, Elegant Blocks in a Natural Closed Loop (3 on Top, 3 on Bottom)
- Generous breathing room, large clear typography, bold icons
- Zero visual clutter, zero theory walls - instant 5-second clarity
- Saves to:
  - figures/CropPoint_Easy_Architecture.png
  - CropPoint_Easy_Architecture.png
  - CropPoint_End_to_End_Workflow.png (for seamless compatibility)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI"
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

OUT_PATHS = [
    os.path.join(FIG_DIR, "CropPoint_Easy_Architecture.png"),
    os.path.join(BASE_DIR, "CropPoint_Easy_Architecture.png"),
    os.path.join(FIG_DIR, "CropPoint_End_to_End_Workflow.png"),
    os.path.join(BASE_DIR, "CropPoint_End_to_End_Workflow.png")
]

def draw_easy_architecture():
    # 20 x 11.25 inches (16:9 widescreen presentation layout)
    fig, ax = plt.subplots(figsize=(20, 11.25), dpi=300)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 11.25)
    ax.axis('off')

    # Background canvas
    bg_canvas = patches.Rectangle((0, 0), 20, 11.25, facecolor="#F8FAFC", edgecolor="none", zorder=0)
    ax.add_patch(bg_canvas)

    # Header Bar
    head_box = patches.FancyBboxPatch((0.8, 10.05), 18.4, 0.90, boxstyle="round,pad=0.06,rounding_size=0.12",
                                     facecolor="#0F172A", edgecolor="#020617", linewidth=1.5, zorder=1)
    ax.add_patch(head_box)
    ax.text(10.0, 10.58, "CropPoint: System Architecture & Workflow",
            fontsize=17, fontweight='bold', color="#FFFFFF", ha='center', va='center', zorder=2)
    ax.text(10.0, 10.25, "Closed-Loop Autonomous Supply Chain: Sensing ➔ Prediction ➔ Decision ➔ Execution ➔ Settlement ➔ Retraining",
            fontsize=10.0, color="#94A3B8", ha='center', va='center', zorder=2)

    # 6 Stage Colors
    THEMES = {
        1: {"border": "#2563EB", "bg": "#EFF6FF", "badge": "#DBEAFE", "badge_text": "#1E40AF"},  # Blue: Sensing
        2: {"border": "#7C3AED", "bg": "#F5F3FF", "badge": "#EDE9FE", "badge_text": "#5B21B6"},  # Purple: AI
        3: {"border": "#EA580C", "bg": "#FFF7ED", "badge": "#FFEDD5", "badge_text": "#9A3412"},  # Orange: Decision
        4: {"border": "#0D9488", "bg": "#F0FDFA", "badge": "#CCFBF1", "badge_text": "#115E59"},  # Teal: Execution
        5: {"border": "#16A34A", "bg": "#F0FDF4", "badge": "#DCFCE7", "badge_text": "#166534"},  # Green: Settlement
        6: {"border": "#DC2626", "bg": "#FEF2F2", "badge": "#FEE2E2", "badge_text": "#991B1B"}   # Red: Closed Loop
    }

    # Helper: Draw Big, Clean Architectural Block
    def draw_block(x, y, w, h, stage_num, icon_symbol, title, subtitle, bullets, chips):
        theme = THEMES[stage_num]
        
        # Outer Card with gentle shadow
        shadow = patches.FancyBboxPatch((x + 0.05, y - 0.05), w, h, boxstyle="round,pad=0.06,rounding_size=0.14",
                                        facecolor="#E2E8F0", edgecolor="none", zorder=1)
        ax.add_patch(shadow)

        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.14",
                                      facecolor="#FFFFFF", edgecolor=theme["border"], linewidth=2.0, zorder=2)
        ax.add_patch(card)

        # Header Pill
        pill = patches.FancyBboxPatch((x + 0.25, y + h - 0.65), w - 0.5, 0.45, boxstyle="round,pad=0.04,rounding_size=0.08",
                                     facecolor=theme["bg"], edgecolor=theme["border"], linewidth=1.0, zorder=3)
        ax.add_patch(pill)

        # Number Badge (Left)
        num_circle = patches.Circle((x + 0.55, y + h - 0.42), 0.18, facecolor=theme["border"], edgecolor="none", zorder=4)
        ax.add_patch(num_circle)
        ax.text(x + 0.55, y + h - 0.42, str(stage_num), fontsize=9.5, fontweight='bold', color="#FFFFFF", ha='center', va='center', zorder=5)

        # Title & Subtitle in Header
        ax.text(x + 0.90, y + h - 0.35, title, fontsize=11.0, fontweight='bold', color="#0F172A", va='center', zorder=5)
        ax.text(x + 0.90, y + h - 0.54, subtitle, fontsize=8.2, color="#64748B", fontstyle='italic', va='center', zorder=5)

        # Icon Glyph (Right)
        ax.text(x + w - 0.55, y + h - 0.42, icon_symbol, fontsize=12.0, fontweight='bold', color=theme["border"], ha='center', va='center', zorder=5)

        # Content Bullets (Clear, Large, 3 Points Max)
        b_y = y + h - 1.05
        for b in bullets:
            # Bullet dot
            dot = patches.Circle((x + 0.45, b_y), 0.05, facecolor=theme["border"], edgecolor="none", zorder=4)
            ax.add_patch(dot)
            ax.text(x + 0.65, b_y, b, fontsize=9.2, color="#1E293B", va='center', zorder=4)
            b_y -= 0.42

        # Bottom Chips / Tech Stack Badges
        c_x = x + 0.35
        for chip in chips:
            c_w = (len(chip) * 0.070 + 0.25) if len(chips) == 4 else (len(chip) * 0.095 + 0.32)
            c_rect = patches.FancyBboxPatch((c_x, y + 0.22), c_w, 0.30, boxstyle="round,pad=0.02,rounding_size=0.06",
                                            facecolor=theme["badge"], edgecolor=theme["border"], linewidth=0.8, zorder=4)
            ax.add_patch(c_rect)
            ax.text(c_x + c_w/2, y + 0.37, chip, fontsize=7.0 if len(chips) == 4 else 7.8, fontweight='bold', color=theme["badge_text"], ha='center', va='center', zorder=5)
            c_x += c_w + (0.10 if len(chips) == 4 else 0.18)

    # Layout Parameters
    bw = 5.6     # Block width
    bh = 3.8     # Block height
    gap_x = 0.8  # Horizontal gap

    # X coordinates for 3 columns:
    # Col 1: 0.8 to 6.4
    # Col 2: 7.2 to 12.8
    # Col 3: 13.6 to 19.2
    x1 = 0.8
    x2 = 7.2
    x3 = 13.6

    y_top = 5.75     # Top row Y
    y_bot = 0.65     # Bottom row Y

    # =========================================================================
    # ROW 1 (TOP): 1. SENSING ➔ 2. AI BRAIN ➔ 3. DECISION
    # =========================================================================

    # Block 1: Sensing & Ingestion
    draw_block(x1, y_top, bw, bh, 1, "[IN]", "Sensing & Ingestion", "Farmer input & real-time streaming", [
        "Farmer inputs crop, quantity & location",
        "AGMARKNET API: Live modal prices (358 mandis)",
        "OpenWeatherMap: Rainfall & storm risk discount"
    ], ["AGMARKNET", "OpenWeather", "React UI"])

    # Block 2: AI Forecasting Engine
    draw_block(x2, y_top, bw, bh, 2, "[AI]", "AI Predictive Brain", "Forecasting & domain advisory", [
        "Random Forest: 1-14 day price forecast",
        "High Accuracy: R² = 0.9687, MAPE = 2.85%",
        "FAISS Vector RAG: Multilingual advisor (En/Hi/Mr)"
    ], ["Random Forest", "FAISS RAG", "Gemini 2.5"])

    # Block 3: Decision Engine
    draw_block(x3, y_top, bw, bh, 3, "[OPT]", "Decision Optimizer", "Net economic profit maximization", [
        "6-Factor weighted math (Modal 35%, ML 25%, EMA 20%)",
        "Evaluates price gain vs. storage & spoilage cost",
        "Actionable Signal: 'SELL NOW' | 'WAIT' | 'STORE'"
    ], ["Weighted Algorithm", "Cost Optimizer", "SELL NOW"])

    # =========================================================================
    # ROW 2 (BOTTOM): 6. CLOSED LOOP ◄ 5. SETTLEMENT ◄ 4. WORKFLOW EXECUTION
    # =========================================================================

    # Block 6: Closed-Loop Feedback (Bottom-Left)
    draw_block(x1, y_bot, bw, bh, 6, "[LOOP]", "Closed-Loop Feedback", "Self-improving AI retraining loop", [
        "Captures real sale price & freight as Actuals",
        "Measures residual error: e = y_actual - y_pred",
        "Periodic walk-forward retraining eliminates drift"
    ], ["Continuous Retrain", "Zero Model Drift", "MongoDB Atlas"])

    # Block 5: Financial Settlement (Bottom-Middle)
    draw_block(x2, y_bot, bw, bh, 5, "[ACC]", "Automated Ledger", "Double-entry bookkeeping & invoices", [
        "Auto-credits revenue & debits freight/labor costs",
        "Computes True Net Farmer Profit instantly",
        "Auto-generates legal GST/APMC compliant invoice"
    ], ["Double-Entry", "Auto Invoicing", "Instant Audit"])

    # Block 4: 4-Day Physical Execution (Bottom-Right)
    draw_block(x3, y_bot, bw, bh, 4, "[FLOW]", "4-Day Execution Plan", "Managed agricultural fulfillment", [
        "Day 1: Field Harvest & Grading (A/B/C)",
        "Day 2: Haversine Freight Logistics & Truck Hire",
        "Day 3: APMC Mandi Auction & Direct Buyer Sale",
        "Day 4: Realized Price & Bills Logged in Ledger"
    ], ["Day 1 Harvest", "Day 2 Truck", "Day 3 Sell", "Day 4 Ledger"])

    # =========================================================================
    # CONNECTING ARROWS (NATURAL CLOSED-LOOP RECTANGLE)
    # =========================================================================

    def draw_clean_arrow(p1, p2, label="", color="#475569", lw=2.5, is_loop=False):
        ls = '--' if is_loop else '-'
        arr = patches.FancyArrowPatch(p1, p2,
                                      arrowstyle="->",
                                      mutation_scale=18,
                                      color=color,
                                      linewidth=lw,
                                      linestyle=ls,
                                      zorder=10)
        ax.add_patch(arr)
        if label:
            mx = (p1[0] + p2[0]) / 2
            my = (p1[1] + p2[1]) / 2
            ax.text(mx, my, label, fontsize=8.2, fontweight='bold', color=color,
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="#FFFFFF", edgecolor=color, alpha=0.95, lw=1.0),
                    ha='center', va='center', zorder=12)

    # 1 ➔ 2 (Top Left to Top Middle)
    draw_clean_arrow((x1 + bw, y_top + bh/2), (x2, y_top + bh/2), "Clean Data", color="#2563EB")

    # 2 ➔ 3 (Top Middle to Top Right)
    draw_clean_arrow((x2 + bw, y_top + bh/2), (x3, y_top + bh/2), "Forecasts", color="#7C3AED")

    # 3 ➔ 4 (Top Right drops straight down to Bottom Right!)
    draw_clean_arrow((x3 + bw/2, y_top), (x3 + bw/2, y_bot + bh), "Trigger (SELL NOW)", color="#EA580C")

    # 4 ➔ 5 (Bottom Right to Bottom Middle)
    draw_clean_arrow((x3, y_bot + bh/2), (x2 + bw, y_bot + bh/2), "Realized Actuals", color="#0D9488")

    # 5 ➔ 6 (Bottom Middle to Bottom Left)
    draw_clean_arrow((x2, y_bot + bh/2), (x1 + bw, y_bot + bh/2), "Verified Records", color="#16A34A")

    # 6 ➔ 2 (THE CLOSED LOOP: Bottom Left straight UP to Top Middle!)
    # Clean orthogonal loop: from top of Block 6 (x1 + bw/2, y_bot + bh)
    # up to y_top - 0.45, then right to bottom of Block 2 (x2 + bw/2, y_top)
    loop_x = [x1 + bw/2, x1 + bw/2, x2 + bw/2, x2 + bw/2]
    loop_y = [y_bot + bh, y_top - 0.45, y_top - 0.45, y_top]
    ax.plot(loop_x, loop_y, color="#DC2626", linewidth=2.5, linestyle="--", zorder=10)
    
    arr_retrain = patches.FancyArrowPatch((x2 + bw/2, y_top - 0.45), (x2 + bw/2, y_top),
                                         arrowstyle="->", mutation_scale=18, color="#DC2626", linewidth=2.5, zorder=12)
    ax.add_patch(arr_retrain)

    ax.text((x1 + bw/2 + x2 + bw/2)/2, y_top - 0.45, "CONTINUOUS CLOSED-LOOP MODEL RETRAINING (ELIMINATES DRIFT)",
            fontsize=8.5, fontweight='bold', color="#DC2626",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#FEF2F2", edgecolor="#DC2626", lw=1.2),
            ha='center', va='center', zorder=15)

    plt.tight_layout()
    for p in OUT_PATHS:
        plt.savefig(p, bbox_inches='tight', dpi=300)
        print(f"Saved: {p}")
    plt.close()

if __name__ == "__main__":
    draw_easy_architecture()
