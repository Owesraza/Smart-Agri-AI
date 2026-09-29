#!/usr/bin/env python3
"""
Generates an ultra-attractive, modern, visual End-to-End Workflow Diagram
for CropPoint (Smart Agri AI).
Features:
- Minimal text, maximum visual clarity
- Colorful icon badges & tech logos (Agmarknet, OpenWeather, Random Forest, Gemini, FAISS, FastAPI, MongoDB)
- High-contrast card styling with sleek modern UI aesthetics
- Zero theory clutter - crystal clear for examiners and presentations
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI"
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

OUT_PATHS = [
    os.path.join(FIG_DIR, "CropPoint_End_to_End_Workflow.png"),
    os.path.join(BASE_DIR, "CropPoint_End_to_End_Workflow.png")
]

def draw_visual_workflow():
    fig, ax = plt.subplots(figsize=(22, 13), dpi=300)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 13)
    ax.axis('off')

    # Color Palette - Modern Vibrant SaaS
    DARK_BG = "#0B1120"
    BANNER_BG = "#0F172A"
    
    # Stage Theme Colors
    C_BLUE = "#3B82F6"      # Stage 1: Ingestion
    C_PURPLE = "#A855F7"    # Stage 2: AI
    C_ORANGE = "#F97316"    # Stage 3: Decision
    C_SLATE = "#64748B"     # Stage 4: Trigger
    C_TEAL = "#0D9488"      # Stage 5: Execution
    C_GREEN = "#10B981"     # Stage 6: Ledger
    C_RED = "#EF4444"       # Stage 7: Feedback Loop

    # Top Header Banner
    header = patches.FancyBboxPatch((0.8, 11.85), 20.4, 0.95, boxstyle="round,pad=0.08,rounding_size=0.15",
                                   facecolor=BANNER_BG, edgecolor="#1E293B", linewidth=1.5, zorder=1)
    ax.add_patch(header)
    
    # Title & Subtitle
    ax.text(11.0, 12.48, "CropPoint: System Workflow (Start Point to End Point)",
            fontsize=17, fontweight='bold', color="#FFFFFF", ha='center', va='center', zorder=2)
    ax.text(11.0, 12.12, "Visual End-to-End Journey: From Farmer Inquiry to ML Prediction, 4-Day Action & Closed-Loop Retraining",
            fontsize=10.5, fontweight='normal', color="#94A3B8", ha='center', va='center', zorder=2)

    # Helper: Draw Visual Stage Container
    def draw_stage_box(x, y, w, h, border_col, bg_col, num, title, icon_text):
        # Outer container
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.14",
                                      facecolor=bg_col, edgecolor=border_col, linewidth=1.8, zorder=1)
        ax.add_patch(rect)
        
        # Header Badge with Icon
        tag_w = min(w * 0.72, 4.4)
        tag = patches.FancyBboxPatch((x + 0.15, y + h - 0.48), tag_w, 0.38, boxstyle="round,pad=0.04,rounding_size=0.08",
                                     facecolor=border_col, edgecolor=border_col, linewidth=1.0, zorder=2)
        ax.add_patch(tag)
        ax.text(x + 0.35, y + h - 0.29, f"STEP {num}: {title.upper()}", fontsize=9.2, fontweight='bold', color="#FFFFFF", va='center', zorder=3)
        
        # Circular Icon Badge at Top-Right
        cir = patches.Circle((x + w - 0.38, y + h - 0.29), 0.24, facecolor="#FFFFFF", edgecolor=border_col, linewidth=1.5, zorder=4)
        ax.add_patch(cir)
        ax.text(x + w - 0.38, y + h - 0.29, icon_text, fontsize=8.0, fontweight='bold', color=border_col, ha='center', va='center', zorder=5)

    # Helper: Draw Modern Content Card with Visual Chips
    def draw_card(x, y, w, h, title, subtitle, bullets, chips=None, border_color="#CBD5E1"):
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.08",
                                      facecolor="#FFFFFF", edgecolor=border_color, linewidth=1.2, zorder=4)
        ax.add_patch(card)

        # Title
        ax.text(x + 0.2, y + h - 0.22, title, fontsize=9.2, fontweight='bold', color="#0F172A", va='center', zorder=5)
        
        # Bullets (started higher so they never collide with bottom chips)
        curr_y = y + h - 0.50
        for b in bullets:
            ax.text(x + 0.2, curr_y, f"✔  {b}", fontsize=8.2, color="#1E293B", va='center', zorder=5)
            curr_y -= 0.26

        # Tech / Brand Chips (Logos)
        if chips:
            chip_x = x + 0.2
            for chip_text, chip_bg, chip_fg in chips:
                chip_len = len(chip_text) * 0.082 + 0.32
                c_rect = patches.FancyBboxPatch((chip_x, y + 0.10), chip_len, 0.24, boxstyle="round,pad=0.02,rounding_size=0.05",
                                               facecolor=chip_bg, edgecolor=chip_fg, linewidth=0.8, zorder=6)
                ax.add_patch(c_rect)
                ax.text(chip_x + chip_len/2, y + 0.22, chip_text, fontsize=6.8, fontweight='bold', color=chip_fg, ha='center', va='center', zorder=7)
                chip_x += chip_len + 0.14

    # Helper: Draw Flow Arrow
    def draw_arrow(x1, y1, x2, y2, label="", color="#475569", lw=2.0):
        arr = patches.FancyArrowPatch((x1, y1), (x2, y2),
                                      arrowstyle="->",
                                      mutation_scale=16,
                                      color=color,
                                      linewidth=lw,
                                      zorder=15)
        ax.add_patch(arr)
        if label:
            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            ax.text(mx, my, label, fontsize=8.0, fontweight='bold', color=color,
                    bbox=dict(boxstyle="round,pad=0.22", facecolor="#FFFFFF", edgecolor=color, alpha=0.95, lw=1.0),
                    ha='center', va='center', zorder=18)

    # =========================================================================
    # ROW 1 (TOP): 3 STAGES (Ingestion ➔ AI Core ➔ Decision Engine)
    # =========================================================================
    
    # 1. START POINT & INGESTION
    draw_stage_box(0.8, 7.8, 6.2, 3.8, C_BLUE, "#EFF6FF", "1", "Start Point", "IN")
    draw_card(1.0, 9.65, 5.8, 1.50, "Farmer Listing Entry", "Farmer registers intent to sell", [
        "Selects Crop: Onion, Soyabean, Wheat, etc.",
        "Inputs Quantity (e.g. 50 Qtl) & APMC Location"
    ], chips=[("React UI", "#EFF6FF", "#2563EB"), ("Tailwind", "#F0FDFA", "#0D9488"), ("FastAPI", "#F0FDF4", "#16A34A")])

    draw_card(1.0, 7.95, 5.8, 1.55, "Live Market & Weather Feeds", "Real-time streaming ingestion", [
        "Live Mandi Prices & Daily Arrivals (358 Mandis)",
        "Weather Forecast: Rain, Temp & Storm Risk"
    ], chips=[("AGMARKNET API", "#EFF6FF", "#1D4ED8"), ("OpenWeatherMap", "#FFF7ED", "#EA580C"), ("1.35M Rows", "#F8FAFC", "#475569")])

    # 2. AI & ANALYTICS ENGINE
    draw_stage_box(7.8, 7.8, 6.8, 3.8, C_PURPLE, "#FAF5FF", "2", "AI Predictor", "AI")
    draw_card(8.0, 9.65, 6.4, 1.50, "25-Feature Engineering", "Extracts hidden price momentum", [
        "Moving Averages: EMA-7, EMA-14, EMA-30",
        "Arrival Shock Volatility & Historical Seasonality"
    ], chips=[("EMA Momentum", "#FAF5FF", "#9333EA"), ("Lag Features", "#FAF5FF", "#7E22CE")])

    draw_card(8.0, 7.95, 6.4, 1.55, "Dual AI Modeling Engine", "Forecasts prices & post-harvest advisory", [
        "Random Forest Regressor: R² = 0.9687, MAPE = 2.85%",
        "FAISS Vector RAG: Multilingual Advisory in En / Hi / Mr"
    ], chips=[("Random Forest", "#F0FDF4", "#15803D"), ("FAISS DB", "#FAF5FF", "#9333EA"), ("Gemini 2.5", "#EFF6FF", "#1D4ED8")])

    # 3. DECISION ENGINE
    draw_stage_box(15.4, 7.8, 5.8, 3.8, C_ORANGE, "#FFF7ED", "3", "Decision Engine", "OPT")
    draw_card(15.6, 9.65, 5.4, 1.50, "Six-Factor Weighted Scoring", "Calculates net optimal gain", [
        "Modal Price (35%) + ML Forecast (25%) + EMA (20%)",
        "Rolling Mean (10%) + Weather Risk (5%) + Season (5%)"
    ], chips=[("Weighted Math", "#FFF7ED", "#C2410C"), ("Cost Optimizer", "#FFF7ED", "#EA580C")])

    draw_card(15.6, 7.95, 5.4, 1.55, "Actionable Output Signal", "Tells the farmer exactly what to do", [
        "SELL NOW (Peak price detected - highest profit)",
        "WAIT / HOLD (Prices surging in next 3-5 days)",
        "STORE (Market glut; recommend cold storage)"
    ], chips=[("SELL NOW", "#DCFCE7", "#15803D"), ("WAIT", "#FEF3C7", "#B45309"), ("STORE", "#E0E7FF", "#4338CA")])

    # Connectors Row 1
    draw_arrow(7.0, 9.7, 7.8, 9.7, "Clean Data", color=C_BLUE)
    draw_arrow(14.6, 9.7, 15.4, 9.7, "Predictions", color=C_PURPLE)

    # =========================================================================
    # ROW 2 (MIDDLE): TRIGGER ➔ 4-DAY PHYSICAL EXECUTION
    # =========================================================================

    # 4. WORKFLOW TRIGGER
    draw_stage_box(0.8, 4.1, 4.6, 3.2, C_SLATE, "#F8FAFC", "4", "Auto Trigger", "ACT")
    draw_card(1.0, 5.75, 4.2, 1.25, "Event-Driven Router", "Instant notification dispatch", [
        "Fires trigger when 'SELL NOW' is selected",
        "Pushes 4-day plan to Workflow Manager"
    ], chips=[("FastAPI Trigger", "#F1F5F9", "#334155")])

    draw_card(1.0, 4.30, 4.2, 1.30, "Farmer UI Dashboard", "Actionable confirmation", [
        "Farmer views projected net profit & schedule",
        "One-click 'Accept Schedule' starts Day 1"
    ], chips=[("Workflow Manager", "#EFF6FF", "#2563EB"), ("Push Alert", "#DCFCE7", "#15803D")])

    # 5. PHYSICAL EXECUTION PIPELINE (4 DAYS)
    draw_stage_box(6.2, 4.1, 15.0, 3.2, C_TEAL, "#F0FDFA", "5", "4-Day Execution", "FLOW")
    
    # 4 Day Action Cards
    c_w = 3.35
    c_h = 2.4
    c_y = 4.3

    draw_card(6.4, c_y, c_w, c_h, "Day 1: Harvest", "Field Operations", [
        "Crop cutting begins",
        "Grading: Grade A / B / C",
        "Standardized bagging",
        "Labor costs recorded"
    ], chips=[("Harvested", "#F0FDFA", "#0D9488"), ("Labor Log", "#F8FAFC", "#475569")])

    draw_card(10.1, c_y, c_w, c_h, "Day 2: Transport", "Logistics & Freight", [
        "Haversine route matching",
        "Best truck freight rate",
        "Transit GPS tracking",
        "Freight bill locked"
    ], chips=[("Haversine", "#EFF6FF", "#2563EB"), ("In-Transit", "#FEF3C7", "#B45309")])

    draw_card(13.8, c_y, c_w, c_h, "Day 3: Sell Crop", "Mandi Trade Settlement", [
        "APMC Mandi arrival",
        "Direct B2B buyer trade",
        "Electronic weighing",
        "Purchase verified"
    ], chips=[("Mandi Sale", "#DCFCE7", "#15803D"), ("B2B Trade", "#FAF5FF", "#7E22CE")])

    draw_card(17.5, c_y, c_w, c_h, "Day 4: Ledger", "Data Capture & Actuals", [
        "Real transaction completed",
        "Realized price captured",
        "Actual transport captured",
        "Actual labor captured"
    ], chips=[("Actuals Ready", "#F0FDF4", "#15803D"), ("Settled", "#EFF6FF", "#1D4ED8")])

    # Corridor Trigger Line from Stage 3 to Stage 4
    ax.plot([18.3, 18.3, 3.1, 3.1], [7.8, 7.5, 7.5, 7.3], color=C_ORANGE, linewidth=2.0, zorder=12)
    arr_t = patches.FancyArrowPatch((3.1, 7.4), (3.1, 7.3), arrowstyle="->", mutation_scale=16, color=C_ORANGE, linewidth=2.0, zorder=15)
    ax.add_patch(arr_t)
    ax.text(10.7, 7.5, "Automated Trigger Signal (When 'SELL NOW' is Decided)",
            fontsize=8.5, fontweight='bold', color=C_ORANGE,
            bbox=dict(boxstyle="round,pad=0.22", facecolor="#FFF7ED", edgecolor=C_ORANGE, lw=1.0),
            ha='center', va='center', zorder=18)

    # Connector from Stage 4 to Stage 5
    draw_arrow(5.4, 5.7, 6.2, 5.7, "Start Day 1", color=C_TEAL, lw=2.0)

    # Day-to-Day Arrows
    draw_arrow(9.75, 5.5, 10.1, 5.5, color=C_TEAL, lw=1.8)
    draw_arrow(13.45, 5.5, 13.8, 5.5, color=C_TEAL, lw=1.8)
    draw_arrow(17.15, 5.5, 17.5, 5.5, color=C_TEAL, lw=1.8)

    # =========================================================================
    # ROW 3 (BOTTOM): LEDGER ➔ CLOSED-LOOP RETRAINING
    # =========================================================================

    # 6. AUTOMATED FINANCIAL LEDGER
    draw_stage_box(11.4, 0.4, 9.8, 3.2, C_GREEN, "#F0FDF4", "6", "Financial Ledger", "ACC")
    draw_card(11.6, 0.6, 4.5, 2.35, "Double-Entry Accounting", "Zero manual math for farmer", [
        "Revenue: Gross crop sale value",
        "Expenses: Freight + Labor + APMC Cess",
        "Net Profit = Gross Sale - Expenses",
        "Syncs with MongoDB / SQLite"
    ], chips=[("Double-Entry", "#F0FDF4", "#15803D"), ("MongoDB", "#DCFCE7", "#16A34A")])

    draw_card(16.4, 0.6, 4.6, 2.35, "Digital Invoicing & Audit", "Verifiable transparent records", [
        "Auto-generates legal tax PDF invoice",
        "Unique cryptographic transaction hash",
        "Updates lifetime revenue analytics",
        "Downloadable for bank agri-credit"
    ], chips=[("PDF Invoice", "#FEF2F2", "#DC2626"), ("Audit Trail", "#EFF6FF", "#2563EB")])

    # 7. CLOSED-LOOP FEEDBACK & RETRAINING
    draw_stage_box(0.8, 0.4, 9.6, 3.2, C_RED, "#FEF2F2", "7", "Closed Loop (End)", "LOOP")
    draw_card(1.0, 0.6, 4.4, 2.35, "Residual Error Tracking", "Measures real prediction error", [
        "Ground Truth Price (y) recorded",
        "Calculates error: e = y_actual - y_pred",
        "Detects sudden price shock & drift",
        "Guarantees data integrity"
    ], chips=[("Residuals", "#FEF2F2", "#DC2626"), ("Drift Check", "#FEF2F2", "#B91C1C")])

    draw_card(5.7, 0.6, 4.4, 2.35, "Walk-Forward Retraining", "Self-improving AI intelligence", [
        "Adds new actuals to training dataset",
        "Triggers periodic Random Forest retraining",
        "Refreshes vector embeddings for new mandi rules",
        "System gets SMARTER after every harvest!"
    ], chips=[("Retrain AI", "#FEF2F2", "#DC2626"), ("Continuous", "#FAF5FF", "#7E22CE")])

    # Connector from Day 4 down into Stage 6 (Ledger)
    draw_arrow(19.2, 4.1, 19.2, 3.6, "Realized Actuals", color=C_GREEN, lw=2.2)

    # Connector from Stage 6 left into Stage 7 (Closed Loop)
    draw_arrow(11.4, 1.8, 10.4, 1.8, "Verified Financials", color=C_RED, lw=2.2)

    # =========================================================================
    # THE CLOSED-LOOP ARROW (Clean outer path)
    # =========================================================================
    loop_pts_x = [0.8, 0.45, 0.45, 11.2, 11.2]
    loop_pts_y = [2.0, 2.0, 11.72, 11.72, 11.6]
    ax.plot(loop_pts_x, loop_pts_y, color=C_RED, linewidth=2.2, linestyle="--", zorder=20)
    
    arrow_retrain = patches.FancyArrowPatch((11.2, 11.72), (11.2, 11.6),
                                            arrowstyle="->", mutation_scale=18, color=C_RED, linewidth=2.2, zorder=22)
    ax.add_patch(arrow_retrain)

    # Label on the vertical run
    ax.text(0.45, 7.0, "CONTINUOUS CLOSED-LOOP RETRAINING (ELIMINATES MODEL DRIFT)",
            fontsize=8.5, fontweight='bold', color=C_RED, rotation=90,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF2F2", edgecolor=C_RED, lw=1.2),
            ha='center', va='center', zorder=25)

    plt.tight_layout()
    for p in OUT_PATHS:
        plt.savefig(p, bbox_inches='tight', dpi=300)
        print(f"Successfully Saved: {p}")
    plt.close()

if __name__ == "__main__":
    draw_visual_workflow()
