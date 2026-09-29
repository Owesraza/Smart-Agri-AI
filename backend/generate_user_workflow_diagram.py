#!/usr/bin/env python3
"""
Generates an executive-level, ultra-clean User Journey & Interaction Workflow Diagram
for CropPoint (Smart Agri AI), showing how Farmers and Buyers use the system.

Features:
- Dual Swimlanes: Farmer Journey (Top, Emerald) vs Buyer Journey (Bottom, Blue)
- 5 Clear Chronological Stages:
    Stage 1: Profile & Sourcing Criteria
    Stage 2: AI Intelligence & Marketplace Discovery
    Stage 3: Listing Creation & Purchase Request
    Stage 4: WhatsApp Negotiation & Deal Locking
    Stage 5: Fulfillment, Double-Entry Ledger & Settlement
- Central interaction arrows connecting Farmer and Buyer at every transaction touchpoint
- Closed-loop AI retraining feedback loop
- 16:9 widescreen 300 DPI high resolution
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI"
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

OUT_PATHS = [
    os.path.join(FIG_DIR, "CropPoint_User_Workflow_Farmer_Buyer.png"),
    os.path.join(BASE_DIR, "CropPoint_User_Workflow_Farmer_Buyer.png")
]

def draw_user_workflow():
    fig, ax = plt.subplots(figsize=(20, 11.25), dpi=300)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 11.25)
    ax.axis('off')

    # Main Canvas Background
    bg_canvas = patches.Rectangle((0, 0), 20, 11.25, facecolor="#F8FAFC", edgecolor="none", zorder=0)
    ax.add_patch(bg_canvas)

    # -------------------------------------------------------------
    # 1. HEADER SECTION
    # -------------------------------------------------------------
    header_box = patches.FancyBboxPatch((0.8, 10.10), 18.4, 0.85, boxstyle="round,pad=0.06,rounding_size=0.12",
                                        facecolor="#0F172A", edgecolor="#020617", linewidth=1.5, zorder=1)
    ax.add_patch(header_box)

    ax.text(10.0, 10.60, "CropPoint: End-to-End User Journey & Interaction Workflow",
            fontsize=17, fontweight='bold', color="#FFFFFF", ha='center', va='center', zorder=2)
    ax.text(10.0, 10.28, "Interactive Dual-Track Flow: How Farmers (Producers) & Buyers (Traders/Processors) Transact via AI Intelligence",
            fontsize=9.8, color="#94A3B8", ha='center', va='center', zorder=2)

    # -------------------------------------------------------------
    # 2. SWIMLANE SIDE INDICATORS
    # -------------------------------------------------------------
    # Farmer Lane Label (Top)
    farmer_tag = patches.FancyBboxPatch((0.8, 5.75), 0.75, 4.05, boxstyle="round,pad=0.04,rounding_size=0.10",
                                        facecolor="#064E3B", edgecolor="#059669", linewidth=1.5, zorder=2)
    ax.add_patch(farmer_tag)
    ax.text(1.17, 7.78, "FARMER JOURNEY  (SELLER)", rotation=90,
            fontsize=10.5, fontweight='bold', color="#6EE7B7", ha='center', va='center', zorder=3)

    # Buyer Lane Label (Bottom)
    buyer_tag = patches.FancyBboxPatch((0.8, 1.20), 0.75, 4.05, boxstyle="round,pad=0.04,rounding_size=0.10",
                                       facecolor="#1E3A8A", edgecolor="#2563EB", linewidth=1.5, zorder=2)
    ax.add_patch(buyer_tag)
    ax.text(1.17, 3.22, "BUYER JOURNEY  (PURCHASER)", rotation=90,
            fontsize=10.5, fontweight='bold', color="#93C5FD", ha='center', va='center', zorder=3)

    # -------------------------------------------------------------
    # 3. COLUMN DEFINITIONS (5 Chronological Stages)
    # -------------------------------------------------------------
    COL_X = [1.85, 5.30, 8.75, 12.20, 15.65]
    COL_W = 3.20
    CARD_H = 3.85
    FARMER_Y = 5.95
    BUYER_Y = 1.30

    STAGE_TITLES = [
        "STAGE 1: ONBOARDING & SETUP",
        "STAGE 2: AI INTEL & DISCOVERY",
        "STAGE 3: LISTING & ORDER BID",
        "STAGE 4: NEGOTIATION & CONTRACT",
        "STAGE 5: SETTLEMENT & LEDGER"
    ]

    # Stage header indicators above Farmer cards
    for idx, (cx, stitle) in enumerate(zip(COL_X, STAGE_TITLES)):
        s_pill = patches.FancyBboxPatch((cx, 9.85), COL_W, 0.28, boxstyle="round,pad=0.02,rounding_size=0.06",
                                        facecolor="#E2E8F0", edgecolor="#CBD5E1", linewidth=1.0, zorder=2)
        ax.add_patch(s_pill)
        ax.text(cx + COL_W / 2.0, 9.99, stitle, fontsize=8.0, fontweight='bold', color="#334155", ha='center', va='center', zorder=3)

    # -------------------------------------------------------------
    # 4. CARD DRAWING FUNCTION
    # -------------------------------------------------------------
    def draw_user_card(x, y, w, h, step_tag, role_color, light_bg, border_col, title, subtitle, bullets, chips):
        # Shadow
        shadow = patches.FancyBboxPatch((x + 0.04, y - 0.04), w, h, boxstyle="round,pad=0.05,rounding_size=0.12",
                                        facecolor="#E2E8F0", edgecolor="none", zorder=1)
        ax.add_patch(shadow)

        # Main Card Body
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.12",
                                      facecolor="#FFFFFF", edgecolor=border_col, linewidth=1.8, zorder=2)
        ax.add_patch(card)

        # Header Pill
        hpill = patches.FancyBboxPatch((x + 0.15, y + h - 0.70), w - 0.30, 0.55, boxstyle="round,pad=0.03,rounding_size=0.08",
                                       facecolor=light_bg, edgecolor=border_col, linewidth=1.0, zorder=3)
        ax.add_patch(hpill)

        # Step Badge
        sbadge = patches.FancyBboxPatch((x + 0.25, y + h - 0.45), 0.75, 0.26, boxstyle="round,pad=0.02,rounding_size=0.06",
                                        facecolor=role_color, edgecolor="none", zorder=4)
        ax.add_patch(sbadge)
        ax.text(x + 0.625, y + h - 0.32, step_tag, fontsize=7.5, fontweight='bold', color="#FFFFFF", ha='center', va='center', zorder=5)

        # Title & Subtitle
        ax.text(x + 1.10, y + h - 0.30, title, fontsize=9.8, fontweight='bold', color="#0F172A", va='center', zorder=5)
        ax.text(x + 1.10, y + h - 0.52, subtitle, fontsize=7.6, color="#64748B", fontstyle='italic', va='center', zorder=5)

        # Bullet Points
        by = y + h - 1.00
        for b in bullets:
            dot = patches.Circle((x + 0.30, by), 0.045, facecolor=role_color, edgecolor="none", zorder=4)
            ax.add_patch(dot)
            ax.text(x + 0.45, by, b, fontsize=8.2, color="#1E293B", va='center', zorder=4)
            by -= 0.38

        # Bottom Tech / Feature Chips
        cx = x + 0.22
        chip_y = y + 0.32
        for c in chips:
            cw = len(c) * 0.058 + 0.22
            cp = patches.FancyBboxPatch((cx, chip_y - 0.13), cw, 0.26, boxstyle="round,pad=0.02,rounding_size=0.06",
                                        facecolor=light_bg, edgecolor=border_col, linewidth=0.7, zorder=4)
            ax.add_patch(cp)
            ax.text(cx + cw / 2.0, chip_y, c, fontsize=7.0, fontweight='bold', color=role_color, ha='center', va='center', zorder=5)
            cx += cw + 0.12

    # -------------------------------------------------------------
    # 5. RENDER FARMER CARDS (TOP ROW)
    # -------------------------------------------------------------
    F_COLOR = "#059669"
    F_LIGHT = "#ECFDF5"
    F_BORDER = "#10B981"

    # F1
    draw_user_card(
        x=COL_X[0], y=FARMER_Y, w=COL_W, h=CARD_H,
        step_tag="STEP F1", role_color=F_COLOR, light_bg=F_LIGHT, border_col=F_BORDER,
        title="Crop & Harvest Setup",
        subtitle="Registers expected yield",
        bullets=[
            "Selects commodity (Wheat, Tomato, Onion)",
            "Enters expected harvest volume (quintals)",
            "Specifies district & farm gate location",
            "Uploads harvest readiness date"
        ],
        chips=["Farmer Auth", "Crop Profile", "Yield Metric"]
    )

    # F2
    draw_user_card(
        x=COL_X[1], y=FARMER_Y, w=COL_W, h=CARD_H,
        step_tag="STEP F2", role_color=F_COLOR, light_bg=F_LIGHT, border_col=F_BORDER,
        title="AI Advisory & Timing",
        subtitle="Predictive market window",
        bullets=[
            "Reviews 7 & 14-day RF price forecasts",
            "Compares mandi rates across APMC centers",
            "Receives recommendation: SELL NOW or WAIT",
            "Checks spoilage risk and storage cost model"
        ],
        chips=["RF Regressor", "Mandi Compare", "SELL/WAIT"]
    )

    # F3
    draw_user_card(
        x=COL_X[2], y=FARMER_Y, w=COL_W, h=CARD_H,
        step_tag="STEP F3", role_color=F_COLOR, light_bg=F_LIGHT, border_col=F_BORDER,
        title="Post Crop Listing",
        subtitle="Publish batch to marketplace",
        bullets=[
            "Sets batch quantity, quality grade & photos",
            "Inputs reserve price guided by AI benchmark",
            "Activates listing visible to verified buyers",
            "Monitors real-time buyer view interest"
        ],
        chips=["Fair Price Tag", "Grade Standards", "Live Listing"]
    )

    # F4
    draw_user_card(
        x=COL_X[3], y=FARMER_Y, w=COL_W, h=CARD_H,
        step_tag="STEP F4", role_color=F_COLOR, light_bg=F_LIGHT, border_col=F_BORDER,
        title="Review Offers & Chat",
        subtitle="WhatsApp deal negotiation",
        bullets=[
            "Receives real-time buyer purchase alerts",
            "Reviews offered price per quintal & terms",
            "Opens direct WhatsApp channel with buyer",
            "Accepts optimal offer & locks digital deal"
        ],
        chips=["Push Alert", "WhatsApp Direct", "Lock Deal"]
    )

    # F5 (Settlement & Ledger)
    draw_user_card(
        x=COL_X[4], y=FARMER_Y, w=COL_W, h=CARD_H,
        step_tag="STEP F5", role_color="#0D9488", light_bg="#F0FDFA", border_col="#14B8A6",
        title="Dispatch & Net Profit",
        subtitle="Execution & digital ledger",
        bullets=[
            "Executes 4-day phased dispatch schedule",
            "Transfers produce upon arrival inspection",
            "Receives automated bank transfer / payout",
            "Ledger computes net margin after transport"
        ],
        chips=["4-Day Plan", "Bank Payout", "Net Margin"]
    )

    # -------------------------------------------------------------
    # 6. RENDER BUYER CARDS (BOTTOM ROW)
    # -------------------------------------------------------------
    B_COLOR = "#2563EB"
    B_LIGHT = "#EFF6FF"
    B_BORDER = "#3B82F6"

    # B1
    draw_user_card(
        x=COL_X[0], y=BUYER_Y, w=COL_W, h=CARD_H,
        step_tag="STEP B1", role_color=B_COLOR, light_bg=B_LIGHT, border_col=B_BORDER,
        title="Profile & Sourcing Needs",
        subtitle="Demand & procurement criteria",
        bullets=[
            "Registers as Wholesaler, Processor or Retailer",
            "Sets target commodity requirements",
            "Defines recurring weekly procurement volume",
            "Configures sourcing radius & logistics hub"
        ],
        chips=["Buyer KYC", "Volume Quota", "GST Profile"]
    )

    # B2
    draw_user_card(
        x=COL_X[1], y=BUYER_Y, w=COL_W, h=CARD_H,
        step_tag="STEP B2", role_color=B_COLOR, light_bg=B_LIGHT, border_col=B_BORDER,
        title="Marketplace Discovery",
        subtitle="Search verified farm batches",
        bullets=[
            "Explores live listings filtered by district & grade",
            "Compares farmer asking rates against AI benchmark",
            "Evaluates harvest readiness & distance to hub",
            "Shortlists verified producer batches"
        ],
        chips=["Geo Search", "AI Price Guide", "Grade Filter"]
    )

    # B3
    draw_user_card(
        x=COL_X[2], y=BUYER_Y, w=COL_W, h=CARD_H,
        step_tag="STEP B3", role_color=B_COLOR, light_bg=B_LIGHT, border_col=B_BORDER,
        title="Submit Purchase Bid",
        subtitle="Formal procurement request",
        bullets=[
            "Selects required quantity (e.g. 50 quintals)",
            "Submits unit bid price (Rs/quintal)",
            "Specifies required delivery / pickup window",
            "Commits purchase request to system queue"
        ],
        chips=["Order Bid", "Volume Quota", "Delivery Date"]
    )

    # B4
    draw_user_card(
        x=COL_X[3], y=BUYER_Y, w=COL_W, h=CARD_H,
        step_tag="STEP B4", role_color=B_COLOR, light_bg=B_LIGHT, border_col=B_BORDER,
        title="Contract Agreement",
        subtitle="Terms finalized on WhatsApp",
        bullets=[
            "Direct WhatsApp chat to confirm quality & moisture",
            "Agrees on freight: farm pickup vs mandi delivery",
            "Formalizes contract terms and payment mode",
            "Secures allocation in active deal tracker"
        ],
        chips=["WhatsApp Chat", "Terms Agreed", "Deal Active"]
    )

    # B5
    draw_user_card(
        x=COL_X[4], y=BUYER_Y, w=COL_W, h=CARD_H,
        step_tag="STEP B5", role_color="#4F46E5", light_bg="#EEF2FF", border_col="#6366F1",
        title="Receipt, Invoice & Rating",
        subtitle="Inspection & transaction close",
        bullets=[
            "Inspects batch weight and quality at handover",
            "Signs digital delivery receipt & releases escrow",
            "Downloads verified GST digital tax invoice",
            "Rates farmer reliability (1 to 5 stars)"
        ],
        chips=["Handover Sign", "GST Invoice", "5-Star Rating"]
    )

    # -------------------------------------------------------------
    # 7. HORIZONTAL PROGRESSION ARROWS (Within each lane)
    # -------------------------------------------------------------
    arrow_style = dict(arrowstyle="-|>", mutation_scale=16, linewidth=2.0)

    # Farmer Lane Arrows (Left to Right)
    for i in range(4):
        ax.annotate("", xy=(COL_X[i+1] - 0.05, FARMER_Y + CARD_H/2.0),
                    xytext=(COL_X[i] + COL_W + 0.05, FARMER_Y + CARD_H/2.0),
                    arrowprops=dict(**arrow_style, color="#059669"), zorder=6)

    # Buyer Lane Arrows (Left to Right)
    for i in range(4):
        ax.annotate("", xy=(COL_X[i+1] - 0.05, BUYER_Y + CARD_H/2.0),
                    xytext=(COL_X[i] + COL_W + 0.05, BUYER_Y + CARD_H/2.0),
                    arrowprops=dict(**arrow_style, color="#2563EB"), zorder=6)

    # -------------------------------------------------------------
    # 8. CENTRAL INTERACTION CONNECTORS (Farmer <-> Buyer Touchpoints)
    # -------------------------------------------------------------
    # Central interaction banner background
    center_bar = patches.FancyBboxPatch((1.85, 5.25), 17.0, 0.55, boxstyle="round,pad=0.03,rounding_size=0.08",
                                        facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=1.2, zorder=2)
    ax.add_patch(center_bar)
    ax.text(1.95, 5.525, "CENTRAL PLATFORM NEXUS: REAL-TIME COLLABORATIVE TOUCHPOINTS",
            fontsize=8.2, fontweight='bold', color="#92400E", va='center', zorder=3)

    # Interaction 1: Listing published (F3) -> Discovered on Marketplace (B2)
    ax.annotate("", xy=(COL_X[1] + COL_W * 0.75, BUYER_Y + CARD_H + 0.02),
                xytext=(COL_X[2] + COL_W * 0.25, FARMER_Y - 0.02),
                arrowprops=dict(arrowstyle="<|-|>", mutation_scale=14, linewidth=2.0,
                                color="#D97706", linestyle="--"), zorder=7)
    tag1 = patches.FancyBboxPatch((7.10, 5.32), 1.90, 0.40, boxstyle="round,pad=0.02,rounding_size=0.06",
                                  facecolor="#FFFFFF", edgecolor="#D97706", linewidth=1.0, zorder=8)
    ax.add_patch(tag1)
    ax.text(8.05, 5.52, "Marketplace Sync", fontsize=7.2, fontweight='bold', color="#B45309", ha='center', va='center', zorder=9)

    # Interaction 2: Buyer submits bid (B3) -> Alerts Farmer (F4)
    ax.annotate("", xy=(COL_X[3] + COL_W * 0.25, FARMER_Y - 0.02),
                xytext=(COL_X[2] + COL_W * 0.75, BUYER_Y + CARD_H + 0.02),
                arrowprops=dict(arrowstyle="<|-|>", mutation_scale=14, linewidth=2.0,
                                color="#D97706", linestyle="--"), zorder=7)
    tag2 = patches.FancyBboxPatch((10.55, 5.32), 1.90, 0.40, boxstyle="round,pad=0.02,rounding_size=0.06",
                                  facecolor="#FFFFFF", edgecolor="#D97706", linewidth=1.0, zorder=8)
    ax.add_patch(tag2)
    ax.text(11.50, 5.52, "Purchase Order Alert", fontsize=7.2, fontweight='bold', color="#B45309", ha='center', va='center', zorder=9)

    # Interaction 3: Mutual WhatsApp Negotiation (F4 <-> B4)
    ax.annotate("", xy=(COL_X[3] + COL_W * 0.70, BUYER_Y + CARD_H + 0.02),
                xytext=(COL_X[3] + COL_W * 0.70, FARMER_Y - 0.02),
                arrowprops=dict(arrowstyle="<|-|>", mutation_scale=14, linewidth=2.2,
                                color="#16A34A"), zorder=7)
    tag3 = patches.FancyBboxPatch((13.80, 5.32), 1.95, 0.40, boxstyle="round,pad=0.02,rounding_size=0.06",
                                  facecolor="#DCFCE7", edgecolor="#16A34A", linewidth=1.2, zorder=8)
    ax.add_patch(tag3)
    ax.text(14.77, 5.52, "WhatsApp Direct Deal", fontsize=7.2, fontweight='bold', color="#166534", ha='center', va='center', zorder=9)

    # Interaction 4: Handover, Escrow & Double-Entry Ledger (F5 <-> B5)
    ax.annotate("", xy=(COL_X[4] + COL_W * 0.50, BUYER_Y + CARD_H + 0.02),
                xytext=(COL_X[4] + COL_W * 0.50, FARMER_Y - 0.02),
                arrowprops=dict(arrowstyle="<|-|>", mutation_scale=14, linewidth=2.2,
                                color="#7C3AED"), zorder=7)
    tag4 = patches.FancyBboxPatch((16.45, 5.32), 2.30, 0.40, boxstyle="round,pad=0.02,rounding_size=0.06",
                                  facecolor="#F5F3FF", edgecolor="#7C3AED", linewidth=1.2, zorder=8)
    ax.add_patch(tag4)
    ax.text(17.60, 5.52, "Escrow & Double-Entry Ledger", fontsize=7.0, fontweight='bold', color="#5B21B6", ha='center', va='center', zorder=9)

    # -------------------------------------------------------------
    # 9. CLOSED-LOOP FEEDBACK ARROW (Bottom to AI Brain)
    # -------------------------------------------------------------
    feedback_box = patches.FancyBboxPatch((0.8, 0.28), 18.4, 0.62, boxstyle="round,pad=0.04,rounding_size=0.10",
                                          facecolor="#FEF2F2", edgecolor="#DC2626", linewidth=1.2, zorder=2)
    ax.add_patch(feedback_box)

    ax.text(1.10, 0.59, "CLOSED-LOOP FEEDBACK: Realized settlement price & quality rating automatically feed back into AI retraining pipeline",
            fontsize=8.5, fontweight='bold', color="#991B1B", va='center', zorder=3)
    ax.text(18.90, 0.59, "Walk-Forward Continuous Retraining Engine (Zero Data Drift)",
            fontsize=8.2, color="#B91C1C", fontstyle='italic', ha='right', va='center', zorder=3)

    plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)

    for path in OUT_PATHS:
        fig.savefig(path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        print(f"[OK] Saved workflow diagram to: {path}")

    plt.close(fig)

if __name__ == "__main__":
    draw_user_workflow()
