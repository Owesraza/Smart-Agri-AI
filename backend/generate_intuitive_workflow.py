#!/usr/bin/env python3
"""
Generates an ultra-intuitive, guide-friendly, executive-level System Workflow Matrix
for CropPoint (Smart Agri AI).

Layout:
- 5 Chronological Stages (Columns 1 to 5)
- 3 Clear Functional Tiers:
    Tier 1 (Top):    FARMER JOURNEY (Emerald Theme)
    Tier 2 (Middle): CROPPOINT AI PLATFORM & BRAIN (Dark Slate / Gold / Violet Theme)
    Tier 3 (Bottom): BUYER JOURNEY (Sapphire Blue Theme)
- Clean vertical interaction arrows showing how the AI Platform bridges Farmer & Buyer
- Continuous closed-loop feedback banner at the bottom
- 16:9 widescreen 300 DPI high resolution
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI"
FIG_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

OUT_PATHS = [
    os.path.join(BASE_DIR, "CropPoint_System_Workflow_Matrix.png"),
    os.path.join(FIG_DIR, "CropPoint_System_Workflow_Matrix.png"),
    os.path.join(BASE_DIR, "CropPoint_User_Workflow_Farmer_Buyer.png"),
    os.path.join(FIG_DIR, "CropPoint_User_Workflow_Farmer_Buyer.png")
]

def draw_intuitive_workflow():
    fig, ax = plt.subplots(figsize=(20, 11.25), dpi=300)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 11.25)
    ax.axis('off')

    # Background Canvas
    bg_canvas = patches.Rectangle((0, 0), 20, 11.25, facecolor="#F8FAFC", edgecolor="none", zorder=0)
    ax.add_patch(bg_canvas)

    # -------------------------------------------------------------
    # 1. HEADER SECTION
    # -------------------------------------------------------------
    header_box = patches.FancyBboxPatch((0.8, 10.15), 18.4, 0.82, boxstyle="round,pad=0.06,rounding_size=0.12",
                                        facecolor="#0F172A", edgecolor="#020617", linewidth=1.5, zorder=1)
    ax.add_patch(header_box)

    ax.text(10.0, 10.63, "CropPoint: End-to-End System & User Interaction Matrix",
            fontsize=17, fontweight='bold', color="#FFFFFF", ha='center', va='center', zorder=2)
    ax.text(10.0, 10.33, "How Farmers & Buyers Transact Seamlessly Through the CropPoint Autonomous AI Platform",
            fontsize=10.0, color="#94A3B8", ha='center', va='center', zorder=2)

    # -------------------------------------------------------------
    # 2. COLUMN DIMENSIONS & STAGE HEADERS
    # -------------------------------------------------------------
    COL_W = 3.50
    GAP = 0.225
    START_X = 0.80
    COL_X = [START_X + i * (COL_W + GAP) for i in range(5)]

    STAGE_INFO = [
        ("STAGE 1", "ONBOARDING & SETUP"),
        ("STAGE 2", "AI INTEL & DISCOVERY"),
        ("STAGE 3", "LISTING & ORDER BID"),
        ("STAGE 4", "NEGOTIATION & CONTRACT"),
        ("STAGE 5", "SETTLEMENT & RETRAINING")
    ]

    # Draw Stage Headers
    for i, (cx, (stag, sname)) in enumerate(zip(COL_X, STAGE_INFO)):
        spill = patches.FancyBboxPatch((cx, 9.72), COL_W, 0.32, boxstyle="round,pad=0.03,rounding_size=0.08",
                                       facecolor="#1E293B", edgecolor="#334155", linewidth=1.0, zorder=2)
        ax.add_patch(spill)
        ax.text(cx + 0.15, 9.88, stag, fontsize=8.0, fontweight='bold', color="#38BDF8", va='center', zorder=3)
        ax.text(cx + COL_W - 0.15, 9.88, sname, fontsize=7.8, fontweight='bold', color="#F8FAFC", ha='right', va='center', zorder=3)

    # -------------------------------------------------------------
    # 3. Y-COORDINATES FOR THE THREE TIERS
    # -------------------------------------------------------------
    FARMER_Y = 6.90
    FARMER_H = 2.65

    SYSTEM_Y = 4.05
    SYSTEM_H = 2.45

    BUYER_Y = 1.05
    BUYER_H = 2.65

    # -------------------------------------------------------------
    # 4. CARD DRAWING HELPERS
    # -------------------------------------------------------------
    def draw_card(x, y, w, h, role_tag, tag_bg, tag_text_col, border_col, card_bg, title, bullets, chip_text):
        # Shadow
        shadow = patches.FancyBboxPatch((x + 0.04, y - 0.04), w, h, boxstyle="round,pad=0.04,rounding_size=0.10",
                                        facecolor="#E2E8F0", edgecolor="none", zorder=1)
        ax.add_patch(shadow)

        # Card
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.10",
                                      facecolor=card_bg, edgecolor=border_col, linewidth=1.8, zorder=2)
        ax.add_patch(card)

        # Role Tag Pill
        rpill = patches.FancyBboxPatch((x + 0.15, y + h - 0.40), len(role_tag) * 0.075 + 0.30, 0.26,
                                       boxstyle="round,pad=0.02,rounding_size=0.06",
                                       facecolor=tag_bg, edgecolor="none", zorder=3)
        ax.add_patch(rpill)
        ax.text(x + 0.15 + (len(role_tag) * 0.075 + 0.30)/2.0, y + h - 0.27, role_tag,
                fontsize=7.2, fontweight='bold', color=tag_text_col, ha='center', va='center', zorder=4)

        # Title
        ax.text(x + 0.15, y + h - 0.65, title, fontsize=10.0, fontweight='bold', color="#0F172A", va='center', zorder=4)

        # Bullets
        by = y + h - 1.00
        for b in bullets:
            dot = patches.Circle((x + 0.28, by), 0.04, facecolor=border_col, edgecolor="none", zorder=4)
            ax.add_patch(dot)
            ax.text(x + 0.42, by, b, fontsize=8.2, color="#334155", va='center', zorder=4)
            by -= 0.38

        # Bottom Chip
        cp = patches.FancyBboxPatch((x + 0.15, y + 0.18), w - 0.30, 0.30,
                                    boxstyle="round,pad=0.02,rounding_size=0.06",
                                    facecolor="#FFFFFF", edgecolor=border_col, linewidth=0.9, zorder=3)
        ax.add_patch(cp)
        ax.text(x + w / 2.0, y + 0.33, chip_text, fontsize=7.2, fontweight='bold', color=border_col, ha='center', va='center', zorder=4)

    def draw_system_card(x, y, w, h, title, bullets, tech_tag):
        # Shadow
        shadow = patches.FancyBboxPatch((x + 0.04, y - 0.04), w, h, boxstyle="round,pad=0.04,rounding_size=0.10",
                                        facecolor="#E2E8F0", edgecolor="none", zorder=1)
        ax.add_patch(shadow)

        # Card
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.10",
                                      facecolor="#0F172A", edgecolor="#F59E0B", linewidth=1.8, zorder=2)
        ax.add_patch(card)

        # System Tag
        ax.text(x + 0.18, y + h - 0.28, "⚡ CROPPOINT AI PLATFORM",
                fontsize=7.2, fontweight='bold', color="#F59E0B", va='center', zorder=4)

        # Title
        ax.text(x + 0.18, y + h - 0.60, title, fontsize=9.6, fontweight='bold', color="#FFFFFF", va='center', zorder=4)

        # Bullets
        by = y + h - 0.95
        for b in bullets:
            dot = patches.Circle((x + 0.28, by), 0.04, facecolor="#F59E0B", edgecolor="none", zorder=4)
            ax.add_patch(dot)
            ax.text(x + 0.42, by, b, fontsize=8.0, color="#CBD5E1", va='center', zorder=4)
            by -= 0.36

        # Bottom Tech Tag
        cp = patches.FancyBboxPatch((x + 0.15, y + 0.18), w - 0.30, 0.28,
                                    boxstyle="round,pad=0.02,rounding_size=0.06",
                                    facecolor="#1E293B", edgecolor="#475569", linewidth=0.8, zorder=3)
        ax.add_patch(cp)
        ax.text(x + w / 2.0, y + 0.32, tech_tag, fontsize=7.0, fontweight='bold', color="#38BDF8", ha='center', va='center', zorder=4)

    # -------------------------------------------------------------
    # 5. RENDER STAGE 1
    # -------------------------------------------------------------
    # Farmer 1
    draw_card(
        x=COL_X[0], y=FARMER_Y, w=COL_W, h=FARMER_H,
        role_tag="FARMER (PRODUCER)", tag_bg="#059669", tag_text_col="#FFFFFF",
        border_col="#059669", card_bg="#F0FDF4",
        title="1. Register Crop Batch",
        bullets=[
            "Selects crop (Wheat, Tomato, Onion)",
            "Enters harvest volume in quintals",
            "Specifies district & harvest date"
        ],
        chip_text="Crop Profile  •  Volume Metric"
    )

    # System 1
    draw_system_card(
        x=COL_X[0], y=SYSTEM_Y, w=COL_W, h=SYSTEM_H,
        title="1. Ingestion & Preprocessing",
        bullets=[
            "Pulls live APMC mandi data via AGMARKNET",
            "Fetches local weather & spoilage risk",
            "Cleanses features for time-series model"
        ],
        tech_tag="AGMARKNET API  •  OpenWeather"
    )

    # Buyer 1
    draw_card(
        x=COL_X[0], y=BUYER_Y, w=COL_W, h=BUYER_H,
        role_tag="BUYER (PURCHASER)", tag_bg="#2563EB", tag_text_col="#FFFFFF",
        border_col="#2563EB", card_bg="#EFF6FF",
        title="1. Define Sourcing Needs",
        bullets=[
            "Registers as Wholesaler / Processor",
            "Sets target commodity requirements",
            "Defines weekly procurement quota"
        ],
        chip_text="Buyer KYC  •  Procurement Target"
    )

    # -------------------------------------------------------------
    # 6. RENDER STAGE 2
    # -------------------------------------------------------------
    # Farmer 2
    draw_card(
        x=COL_X[1], y=FARMER_Y, w=COL_W, h=FARMER_H,
        role_tag="FARMER (PRODUCER)", tag_bg="#059669", tag_text_col="#FFFFFF",
        border_col="#059669", card_bg="#F0FDF4",
        title="2. Consult AI Advisory",
        bullets=[
            "Views 7 & 14-day price forecasts",
            "Compares mandi rates across APMC",
            "Receives verdict: SELL NOW or WAIT"
        ],
        chip_text="RF Price Forecast  •  SELL / WAIT"
    )

    # System 2
    draw_system_card(
        x=COL_X[1], y=SYSTEM_Y, w=COL_W, h=SYSTEM_H,
        title="2. Predictive Brain Engine",
        bullets=[
            "Random Forest Regressor (R²=0.9687)",
            "FAISS vector store & Gemini RAG",
            "6-factor decision & profit optimization"
        ],
        tech_tag="Random Forest  •  FAISS  •  Gemini"
    )

    # Buyer 2
    draw_card(
        x=COL_X[1], y=BUYER_Y, w=COL_W, h=BUYER_H,
        role_tag="BUYER (PURCHASER)", tag_bg="#2563EB", tag_text_col="#FFFFFF",
        border_col="#2563EB", card_bg="#EFF6FF",
        title="2. Browse Verified Market",
        bullets=[
            "Explores active listings filtered by district",
            "Compares asking price to AI benchmark",
            "Inspects quality grade & harvest date"
        ],
        chip_text="Direct Marketplace  •  AI Fair Price"
    )

    # -------------------------------------------------------------
    # 7. RENDER STAGE 3
    # -------------------------------------------------------------
    # Farmer 3
    draw_card(
        x=COL_X[2], y=FARMER_Y, w=COL_W, h=FARMER_H,
        role_tag="FARMER (PRODUCER)", tag_bg="#059669", tag_text_col="#FFFFFF",
        border_col="#059669", card_bg="#F0FDF4",
        title="3. Post Crop Listing",
        bullets=[
            "Inputs batch quantity, grade & photos",
            "Sets fair reserve price guided by AI",
            "Publishes listing live to verified buyers"
        ],
        chip_text="Verified Listing  •  Reserve Price"
    )

    # System 3
    draw_system_card(
        x=COL_X[2], y=SYSTEM_Y, w=COL_W, h=SYSTEM_H,
        title="3. Matchmaking & Dispatch",
        bullets=[
            "Matches farmer produce with buyer quotas",
            "Ranks listings by distance & grade score",
            "Sends real-time push alert to parties"
        ],
        tech_tag="Matching Engine  •  FastAPI Alerts"
    )

    # Buyer 3
    draw_card(
        x=COL_X[2], y=BUYER_Y, w=COL_W, h=BUYER_H,
        role_tag="BUYER (PURCHASER)", tag_bg="#2563EB", tag_text_col="#FFFFFF",
        border_col="#2563EB", card_bg="#EFF6FF",
        title="3. Submit Purchase Bid",
        bullets=[
            "Selects desired quantity from batch",
            "Submits formal offer price (Rs/quintal)",
            "Specifies target delivery / pickup date"
        ],
        chip_text="Purchase Request  •  Volume Bid"
    )

    # -------------------------------------------------------------
    # 8. RENDER STAGE 4
    # -------------------------------------------------------------
    # Farmer 4
    draw_card(
        x=COL_X[3], y=FARMER_Y, w=COL_W, h=FARMER_H,
        role_tag="FARMER (PRODUCER)", tag_bg="#059669", tag_text_col="#FFFFFF",
        border_col="#059669", card_bg="#F0FDF4",
        title="4. Review Offer & Chat",
        bullets=[
            "Receives buyer purchase request alert",
            "Opens 1-click verified WhatsApp chat",
            "Accepts optimal offer & locks deal"
        ],
        chip_text="WhatsApp Direct  •  Deal Accepted"
    )

    # System 4
    draw_system_card(
        x=COL_X[3], y=SYSTEM_Y, w=COL_W, h=SYSTEM_H,
        title="4. WhatsApp Bridge & Escrow",
        bullets=[
            "Generates pre-filled WhatsApp deep-link",
            "Formalizes digital terms & order status",
            "Secures transaction in escrow state"
        ],
        tech_tag="WhatsApp API  •  Smart Escrow"
    )

    # Buyer 4
    draw_card(
        x=COL_X[3], y=BUYER_Y, w=COL_W, h=BUYER_H,
        role_tag="BUYER (PURCHASER)", tag_bg="#2563EB", tag_text_col="#FFFFFF",
        border_col="#2563EB", card_bg="#EFF6FF",
        title="4. Finalize Deal Terms",
        bullets=[
            "Direct chat with farmer on produce samples",
            "Confirms logistics: farm-gate or mandi",
            "Locks contract terms & escrow deposit"
        ],
        chip_text="WhatsApp Negotiation  •  Escrow Lock"
    )

    # -------------------------------------------------------------
    # 9. RENDER STAGE 5
    # -------------------------------------------------------------
    # Farmer 5
    draw_card(
        x=COL_X[4], y=FARMER_Y, w=COL_W, h=FARMER_H,
        role_tag="FARMER (PRODUCER)", tag_bg="#0D9488", tag_text_col="#FFFFFF",
        border_col="#0D9488", card_bg="#F0FDFA",
        title="5. Dispatch & Net Profit",
        bullets=[
            "Follows 4-day phased logistics plan",
            "Signs handover upon arrival inspection",
            "Receives instant payout; net margin logged"
        ],
        chip_text="4-Day Dispatch  •  Direct Payout"
    )

    # System 5
    draw_system_card(
        x=COL_X[4], y=SYSTEM_Y, w=COL_W, h=SYSTEM_H,
        title="5. Double-Entry & Retrain",
        bullets=[
            "Double-Entry: Revenue - Transport = Profit",
            "Generates digital GST tax invoice",
            "Feeds actual sale price into retraining"
        ],
        tech_tag="Double-Entry Ledger  •  Retrain Loop"
    )

    # Buyer 5
    draw_card(
        x=COL_X[4], y=BUYER_Y, w=COL_W, h=BUYER_H,
        role_tag="BUYER (PURCHASER)", tag_bg="#4F46E5", tag_text_col="#FFFFFF",
        border_col="#4F46E5", card_bg="#EEF2FF",
        title="5. Inspection & Receipt",
        bullets=[
            "Inspects batch weight & quality grade",
            "Signs delivery receipt & releases escrow",
            "Downloads GST invoice & rates farmer"
        ],
        chip_text="Quality Sign-off  •  GST Invoice"
    )

    # -------------------------------------------------------------
    # 10. CONNECTING ARROWS & FLOW
    # -------------------------------------------------------------
    # Horizontal Stage Progression Arrows across Tier 1 (Farmer)
    for i in range(4):
        ax.annotate("", xy=(COL_X[i+1] - 0.04, FARMER_Y + FARMER_H/2.0),
                    xytext=(COL_X[i] + COL_W + 0.04, FARMER_Y + FARMER_H/2.0),
                    arrowprops=dict(arrowstyle="-|>", mutation_scale=15, linewidth=2.0, color="#059669"), zorder=5)

    # Horizontal Stage Progression Arrows across Tier 2 (System)
    for i in range(4):
        ax.annotate("", xy=(COL_X[i+1] - 0.04, SYSTEM_Y + SYSTEM_H/2.0),
                    xytext=(COL_X[i] + COL_W + 0.04, SYSTEM_Y + SYSTEM_H/2.0),
                    arrowprops=dict(arrowstyle="-|>", mutation_scale=15, linewidth=2.0, color="#F59E0B"), zorder=5)

    # Horizontal Stage Progression Arrows across Tier 3 (Buyer)
    for i in range(4):
        ax.annotate("", xy=(COL_X[i+1] - 0.04, BUYER_Y + BUYER_H/2.0),
                    xytext=(COL_X[i] + COL_W + 0.04, BUYER_Y + BUYER_H/2.0),
                    arrowprops=dict(arrowstyle="-|>", mutation_scale=15, linewidth=2.0, color="#2563EB"), zorder=5)

    # Vertical Interaction Arrows (Farmer <-> System <-> Buyer)
    for i in range(5):
        mid_x = COL_X[i] + COL_W / 2.0
        
        # Farmer <-> System
        ax.annotate("", xy=(mid_x, SYSTEM_Y + SYSTEM_H + 0.03),
                    xytext=(mid_x, FARMER_Y - 0.03),
                    arrowprops=dict(arrowstyle="<|-|>", mutation_scale=13, linewidth=1.8, color="#059669", linestyle="-"), zorder=6)
        
        # System <-> Buyer
        ax.annotate("", xy=(mid_x, BUYER_Y + BUYER_H + 0.03),
                    xytext=(mid_x, SYSTEM_Y - 0.03),
                    arrowprops=dict(arrowstyle="<|-|>", mutation_scale=13, linewidth=1.8, color="#2563EB", linestyle="-"), zorder=6)

    # -------------------------------------------------------------
    # 11. CLOSED-LOOP FEEDBACK BANNER (Bottom)
    # -------------------------------------------------------------
    retrain_box = patches.FancyBboxPatch((0.8, 0.22), 18.4, 0.65, boxstyle="round,pad=0.04,rounding_size=0.10",
                                         facecolor="#FEF2F2", edgecolor="#DC2626", linewidth=1.5, zorder=2)
    ax.add_patch(retrain_box)

    ax.text(1.10, 0.545, "CLOSED-LOOP FEEDBACK RETRAINING:",
            fontsize=8.8, fontweight='bold', color="#DC2626", va='center', zorder=3)
    ax.text(4.75, 0.545, "Actual settled mandi prices & transaction ratings automatically feed back into the Random Forest model to eliminate data drift.",
            fontsize=8.4, color="#991B1B", va='center', zorder=3)
    ax.text(18.90, 0.545, "WALK-FORWARD RETRAINING ENGINE (ZERO DRIFT)",
            fontsize=8.2, fontweight='bold', color="#DC2626", ha='right', va='center', zorder=3)

    plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)

    for path in OUT_PATHS:
        fig.savefig(path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
        print(f"[OK] Saved intuitive workflow matrix to: {path}")

    plt.close(fig)

if __name__ == "__main__":
    draw_intuitive_workflow()
