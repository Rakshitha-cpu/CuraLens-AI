import os
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ---------------------------------------------------
# Output folder for generated reports
# ---------------------------------------------------

REPORTS_DIR = Path(__file__).resolve().parents[2] / "generated_reports"
REPORTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------
# Brand colors
# ---------------------------------------------------

CYAN = HexColor("#06B6D4")
DARK = HexColor("#0F172A")
GRAY = HexColor("#475569")
GREEN = HexColor("#16A34A")
ORANGE = HexColor("#D97706")
RED = HexColor("#DC2626")

CONFIDENCE_COLOR = {
    "high": GREEN,
    "medium": ORANGE,
    "low": RED,
}

# ---------------------------------------------------
# Styles
# ---------------------------------------------------

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    textColor=CYAN,
    fontSize=22,
    alignment=TA_CENTER,
    spaceAfter=2,
)

subtitle_style = ParagraphStyle(
    "SubtitleStyle",
    parent=styles["Normal"],
    textColor=GRAY,
    fontSize=10,
    alignment=TA_CENTER,
    spaceAfter=14,
)

section_style = ParagraphStyle(
    "SectionStyle",
    parent=styles["Heading2"],
    textColor=DARK,
    fontSize=13,
    spaceBefore=14,
    spaceAfter=6,
)

label_style = ParagraphStyle(
    "LabelStyle",
    parent=styles["Normal"],
    textColor=GRAY,
    fontSize=9,
)

value_style = ParagraphStyle(
    "ValueStyle",
    parent=styles["Normal"],
    textColor=DARK,
    fontSize=11,
)

med_name_style = ParagraphStyle(
    "MedNameStyle",
    parent=styles["Heading3"],
    textColor=DARK,
    fontSize=13,
    spaceAfter=2,
)

body_style = ParagraphStyle(
    "BodyStyle",
    parent=styles["Normal"],
    textColor=GRAY,
    fontSize=9.5,
    leading=13,
)

footer_style = ParagraphStyle(
    "FooterStyle",
    parent=styles["Normal"],
    textColor=GRAY,
    fontSize=8,
    alignment=TA_CENTER,
)

# ---------------------------------------------------
# Helper: safe get (handles missing keys gracefully)
# ---------------------------------------------------

def g(data: dict, *keys, default="UNKNOWN"):
    for key in keys:
        if not isinstance(data, dict):
            return default
        data = data.get(key, default)
    return data if data not in (None, "") else default


# ---------------------------------------------------
# Main function: builds the PDF
# ---------------------------------------------------

def generate_prescription_report(prescription: dict) -> str:
    """
    Takes the AI analysis dict (same shape returned by your agents)
    and generates a PDF report. Returns the file path.
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"CuraLens_Report_{timestamp}.pdf"
    filepath = str(REPORTS_DIR / filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=15 * mm,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
    )

    elements = []

    # ---------------- Header ----------------
    elements.append(Paragraph("CuraLens AI", title_style))
    elements.append(Paragraph("AI Prescription Analysis Report", subtitle_style))
    elements.append(HRFlowable(width="100%", color=CYAN, thickness=1.2))
    elements.append(Spacer(1, 12))

    # ---------------- Patient Info ----------------
    patient_name = g(prescription, "patient_name")
    doctor_name = g(prescription, "doctor_name")
    hospital = g(prescription, "hospital")

    info_table = Table(
        [
            [Paragraph("Patient", label_style), Paragraph(patient_name, value_style)],
            [Paragraph("Doctor", label_style), Paragraph(doctor_name, value_style)],
            [Paragraph("Hospital", label_style), Paragraph(hospital, value_style)],
            [Paragraph("Generated On", label_style),
             Paragraph(datetime.now().strftime("%d %b %Y, %I:%M %p"), value_style)],
        ],
        colWidths=[35 * mm, 130 * mm],
    )
    info_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(info_table)

    # ---------------- Medicines ----------------
    elements.append(Paragraph("Medicines", section_style))
    elements.append(HRFlowable(width="100%", color=GRAY, thickness=0.5))

    medicines = prescription.get("medicines", []) or []

    if not medicines:
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("No medicines were detected in this prescription.", body_style))

    for idx, med in enumerate(medicines, start=1):
        elements.append(Spacer(1, 10))

        name = g(med, "name")
        confidence = str(g(med, "confidence", default="medium")).lower()
        conf_color = CONFIDENCE_COLOR.get(confidence, GRAY)

        # Medicine name + confidence tag
        name_row = Table(
            [[
                Paragraph(f"{idx}. {name}", med_name_style),
                Paragraph(
                    f'<font color="{conf_color.hexval()}">'
                    f'● {confidence.upper()} CONFIDENCE</font>',
                    ParagraphStyle("conf", parent=body_style, alignment=TA_LEFT, fontSize=8.5),
                ),
            ]],
            colWidths=[110 * mm, 55 * mm],
        )
        name_row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(name_row)

        dosage = g(med, "dosage")
        frequency = g(med, "frequency")
        duration = g(med, "duration")
        instructions = g(med, "instructions")

        detail_table = Table(
            [
                [Paragraph("Dosage", label_style), Paragraph(dosage, value_style),
                 Paragraph("Frequency", label_style), Paragraph(frequency, value_style)],
                [Paragraph("Duration", label_style), Paragraph(duration, value_style),
                 Paragraph("Instructions", label_style), Paragraph(instructions, value_style)],
            ],
            colWidths=[22 * mm, 55 * mm, 22 * mm, 55 * mm],
        )
        detail_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        elements.append(detail_table)

        # Education fields (if present)
        edu = med.get("education", {}) if isinstance(med, dict) else {}
        if edu:
            purpose = g(edu, "purpose", default="")
            how_to_take = g(edu, "how_to_take", default="")
            food = g(edu, "food_instruction", default="")
            side_effects = edu.get("common_side_effects", []) or []
            warnings = edu.get("warnings", []) or []

            if purpose and purpose != "UNKNOWN":
                elements.append(Paragraph(f"<b>Purpose:</b> {purpose}", body_style))
            if how_to_take and how_to_take != "UNKNOWN":
                elements.append(Paragraph(f"<b>How to take:</b> {how_to_take}", body_style))
            if food and food != "UNKNOWN":
                elements.append(Paragraph(f"<b>Food instruction:</b> {food}", body_style))
            if side_effects:
                elements.append(Paragraph(
                    f"<b>Side effects:</b> {', '.join(side_effects)}", body_style
                ))
            if warnings:
                elements.append(Paragraph(
                    f'<b><font color="{RED.hexval()}">Warnings:</font></b> {", ".join(warnings)}',
                    body_style,
                ))

        elements.append(Spacer(1, 4))
        elements.append(HRFlowable(width="100%", color=HexColor("#E2E8F0"), thickness=0.5))

    # ---------------- Safety & Score ----------------
    safety = prescription.get("safety", {})
    score = prescription.get("score", {})

    if safety or score:
        elements.append(Paragraph("Safety Analysis", section_style))
        elements.append(HRFlowable(width="100%", color=GRAY, thickness=0.5))
        elements.append(Spacer(1, 6))

        overall_score = g(score, "score", default="N/A")
        risk_level = g(score, "risk_level", default="")
        elements.append(Paragraph(f"<b>AI Prescription Score:</b> {overall_score}/100 ({risk_level})", value_style))

        overall_risk = g(safety, "overall_risk", default="")
        if overall_risk:
            elements.append(Paragraph(f"<b>Overall Risk:</b> {overall_risk}", body_style))

        alerts = safety.get("alerts", []) if isinstance(safety, dict) else []
        for alert in alerts:
            if not isinstance(alert, dict):
                continue
            atype = alert.get("type", "Alert")
            amed = alert.get("medicine", "")
            amsg = alert.get("message", "")
            asev = alert.get("severity", "")
            elements.append(Paragraph(
                f"<b>{atype}</b> ({asev}) - {amed}: {amsg}", body_style
            ))

    # ---------------- Footer ----------------
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", color=CYAN, thickness=1))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "Generated by CuraLens AI — This report is AI-generated and should be verified by a licensed pharmacist or doctor before use.",
        footer_style,
    ))

    doc.build(elements)

    return filepath