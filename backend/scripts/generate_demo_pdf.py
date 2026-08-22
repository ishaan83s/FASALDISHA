"""
Generate professional PDF guide for FasalDisha Demo Flow and Judge Playbook.
Uses ReportLab to construct a multi-page styled PDF.
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

pdf_filename = r"c:\Users\jayg\FASALDISHA\FASALDISHA_DEMO_FLOW_AND_JUDGE_PLAYBOOK.pdf"

doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    rightMargin=36,
    leftMargin=36,
    topMargin=36,
    bottomMargin=36,
)

styles = getSampleStyleSheet()

# Custom Palette
PRIMARY = colors.HexColor("#065f46")     # Emerald 800
SECONDARY = colors.HexColor("#047857")   # Emerald 700
ACCENT = colors.HexColor("#d97706")      # Amber 600
DARK_TEXT = colors.HexColor("#111827")   # Gray 900
MUTED_TEXT = colors.HexColor("#4b5563")  # Gray 600
LIGHT_BG = colors.HexColor("#f0fdf4")    # Emerald 50
BORDER_COLOR = colors.HexColor("#cbd5e1")# Slate 300
HIGHLIGHT_BG = colors.HexColor("#fef3c7")# Amber 100

# Custom Typography Styles
title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Heading1"],
    fontSize=22,
    leading=26,
    textColor=PRIMARY,
    fontName="Helvetica-Bold",
    spaceAfter=4,
)

subtitle_style = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    textColor=MUTED_TEXT,
    fontName="Helvetica",
    spaceAfter=12,
)

h1_style = ParagraphStyle(
    "H1",
    parent=styles["Heading2"],
    fontSize=14,
    leading=18,
    textColor=PRIMARY,
    fontName="Helvetica-Bold",
    spaceBefore=12,
    spaceAfter=6,
)

h2_style = ParagraphStyle(
    "H2",
    parent=styles["Heading3"],
    fontSize=11,
    leading=15,
    textColor=SECONDARY,
    fontName="Helvetica-Bold",
    spaceBefore=8,
    spaceAfter=4,
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=9,
    leading=13,
    textColor=DARK_TEXT,
    fontName="Helvetica",
    spaceAfter=6,
)

bullet_style = ParagraphStyle(
    "Bullet",
    parent=body_style,
    leftIndent=12,
    firstLineIndent=-8,
    spaceAfter=3,
)

code_style = ParagraphStyle(
    "CodeBlock",
    parent=styles["Normal"],
    fontSize=8,
    leading=11,
    fontName="Courier",
    textColor=colors.HexColor("#0f172a"),
    backColor=colors.HexColor("#f8fafc"),
    borderPadding=6,
    spaceAfter=6,
)

table_header_style = ParagraphStyle(
    "TableHeader",
    parent=styles["Normal"],
    fontSize=8.5,
    leading=11,
    textColor=colors.white,
    fontName="Helvetica-Bold",
    alignment=0,
)

table_cell_style = ParagraphStyle(
    "TableCell",
    parent=styles["Normal"],
    fontSize=8,
    leading=11,
    textColor=DARK_TEXT,
    fontName="Helvetica",
)

story = []

# Title Section
story.append(Paragraph("FasalDisha — फसल दिशा", title_style))
story.append(Paragraph("<b>AI Crop Price Forecasting & Market Routing System (Round 2 v2.0)</b><br/>Official Judge Demonstration Flow & Evaluation Playbook", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=10))

# 1. Executive Pitch
story.append(Paragraph("1. Executive Value Proposition & Opening Pitch", h1_style))
story.append(Paragraph("<b>The Core Question:</b> <i>'Given my commodity, quantity, coordinates, price forecast, transport cost, and active risks — where should I sell, and should I sell now or wait?'</i>", body_style))
story.append(Paragraph("FasalDisha is not a passive price board. It is an end-to-end <b>forecasting + market-routing + risk-aware decision engine</b> that empowers farmers with transparent, quantity-aware, and risk-adjusted market options.", body_style))

story.append(Spacer(1, 4))

# 2. Setup & Execution Commands
story.append(Paragraph("2. Quick Server Startup (Run in 2 Terminals)", h1_style))
setup_table_data = [
    [
        Paragraph("<b>Component</b>", table_header_style),
        Paragraph("<b>Port / URL</b>", table_header_style),
        Paragraph("<b>Startup Command (PowerShell)</b>", table_header_style),
    ],
    [
        Paragraph("<b>Backend (FastAPI)</b>", table_cell_style),
        Paragraph("http://127.0.0.1:8000", table_cell_style),
        Paragraph("<code>$env:PYTHONPATH='backend;.' ; uvicorn app.main:app --port 8000</code>", code_style),
    ],
    [
        Paragraph("<b>Frontend (React+Vite)</b>", table_cell_style),
        Paragraph("http://localhost:5173", table_cell_style),
        Paragraph("<code>cd frontend ; npm run dev</code>", code_style),
    ],
]
t_setup = Table(setup_table_data, colWidths=[1.4*inch, 1.8*inch, 3.8*inch])
t_setup.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t_setup)

story.append(Spacer(1, 8))

# 3. Step-by-Step 3-Minute Demo Script
story.append(Paragraph("3. Step-by-Step 3-Minute Judge Demonstration Flow", h1_style))

# Scenario A
story.append(Paragraph("Step A: Hero Scenario — Pune Onion (Deterministic Seeded Weather Risk Override)", h2_style))
story.append(Paragraph("• <b>Action:</b> On the form, click preset button <b>'Scenario A: Pune Onion (Risk Override)'</b> and click <b>'Run Analysis'</b>.", bullet_style))
story.append(Paragraph("• <b>Context:</b> Maharashtra / Pune, Coordinates (18.52° N, 73.85° E), Onion (25 Quintals), Radius 120 km.", bullet_style))
story.append(Paragraph("• <b>Key Highlight 1 (Recommendation Banner):</b> Show that the base forecast decision was <b>HOLD</b> (prices rising), but the final recommendation is <b>SELL EARLY DUE TO RISK</b> due to active severe waterlogging.", bullet_style))
story.append(Paragraph("• <b>Key Highlight 2 (Honest Weather Banner):</b> Show the red alert banner labeled <b>'Source: SEEDED'</b> (clearly disclosing demo scenario).", bullet_style))
story.append(Paragraph("• <b>Key Highlight 3 (ML Forecast & Peak Alert):</b> Show 7-day horizons (Day 1: ₹2,390, Day 3: ₹2,480, Peak Day 6: ₹2,650) with active <b>PEAK ALERT (+12.8%)</b> and historical series provenance (45 days).", bullet_style))
story.append(Paragraph("• <b>Key Highlight 4 (Dynamic Mandi Rankings):</b> Show 7 mandis discovered dynamically with #1 APMC Chakan (Risk-Adjusted Return: ₹60,428 after ₹1,643 transport).", bullet_style))
story.append(Paragraph("• <b>Key Highlight 5 (Synthetic Buyer Intelligence):</b> Expand card to show 4 active buyers (Demand: MEDIUM, Offer: 77%, Reliability: 82.5%) labeled <b>'SYNTHETIC DEMO DATASET'</b>.", bullet_style))
story.append(Paragraph("• <b>Key Highlight 6 (Explainability Breakdown):</b> Show 70% Risk-Adj Return + 20% Buyer Signal + 10% Data Quality formula.", bullet_style))

story.append(Spacer(1, 4))

# Scenario B & C
story.append(Paragraph("Step B & C: Group-Wise Perishability Comparison (Tomato vs Wheat)", h2_style))
story.append(Paragraph("• <b>Action:</b> Click 'Modify Parameters', then select <b>Scenario B: Tomato</b> (Highly Perishable) and run.", bullet_style))
story.append(Paragraph("• <b>Highlight:</b> Tomato has high spoilage risk, enforcing an immediate <b>SELL_NOW</b> recommendation.", bullet_style))
story.append(Paragraph("• <b>Action:</b> Return and select <b>Scenario C: Wheat</b> (Non-Perishable / Durable Cereal).", bullet_style))
story.append(Paragraph("• <b>Highlight:</b> Durable grains under low operational risk permit holding to capture expected peak prices.", bullet_style))

story.append(Spacer(1, 4))

# Scenario D
story.append(Paragraph("Step D: Cross-Boundary Market Routing (Ahmedabad Cotton)", h2_style))
story.append(Paragraph("• <b>Action:</b> Select <b>Scenario D: Ahmedabad Cotton</b> (150 km search radius).", bullet_style))
story.append(Paragraph("• <b>Highlight:</b> Point to <b>'Cross-Boundary Enabled'</b> badge. Show how coordinate-based radius discovery finds mandis across district/state lines, eliminating artificial administrative barriers.", bullet_style))

story.append(Spacer(1, 8))

# 4. Judge Q&A Cheat Sheet
story.append(Paragraph("4. Instant Judge Q&A Cheat-Sheet (SSOT Ground Truth)", h1_style))

qa_table_data = [
    [
        Paragraph("<b>Judge Question</b>", table_header_style),
        Paragraph("<b>Winning Answer & SSOT Architecture Reference</b>", table_header_style),
    ],
    [
        Paragraph("<b>Why is this mandi ranked #1?</b>", table_cell_style),
        Paragraph("Calculated transparently via <b>ranking_service.py</b>: <b>70% Risk-Adjusted Net Return</b> (expected revenue minus distance transit cost and risk penalty) + <b>20% Synthetic Buyer Signal</b> + <b>10% Data Quality</b>.", table_cell_style),
    ],
    [
        Paragraph("<b>Are the buyers real? Where do they come from?</b>", table_cell_style),
        Paragraph("<b>No, they are explicitly labeled SYNTHETIC.</b> We aggregate active buyer records (demand level, offer strength, reliability) from our catalog to model market liquidity without falsely claiming a live marketplace.", table_cell_style),
    ],
    [
        Paragraph("<b>How does weather change the decision?</b>", table_cell_style),
        Paragraph("Weather feeds a separate risk layer (<b>risk_service.py</b>). When severe meteorological or transit risk is active, the engine overrides a HOLD decision to <b>SELL_EARLY_DUE_TO_RISK</b> to prevent spoilage.", table_cell_style),
    ],
    [
        Paragraph("<b>Why not limit search to the farmer's district?</b>", table_cell_style),
        Paragraph("District is just an entry context. A farmer near a border might have a much higher-paying mandi 20 km away in a neighboring district. Routing is strictly <b>coordinate and radius-driven</b>.", table_cell_style),
    ],
    [
        Paragraph("<b>Is the forecast model live or precomputed?</b>", table_cell_style),
        Paragraph("Our system supports pooled ML models (<b>forecast_engine.py</b>) with contract-compliant precomputed fallbacks. We honestly disclose <code>modelType: PRECOMPUTED</code> and <code>historyClassification: SEEDED</code> on screen.", table_cell_style),
    ],
]

t_qa = Table(qa_table_data, colWidths=[2.2*inch, 4.8*inch])
t_qa.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(t_qa)

story.append(Spacer(1, 10))

# 5. Judge-Proof Acceptance Matrix
story.append(Paragraph("5. Judge-Proof Acceptance & Verification Matrix", h1_style))

matrix_data = [
    [Paragraph("<b>Proof Requirement</b>", table_header_style), Paragraph("<b>UI Element / Proof Anchor</b>", table_header_style), Paragraph("<b>Status</b>", table_header_style)],
    [Paragraph("Weather Impact", table_cell_style), Paragraph("WeatherAlert banner + Seeded Source label + Risk Override", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
    [Paragraph("Group Perishability", table_cell_style), Paragraph("3-level perishability badge + storage urgency logic", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
    [Paragraph("Buyer Intelligence", table_cell_style), Paragraph("Active buyer count + SYNTHETIC label + demand metrics", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
    [Paragraph("Best Location Selection", table_cell_style), Paragraph("Dynamic ranked list + 70/20/10 formula explainability", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
    [Paragraph("ML Forecast & Peak Alert", table_cell_style), Paragraph("7-day horizons + PEAK ALERT banner + 45d history basis", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
    [Paragraph("Decision Audit Trail", table_cell_style), Paragraph("Judge-Proof Audit Panel with 4 transparent proof cards", table_cell_style), Paragraph("<b>PASS</b>", table_cell_style)],
]

t_matrix = Table(matrix_data, colWidths=[2.0*inch, 4.0*inch, 1.0*inch])
t_matrix.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), SECONDARY),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, BORDER_COLOR),
    ("TOPPADDING", (0, 0), (-1, -1), 3),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(t_matrix)

doc.build(story)
print(f"PDF successfully generated: {pdf_filename}")
