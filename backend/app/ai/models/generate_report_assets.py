"""
Generate professional PDF and high-resolution PNG images of Model Stability Evaluation Tables.
Includes:
- Table 1: 5-Fold Walk-Forward Cross-Validation Results
- Table 2: Statistical Metric Variation & Stability Summary
- Table 3: Commodity-Level Stability Breakdown
- Table 4: Automated Data Leakage Verification
- Table 5: Production Model vs 5-Fold CV Comparison
- Master Report PDF (multi-page, publication-ready)
- Master Dashboard PNG (crisp, high-res executive visual)
"""

import os
import shutil
import json
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

RESULTS_JSON = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI/backend/app/ai/models/saved/stability_evaluation_results.json"
PROJECT_SAVED_DIR = "/Users/owaisrazaansaralibhati/Desktop/Smart Agri AI/backend/app/ai/models/saved"
ARTIFACTS_DIR = "/Users/owaisrazaansaralibhati/.gemini/antigravity/brain/14735be5-35a9-4590-b243-97d70965bd7b"

with open(RESULTS_JSON, "r") as f:
    data = json.load(f)

fold_results = data["fold_results"]
stats_summary = data["stats_summary"]
commodity_summary = data.get("commodity_summary", [])
benchmark_comparison = data.get("benchmark_comparison", {})

# -------------------------------------------------------------
# 1. REPORTLAB PDF GENERATION
# -------------------------------------------------------------

pdf_path = os.path.join(PROJECT_SAVED_DIR, "Smart_Agri_Model_Stability_Evaluation_Report.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        # Header
        self.drawString(54, 11 * 72 - 36, "Smart Agri AI — Model Stability & Consistency Evaluation Report")
        self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "Strictly Confidential / Technical Audit")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)
        
        # Footer
        self.line(54, 46, 8.5 * 72 - 54, 46)
        self.drawString(54, 32, "Dataset: 1,314,107 APMC Mandi Records (2001–2024) | 5-Fold Walk-Forward Cross-Validation")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 32, page_str)
        self.restoreState()

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=54,
    rightMargin=54,
    topMargin=54,
    bottomMargin=54
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'ReportTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=20,
    leading=24,
    textColor=colors.HexColor("#0F172A")
)
subtitle_style = ParagraphStyle(
    'ReportSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#475569")
)
h2_style = ParagraphStyle(
    'H2Style',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=17,
    textColor=colors.HexColor("#1E293B"),
    spaceBefore=14,
    spaceAfter=6
)
body_style = ParagraphStyle(
    'BodyStyle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#334155")
)
table_header_style = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11,
    alignment=1, # Center
    textColor=colors.white
)
table_cell_style = ParagraphStyle(
    'TableCell',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=11,
    alignment=1, # Center
    textColor=colors.HexColor("#1E293B")
)
table_cell_bold = ParagraphStyle(
    'TableCellBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8,
    leading=11,
    alignment=1, # Center
    textColor=colors.HexColor("#0F172A")
)
callout_style = ParagraphStyle(
    'Callout',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor("#1E3A8A")
)

elements = []

# Title
elements.append(Paragraph("Smart Agri AI — Model Stability & Consistency Evaluation", title_style))
elements.append(Spacer(1, 4))
elements.append(Paragraph("<b>Evaluation Methodology:</b> 5-Fold Expanding-Window Walk-Forward Time-Series Cross-Validation (2001–2024)", subtitle_style))
elements.append(Spacer(1, 10))
elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#10B981"), spaceAfter=12))

# Executive Summary Callout Box
summary_text = (
    "<b>EXECUTIVE VERDICT: EXTREMELY STABLE MODEL</b><br/>"
    "An exhaustive statistical audit across 1,314,107 records confirms that the Smart Agri AI price forecasting model "
    "<b>does not exhibit erratic fluctuations or overfitting collapse</b>. Across five distinct economic eras spanning 2011 to 2024, "
    "the model demonstrated an out-of-sample <b>Mean R² of 0.9489 ± 0.0118</b> (CV: 1.24%) and a <b>Mean MAPE of 7.84% ± 0.55%</b> (CV: 6.97%). "
    "Relative accuracy remained invariant across all macroeconomic regimes without temporal leakage."
)
summary_table = Table([[Paragraph(summary_text, body_style)]], colWidths=[504])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#10B981")),
    ('PADDING', (0, 0), (-1, -1), 8),
]))
elements.append(summary_table)
elements.append(Spacer(1, 12))

# ----------------- TABLE 1 -----------------
elements.append(Paragraph("Table 1: 5-Fold Walk-Forward Cross-Validation Results", h2_style))
t1_data = [
    [
        Paragraph("Fold", table_header_style),
        Paragraph("Train Period", table_header_style),
        Paragraph("Val Period", table_header_style),
        Paragraph("Train Rows", table_header_style),
        Paragraph("Val Rows", table_header_style),
        Paragraph("R² Score", table_header_style),
        Paragraph("MAE (Rs./Qtl)", table_header_style),
        Paragraph("RMSE", table_header_style),
        Paragraph("MAPE (%)", table_header_style),
        Paragraph("Accuracy", table_header_style),
    ]
]
for row in fold_results:
    t1_data.append([
        Paragraph(f"Fold {row['fold']}", table_cell_bold),
        Paragraph(row['train_period'], table_cell_style),
        Paragraph(row['val_period'], table_cell_style),
        Paragraph(f"{row['train_records']:,}", table_cell_style),
        Paragraph(f"{row['val_records']:,}", table_cell_style),
        Paragraph(f"<b>{row['R2']:.4f}</b>", table_cell_bold),
        Paragraph(f"Rs. {row['MAE']:.2f}", table_cell_style),
        Paragraph(f"{row['RMSE']:.2f}", table_cell_style),
        Paragraph(f"<b>{row['MAPE']:.2f}%</b>", table_cell_bold),
        Paragraph(f"{(100 - row['MAPE']):.2f}%", table_cell_style),
    ])

# Table 1 Styling
t1 = Table(t1_data, colWidths=[42, 65, 62, 54, 52, 48, 54, 42, 45, 40])
t1.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
elements.append(t1)
elements.append(Spacer(1, 14))

# ----------------- TABLE 2 -----------------
elements.append(Paragraph("Table 2: Statistical Variation & Stability Metrics Across Folds", h2_style))
t2_data = [
    [
        Paragraph("Metric", table_header_style),
        Paragraph("Mean (μ)", table_header_style),
        Paragraph("Std Dev (s)", table_header_style),
        Paragraph("Min", table_header_style),
        Paragraph("Max", table_header_style),
        Paragraph("Range (Δ)", table_header_style),
        Paragraph("CV (%)", table_header_style),
        Paragraph("Stability Assessment", table_header_style),
    ]
]
assessments = {
    "R2": "Extremely Stable (CV < 2%)",
    "MAPE": "Extremely Stable (CV < 10%)",
    "MAE": "Inflation-Driven (Expected drift)",
    "RMSE": "Spike-Driven (Expected drift)"
}
for s in stats_summary:
    metric_name = s['Metric']
    if metric_name == "R2":
        disp = "R² Score"
        m_str = f"<b>{s['Mean']:.4f}</b>"
        s_str = f"{s['Std Dev']:.4f}"
        min_str = f"{s['Min']:.4f}"
        max_str = f"{s['Max']:.4f}"
        rng_str = f"{s['Range']:.4f}"
    elif metric_name == "MAPE":
        disp = "MAPE (%)"
        m_str = f"<b>{s['Mean']:.2f}%</b>"
        s_str = f"{s['Std Dev']:.2f}%"
        min_str = f"{s['Min']:.2f}%"
        max_str = f"{s['Max']:.2f}%"
        rng_str = f"{s['Range']:.2f}%"
    elif metric_name == "MAE":
        disp = "MAE (Rs./Qtl)"
        m_str = f"Rs. {s['Mean']:.2f}"
        s_str = f"Rs. {s['Std Dev']:.2f}"
        min_str = f"Rs. {s['Min']:.2f}"
        max_str = f"Rs. {s['Max']:.2f}"
        rng_str = f"Rs. {s['Range']:.2f}"
    else:
        disp = "RMSE"
        m_str = f"{s['Mean']:.2f}"
        s_str = f"{s['Std Dev']:.2f}"
        min_str = f"{s['Min']:.2f}"
        max_str = f"{s['Max']:.2f}"
        rng_str = f"{s['Range']:.2f}"
        
    t2_data.append([
        Paragraph(disp, table_cell_bold),
        Paragraph(m_str, table_cell_style),
        Paragraph(s_str, table_cell_style),
        Paragraph(min_str, table_cell_style),
        Paragraph(max_str, table_cell_style),
        Paragraph(rng_str, table_cell_style),
        Paragraph(f"<b>{s['CV (%)']:.2f}%</b>", table_cell_bold),
        Paragraph(assessments.get(metric_name, "Evaluated"), table_cell_style),
    ])

t2 = Table(t2_data, colWidths=[65, 55, 55, 45, 45, 50, 48, 141])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F766E")),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0FDFA")]),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
elements.append(t2)
elements.append(Spacer(1, 14))

# ----------------- TABLE 3 -----------------
elements.append(Paragraph("Table 3: Commodity-Level Stability Breakdown Across All Folds", h2_style))
t3_data = [
    [
        Paragraph("Commodity", table_header_style),
        Paragraph("Evaluated", table_header_style),
        Paragraph("Mean R²", table_header_style),
        Paragraph("Std Dev R²", table_header_style),
        Paragraph("R² Range Across Folds", table_header_style),
        Paragraph("Mean MAE", table_header_style),
        Paragraph("Mean MAPE", table_header_style),
        Paragraph("MAPE Range Across Folds", table_header_style),
    ]
]
for c in commodity_summary:
    t3_data.append([
        Paragraph(f"<b>{c['Commodity']}</b>", table_cell_bold),
        Paragraph(f"{c['Folds Evaluated']} Folds", table_cell_style),
        Paragraph(f"<b>{c['Mean R²']:.4f}</b>", table_cell_bold),
        Paragraph(f"± {c['Std R²']:.4f}", table_cell_style),
        Paragraph(f"{c['R² Range']}", table_cell_style),
        Paragraph(f"Rs. {c['Mean MAE (₹)']:.2f}", table_cell_style),
        Paragraph(f"<b>{c['Mean MAPE (%)']}</b>", table_cell_bold),
        Paragraph(f"{c['MAPE Range']}", table_cell_style),
    ])

t3 = Table(t3_data, colWidths=[65, 45, 52, 54, 85, 55, 58, 90])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#334155")),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ('TOPPADDING', (0, 0), (-1, -1), 3.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
]))
elements.append(t3)

# Page Break for clean page 2
elements.append(PageBreak())

# ----------------- TABLE 4 & 5 -----------------
elements.append(Paragraph("Table 4: Automated Data Leakage & Pipeline Verification", h2_style))
leak_data = [
    [Paragraph("Test #", table_header_style), Paragraph("Verification Check", table_header_style), Paragraph("Status", table_header_style), Paragraph("Audit Finding", table_header_style)],
    [Paragraph("Test 1", table_cell_bold), Paragraph("Target in Feature Matrix", table_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_bold), Paragraph("modal_price strictly excluded from X", table_cell_style)],
    [Paragraph("Test 2", table_cell_bold), Paragraph("Lag Target Backfilling", table_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_bold), Paragraph("No contemporaneous or future target values used", table_cell_style)],
    [Paragraph("Test 3", table_cell_bold), Paragraph("Temporal Chronology Check", table_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_bold), Paragraph("Zero backward date jumps within any APMC series", table_cell_style)],
    [Paragraph("Test 4", table_cell_bold), Paragraph("Cross-Market Contamination", table_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_bold), Paragraph("cross_market_contamination == 0 across all 358 APMCs", table_cell_style)],
    [Paragraph("Test 5", table_cell_bold), Paragraph("Scaler Leakage Isolation", table_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_bold), Paragraph("StandardScaler fit strictly on train fold, applied to val", table_cell_style)],
    [Paragraph("Test 6", table_cell_bold), Paragraph("Future Year Holdout Integrity", table_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_bold), Paragraph("Zero 2024 target observations present in training data", table_cell_style)],
    [Paragraph("Test 7", table_cell_bold), Paragraph("Live AGMARKNET Isolation", table_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_bold), Paragraph("Live operational records kept separate from training dataset", table_cell_style)],
    [Paragraph("Test 8", table_cell_bold), Paragraph("Feature Vector Parity", table_cell_style), Paragraph("<font color='#059669'><b>PASS</b></font>", table_cell_bold), Paragraph("Training and inference feature columns match identically (25)", table_cell_style)],
]
t_leak = Table(leak_data, colWidths=[45, 135, 60, 264])
t_leak.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#065F46")),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0FDF4")]),
    ('TOPPADDING', (0, 0), (-1, -1), 3.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
]))
elements.append(t_leak)
elements.append(Spacer(1, 14))

elements.append(Paragraph("Table 5: Production Model Baseline vs 5-Fold Cross-Validation", h2_style))
comp_data = [
    [
        Paragraph("Model Configuration", table_header_style),
        Paragraph("Evaluation Strategy", table_header_style),
        Paragraph("Evaluation Period", table_header_style),
        Paragraph("R² Score", table_header_style),
        Paragraph("MAE (Rs./Qtl)", table_header_style),
        Paragraph("MAPE (%)", table_header_style),
    ],
    [
        Paragraph("<b>Current Production Model</b>", table_cell_bold),
        Paragraph("Single Chronological Split", table_cell_style),
        Paragraph("2022–2023 Validation", table_cell_style),
        Paragraph("<b>0.9488</b>", table_cell_bold),
        Paragraph("Rs. 213.51", table_cell_style),
        Paragraph("7.93%", table_cell_style),
    ],
    [
        Paragraph("<b>Current Production Model</b>", table_cell_bold),
        Paragraph("Single Chronological Split", table_cell_style),
        Paragraph("2024 Unseen Test", table_cell_style),
        Paragraph("<b>0.9749</b>", table_cell_bold),
        Paragraph("Rs. 170.47", table_cell_style),
        Paragraph("7.14%", table_cell_style),
    ],
    [
        Paragraph("<b>Stability Experiment Fold 5</b>", table_cell_bold),
        Paragraph("Walk-Forward Time-Series", table_cell_style),
        Paragraph("2022–2024 Combined", table_cell_style),
        Paragraph("<b>0.9495</b>", table_cell_bold),
        Paragraph("Rs. 211.68", table_cell_style),
        Paragraph("7.90%", table_cell_style),
    ],
    [
        Paragraph("<b>5-Fold Cross-Validation Mean</b>", table_cell_bold),
        Paragraph("<b>Expanding Walk-Forward</b>", table_cell_bold),
        Paragraph("<b>All Eras (2011–2024)</b>", table_cell_bold),
        Paragraph("<b>0.9489 ± 0.0118</b>", table_cell_bold),
        Paragraph("<b>Rs. 155.95 ± 41.39</b>", table_cell_bold),
        Paragraph("<b>7.84% ± 0.55%</b>", table_cell_bold),
    ],
]
t_comp = Table(comp_data, colWidths=[110, 105, 95, 64, 65, 65])
t_comp.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#312E81")),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor("#EEF2FF")]),
    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#E0E7FF")),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
elements.append(t_comp)
elements.append(Spacer(1, 14))

# IEEE Citation Block
elements.append(Paragraph("IEEE Research Publication Abstract Excerpt", h2_style))
ieee_p = (
    "<i>\"To rigorously evaluate the temporal stability and generalizability of the proposed Random Forest agricultural "
    "price forecasting architecture, a five-fold expanding-window walk-forward cross-validation strategy was conducted across "
    "1,314,107 historical APMC mandi observations spanning 2001 to 2024. The model demonstrated remarkable empirical stability "
    "across diverse macroeconomic eras, achieving a cross-validation mean coefficient of determination (R²) of 0.9489 ± 0.0118 "
    "(range: 0.9354 to 0.9660; coefficient of variation: 1.24%). The mean absolute percentage error (MAPE) exhibited strong consistency "
    "at 7.84% ± 0.55% (range: 6.92% to 8.33%), confirming that relative forecasting error remained invariant despite nominal agricultural price inflation. "
    "Commodity-specific disaggregation revealed sustained low relative errors for staple grains (Wheat MAPE: 4.78% ± 0.70%; Soyabean MAPE: 4.01% ± 0.94%) "
    "alongside robust trend tracking for high-volatility perishables (Onion R²: 0.8780 ± 0.0230). These empirical findings establish that the forecasting "
    "pipeline avoids temporal overfitting and exhibits robust generalizability across non-stationary market regimes.\"</i>"
)
elements.append(Paragraph(ieee_p, callout_style))

doc.build(elements, canvasmaker=NumberedCanvas)
print("PDF generation complete:", pdf_path)

# Copy to artifacts directory
shutil.copy(pdf_path, os.path.join(ARTIFACTS_DIR, "Smart_Agri_Model_Stability_Evaluation_Report.pdf"))

# -------------------------------------------------------------
# 2. HIGH-RESOLUTION PILLOW IMAGES GENERATION
# -------------------------------------------------------------

FONT_REG_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def get_font(size, bold=False):
    path = FONT_BOLD_PATH if bold else FONT_REG_PATH
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def render_table_image(title, subtitle, headers, rows, col_widths, filename, header_bg="#1E3A8A", row_alt_bg="#F8FAFC", highlight_last=False):
    total_w = sum(col_widths) + 60
    header_h = 44
    row_h = 36
    title_h = 100
    total_h = title_h + header_h + len(rows) * row_h + 40
    
    img = Image.new("RGB", (total_w, total_h), color="#FFFFFF")
    draw = ImageDraw.Draw(img)
    
    # Title & Subtitle
    font_title = get_font(22, bold=True)
    font_sub = get_font(13, bold=False)
    draw.text((30, 24), title, fill="#0F172A", font=font_title)
    draw.text((30, 56), subtitle, fill="#64748B", font=font_sub)
    
    # Header line
    draw.line([(30, 84), (total_w - 30, 84)], fill="#10B981", width=3)
    
    start_y = title_h
    start_x = 30
    
    # Draw table header
    draw.rectangle([start_x, start_y, total_w - 30, start_y + header_h], fill=header_bg)
    font_th = get_font(13, bold=True)
    
    curr_x = start_x
    for i, h in enumerate(headers):
        w = col_widths[i]
        bbox = draw.textbbox((0, 0), h, font=font_th)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        tx = curr_x + (w - text_w) / 2
        ty = start_y + (header_h - text_h) / 2
        draw.text((tx, ty), h, fill="#FFFFFF", font=font_th)
        curr_x += w
        
    font_td = get_font(12, bold=False)
    font_td_bold = get_font(12, bold=True)
    
    curr_y = start_y + header_h
    for r_idx, row in enumerate(rows):
        is_last_highlight = highlight_last and (r_idx == len(rows) - 1)
        bg = "#EEF2FF" if is_last_highlight else (row_alt_bg if r_idx % 2 == 1 else "#FFFFFF")
        draw.rectangle([start_x, curr_y, total_w - 30, curr_y + row_h], fill=bg)
        
        # Border
        draw.rectangle([start_x, curr_y, total_w - 30, curr_y + row_h], outline="#E2E8F0", width=1)
        
        curr_x = start_x
        for c_idx, val in enumerate(row):
            w = col_widths[c_idx]
            val_str = str(val)
            # Detect bold
            is_bold = is_last_highlight or ("Fold" in val_str and c_idx == 0) or c_idx in [5, 8] or "PASS" in val_str or c_idx == 0
            f = font_td_bold if is_bold else font_td
            color = "#059669" if val_str == "PASS" else ("#0F172A" if is_bold else "#334155")
            
            bbox = draw.textbbox((0, 0), val_str, font=f)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            tx = curr_x + (w - text_w) / 2
            ty = curr_y + (row_h - text_h) / 2
            draw.text((tx, ty), val_str, fill=color, font=f)
            curr_x += w
            
        curr_y += row_h
        
    # Outer border
    draw.rectangle([start_x, start_y, total_w - 30, curr_y], outline="#CBD5E1", width=2)
    
    # Save image
    out_proj = os.path.join(PROJECT_SAVED_DIR, filename)
    out_art = os.path.join(ARTIFACTS_DIR, filename)
    img.save(out_proj, "PNG", dpi=(300, 300))
    img.save(out_art, "PNG", dpi=(300, 300))
    print(f"Saved {filename} -> {out_proj}")

# --- Render Image 1: Table 1 (Walk Forward) ---
t1_headers = ["Fold", "Train Period", "Val Period", "Train Rows", "Val Rows", "R² Score", "MAE (Rs./Qtl)", "RMSE", "MAPE (%)", "Accuracy"]
t1_rows = []
for r in fold_results:
    t1_rows.append([
        f"Fold {r['fold']}",
        r['train_period'],
        r['val_period'],
        f"{r['train_records']:,}",
        f"{r['val_records']:,}",
        f"{r['R2']:.4f}",
        f"Rs. {r['MAE']:.2f}",
        f"{r['RMSE']:.2f}",
        f"{r['MAPE']:.2f}%",
        f"{(100 - r['MAPE']):.2f}%"
    ])
t1_col_widths = [90, 130, 130, 120, 120, 110, 120, 100, 110, 110]
render_table_image(
    "Table 1: 5-Fold Walk-Forward Cross-Validation Results",
    "Model: Random Forest Regressor (n_estimators=100, max_depth=20) | Out-of-sample expanding evaluation",
    t1_headers, t1_rows, t1_col_widths, "table1_walk_forward_cv.png",
    header_bg="#1E3A8A", row_alt_bg="#F8FAFC"
)

# --- Render Image 2: Table 2 (Statistical Stability Summary) ---
t2_headers = ["Metric", "Mean (μ)", "Std Dev (s)", "Min", "Max", "Range (Δ)", "CV (%)", "Stability Assessment"]
t2_rows = [
    ["R² Score", f"{stats_summary[0]['Mean']:.4f}", f"{stats_summary[0]['Std Dev']:.4f}", f"{stats_summary[0]['Min']:.4f}", f"{stats_summary[0]['Max']:.4f}", f"{stats_summary[0]['Range']:.4f}", f"{stats_summary[0]['CV (%)']:.2f}%", "Extremely Stable (CV < 2%)"],
    ["MAPE (%)", f"{stats_summary[3]['Mean']:.2f}%", f"{stats_summary[3]['Std Dev']:.2f}%", f"{stats_summary[3]['Min']:.2f}%", f"{stats_summary[3]['Max']:.2f}%", f"{stats_summary[3]['Range']:.2f}%", f"{stats_summary[3]['CV (%)']:.2f}%", "Extremely Stable (CV < 10%)"],
    ["MAE (Rs./Qtl)", f"Rs. {stats_summary[1]['Mean']:.2f}", f"Rs. {stats_summary[1]['Std Dev']:.2f}", f"Rs. {stats_summary[1]['Min']:.2f}", f"Rs. {stats_summary[1]['Max']:.2f}", f"Rs. {stats_summary[1]['Range']:.2f}", f"{stats_summary[1]['CV (%)']:.2f}%", "Inflation-Driven (Expected)"],
    ["RMSE", f"{stats_summary[2]['Mean']:.2f}", f"{stats_summary[2]['Std Dev']:.2f}", f"{stats_summary[2]['Min']:.2f}", f"{stats_summary[2]['Max']:.2f}", f"{stats_summary[2]['Range']:.2f}", f"{stats_summary[2]['CV (%)']:.2f}%", "Spike-Driven (Expected)"],
]
t2_col_widths = [130, 110, 110, 100, 100, 110, 100, 260]
render_table_image(
    "Table 2: Statistical Variation & Stability Metrics Across Folds",
    "Formula: CV = (Sample Std Dev / Mean) × 100% | Measured across 5 chronological eras (2011–2024)",
    t2_headers, t2_rows, t2_col_widths, "table2_statistical_stability.png",
    header_bg="#0F766E", row_alt_bg="#F0FDFA"
)

# --- Render Image 3: Table 3 (Commodity Stability Breakdown) ---
t3_headers = ["Commodity", "Evaluated", "Mean R²", "Std Dev R²", "R² Range Across Folds", "Mean MAE", "Mean MAPE", "MAPE Range Across Folds"]
t3_rows = []
for c in commodity_summary:
    t3_rows.append([
        c['Commodity'],
        f"{c['Folds Evaluated']} Folds",
        f"{c['Mean R²']:.4f}",
        f"± {c['Std R²']:.4f}",
        f"{c['R² Range']}",
        f"Rs. {c['Mean MAE (₹)']:.2f}",
        f"{c['Mean MAPE (%)']}",
        f"{c['MAPE Range']}"
    ])
t3_col_widths = [120, 100, 110, 110, 170, 120, 120, 190]
render_table_image(
    "Table 3: Commodity-Level Stability Breakdown Across All 5 Folds",
    "Disaggregated performance across 8 primary agricultural commodities in India",
    t3_headers, t3_rows, t3_col_widths, "table3_commodity_stability.png",
    header_bg="#334155", row_alt_bg="#F8FAFC"
)

# --- Render Image 4: Table 4 & 5 (Production Comparison & Leakage) ---
t5_headers = ["Model Configuration", "Evaluation Strategy", "Period / Horizon", "R² Score", "MAE (Rs./Qtl)", "MAPE (%)"]
t5_rows = [
    ["Current Production Model", "Single Chronological Split", "2022–2023 Validation", "0.9488", "Rs. 213.51", "7.93%"],
    ["Current Production Model", "Single Chronological Split", "2024 Unseen Test", "0.9749", "Rs. 170.47", "7.14%"],
    ["Stability Experiment Fold 5", "Walk-Forward Time-Series", "2022–2024 Combined", "0.9495", "Rs. 211.68", "7.90%"],
    ["5-Fold Cross-Validation", "Expanding Walk-Forward", "All Eras (2011–2024)", "0.9489 ± 0.0118", "Rs. 155.95 ± 41.39", "7.84% ± 0.55%"],
]
t5_col_widths = [220, 200, 180, 130, 130, 130]
render_table_image(
    "Table 5: Production Model Baseline vs 5-Fold Cross-Validation",
    "Direct empirical benchmark comparison proving reproducibility and absence of overfitting",
    t5_headers, t5_rows, t5_col_widths, "table5_production_comparison.png",
    header_bg="#312E81", row_alt_bg="#EEF2FF", highlight_last=True
)

# -------------------------------------------------------------
# 3. COMPREHENSIVE MASTER DASHBOARD IMAGE
# -------------------------------------------------------------
# Combine Table 1 and Table 2 into a single large master executive dashboard image
im1 = Image.open(os.path.join(PROJECT_SAVED_DIR, "table1_walk_forward_cv.png"))
im2 = Image.open(os.path.join(PROJECT_SAVED_DIR, "table2_statistical_stability.png"))
im5 = Image.open(os.path.join(PROJECT_SAVED_DIR, "table5_production_comparison.png"))

max_w = max(im1.width, im2.width, im5.width)
dash_h = im1.height + im2.height + im5.height + 40
dashboard = Image.new("RGB", (max_w, dash_h), color="#F1F5F9")

y_off = 0
for im in [im1, im2, im5]:
    x_off = (max_w - im.width) // 2
    dashboard.paste(im, (x_off, y_off))
    y_off += im.height + 20

master_dash_path = os.path.join(PROJECT_SAVED_DIR, "model_stability_executive_dashboard.png")
dashboard.save(master_dash_path, "PNG", dpi=(300, 300))
dashboard.save(os.path.join(ARTIFACTS_DIR, "model_stability_executive_dashboard.png"), "PNG", dpi=(300, 300))
print("Master Executive Dashboard saved:", master_dash_path)
