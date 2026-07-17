import jsPDF from "jspdf";

// ---------------------------------------------------------
// Color palette - matches the app's theme, print-friendly
// ---------------------------------------------------------
const COLORS = {
  primary: [8, 145, 178],       // cyan-600 - headers, accents
  primaryDark: [21, 40, 64],    // dark navy - header band background
  textDark: [30, 41, 59],       // slate-800 - body text
  textMuted: [100, 116, 139],   // slate-500 - labels
  border: [226, 232, 240],      // slate-200 - card borders
  bgLight: [248, 250, 252],     // slate-50 - card backgrounds
  success: [22, 163, 74],       // green - low risk / verified
  warning: [217, 119, 6],       // amber - moderate risk
  danger: [220, 38, 38],        // red - high risk
  white: [255, 255, 255],
};

function riskColor(level) {
  const l = String(level || "").toUpperCase();
  if (l.includes("HIGH")) return COLORS.danger;
  if (l.includes("MODERATE") || l.includes("MEDIUM")) return COLORS.warning;
  return COLORS.success;
}

function severityColor(sev) {
  const s = String(sev || "").toUpperCase();
  if (s === "HIGH") return COLORS.danger;
  if (s === "MODERATE" || s === "MEDIUM") return COLORS.warning;
  return COLORS.textMuted;
}

export function generatePDF(result) {
  const doc = new jsPDF();
  const pageWidth = doc.internal.pageSize.width;
  const pageHeight = doc.internal.pageSize.height;
  const marginX = 18;
  const contentWidth = pageWidth - marginX * 2;

  let y = 0;

  // -------------------------------------------------------
  // Helpers
  // -------------------------------------------------------
  function ensureSpace(neededHeight) {
    if (y + neededHeight > pageHeight - 20) {
      doc.addPage();
      y = 20;
    }
  }

  function sectionHeader(title) {
    ensureSpace(16);
    doc.setFillColor(...COLORS.primary);
    doc.rect(marginX, y, 3, 8, "F");
    doc.setFont(undefined, "bold");
    doc.setFontSize(13);
    doc.setTextColor(...COLORS.textDark);
    doc.text(title, marginX + 6, y + 6.5);
    y += 13;
  }

  function labelValue(label, value, x, width) {
    doc.setFont(undefined, "normal");
    doc.setFontSize(9);
    doc.setTextColor(...COLORS.textMuted);
    doc.text(label.toUpperCase(), x, y);
    doc.setFont(undefined, "normal");
    doc.setFontSize(10.5);
    doc.setTextColor(...COLORS.textDark);
    const lines = doc.splitTextToSize(String(value || "Not Available"), width);
    doc.text(lines, x, y + 5);
    return lines.length * 5;
  }

  function wrappedText(text, x, width, fontSize = 10, color = COLORS.textDark) {
    doc.setFont(undefined, "normal");
    doc.setFontSize(fontSize);
    doc.setTextColor(...color);
    const lines = doc.splitTextToSize(String(text || ""), width);
    ensureSpace(lines.length * 5 + 2);
    doc.text(lines, x, y);
    y += lines.length * 5;
    return lines.length * 5;
  }

  function badge(text, x, yPos, color) {
    doc.setFontSize(8);
    doc.setFont(undefined, "bold");
    const textWidth = doc.getTextWidth(text) + 6;
    doc.setFillColor(...color);
    doc.roundedRect(x, yPos - 4.5, textWidth, 6, 1.5, 1.5, "F");
    doc.setTextColor(...COLORS.white);
    doc.text(text, x + 3, yPos);
    return textWidth;
  }

  // -------------------------------------------------------
  // Header band
  // -------------------------------------------------------
  doc.setFillColor(...COLORS.primaryDark);
  doc.rect(0, 0, pageWidth, 32, "F");

  doc.setTextColor(...COLORS.white);
  doc.setFont(undefined, "bold");
  doc.setFontSize(19);
  doc.text("CuraLens AI", marginX, 15);

  doc.setFont(undefined, "normal");
  doc.setFontSize(10);
  doc.setTextColor(180, 220, 230);
  doc.text("AI-Powered Prescription Intelligence Report", marginX, 22);

  const generatedDate = new Date().toLocaleString();
  doc.setFontSize(8.5);
  doc.text(`Generated: ${generatedDate}`, pageWidth - marginX, 22, { align: "right" });

  y = 42;

  // -------------------------------------------------------
  // Summary dashboard row (Medicines / Verified / Risk / Score)
  // -------------------------------------------------------
  const medicines = result.medicines || [];
  const verifiedCount = medicines.filter((m) => m.database_verified).length;
  const overallRisk = result.safety?.overall_risk || "UNKNOWN";
  const score = result.score?.score ?? "N/A";

  const cardW = (contentWidth - 9) / 4;
  const cardH = 20;
  const summaryItems = [
    { label: "MEDICINES", value: String(medicines.length), color: COLORS.primary },
    { label: "VERIFIED", value: String(verifiedCount), color: COLORS.success },
    { label: "RISK", value: overallRisk, color: riskColor(overallRisk) },
    { label: "AI SCORE", value: `${score}%`, color: COLORS.primary },
  ];

  summaryItems.forEach((item, i) => {
    const cardX = marginX + i * (cardW + 3);
    doc.setFillColor(...COLORS.bgLight);
    doc.setDrawColor(...COLORS.border);
    doc.roundedRect(cardX, y, cardW, cardH, 2, 2, "FD");

    doc.setFontSize(7.5);
    doc.setFont(undefined, "normal");
    doc.setTextColor(...COLORS.textMuted);
    doc.text(item.label, cardX + 4, y + 7);

    doc.setFontSize(13);
    doc.setFont(undefined, "bold");
    doc.setTextColor(...item.color);
    const displayValue = item.value.length > 10 ? item.value.slice(0, 9) + "…" : item.value;
    doc.text(displayValue, cardX + 4, y + 15.5);
  });

  y += cardH + 12;

  // -------------------------------------------------------
  // Patient Information
  // -------------------------------------------------------
  sectionHeader("Patient Information");

  doc.setDrawColor(...COLORS.border);
  doc.setFillColor(...COLORS.bgLight);
  const patientBoxH = 22;
  doc.roundedRect(marginX, y, contentWidth, patientBoxH, 2, 2, "FD");

  const colW = contentWidth / 3;
  labelValue("Patient", result.patient_name, marginX + 5, colW - 10);
  labelValue("Doctor", result.doctor_name, marginX + colW + 5, colW - 10);
  labelValue("Hospital", result.hospital, marginX + colW * 2 + 5, colW - 10);

  y += patientBoxH + 10;

  // -------------------------------------------------------
  // Medicines (with education - the important AI findings)
  // -------------------------------------------------------
  sectionHeader(`Medicines Detected (${medicines.length})`);

  medicines.forEach((medicine, index) => {
    ensureSpace(30);

    const cardStartY = y;
    doc.setDrawColor(...COLORS.border);
    doc.setFillColor(255, 255, 255);

    // Name + verification badge
    doc.setFont(undefined, "bold");
    doc.setFontSize(11.5);
    doc.setTextColor(...COLORS.textDark);
    doc.text(`${index + 1}. ${medicine.name || "Unknown"}`, marginX + 2, y + 6);

    const verified = medicine.database_verified;
    badge(
      verified ? "DATABASE VERIFIED" : "AI ESTIMATED",
      marginX + 2,
      y + 12,
      verified ? COLORS.success : COLORS.warning
    );

    y += 18;

    // Dosage / Frequency / Duration / Instructions - 2 column grid
    const gridColW = contentWidth / 2;
    const rowStartY = y;
    let leftH = labelValue("Dosage", medicine.dosage, marginX + 2, gridColW - 10);
    labelValue("Frequency", medicine.frequency, marginX + gridColW, gridColW - 10);
    y += Math.max(leftH, 8) + 7;

    let rightH = labelValue("Duration", medicine.duration, marginX + 2, gridColW - 10);
    labelValue("Instructions", medicine.instructions, marginX + gridColW, gridColW - 10);
    y += Math.max(rightH, 8) + 7;

    // Generic / brand / category if known
    if (medicine.generic_name || medicine.brand_name) {
      let genH = labelValue("Generic Name", medicine.generic_name, marginX + 2, gridColW - 10);
      labelValue("Category", medicine.category, marginX + gridColW, gridColW - 10);
      y += Math.max(genH, 8) + 7;
    }

    // Issues found
    if (medicine.issues && medicine.issues.length > 0) {
      ensureSpace(10);
      doc.setFont(undefined, "bold");
      doc.setFontSize(9);
      doc.setTextColor(...COLORS.warning);
      doc.text("Issues: " + medicine.issues.join(", "), marginX + 2, y);
      y += 7;
    }

    // Medicine education - the important AI-analyzed content
    const edu = medicine.education;
    if (edu && edu.purpose && edu.purpose !== "UNKNOWN") {
      ensureSpace(8);
      doc.setDrawColor(...COLORS.border);
      doc.line(marginX + 2, y, marginX + contentWidth - 2, y);
      y += 6;

      doc.setFont(undefined, "bold");
      doc.setFontSize(9.5);
      doc.setTextColor(...COLORS.primary);
      doc.text("AI MEDICINE EDUCATION", marginX + 2, y);
      y += 6;

      if (edu.purpose) {
        wrappedText(`Purpose: ${edu.purpose}`, marginX + 2, contentWidth - 4, 9.5);
        y += 2;
      }
      if (edu.how_to_take) {
        wrappedText(`How to take: ${edu.how_to_take}`, marginX + 2, contentWidth - 4, 9.5);
        y += 2;
      }
      if (edu.warnings && edu.warnings.length > 0) {
        const warningsText = Array.isArray(edu.warnings) ? edu.warnings.join("; ") : edu.warnings;
        wrappedText(`Warnings: ${warningsText}`, marginX + 2, contentWidth - 4, 9.5, COLORS.danger);
        y += 2;
      }
      if (edu.common_side_effects && edu.common_side_effects.length > 0) {
        const sideEffectsText = Array.isArray(edu.common_side_effects)
          ? edu.common_side_effects.join(", ")
          : edu.common_side_effects;
        wrappedText(`Side effects: ${sideEffectsText}`, marginX + 2, contentWidth - 4, 9.5);
        y += 2;
      }
    }

    y += 4;
    // Card border around the whole medicine block
    doc.setDrawColor(...COLORS.border);
    doc.roundedRect(marginX, cardStartY - 3, contentWidth, y - cardStartY, 2, 2, "D");
    y += 8;
  });

  // -------------------------------------------------------
  // Safety Analysis
  // -------------------------------------------------------
  sectionHeader("Safety Analysis");

  ensureSpace(14);
  const riskBadgeColor = riskColor(overallRisk);
  doc.setFillColor(...riskBadgeColor);
  doc.roundedRect(marginX, y, contentWidth, 12, 2, 2, "F");
  doc.setTextColor(...COLORS.white);
  doc.setFont(undefined, "bold");
  doc.setFontSize(11);
  doc.text(`Overall Risk: ${overallRisk}`, marginX + 5, y + 8);
  y += 18;

  const alerts = result.safety?.alerts || [];
  if (alerts.length === 0) {
    doc.setFont(undefined, "normal");
    doc.setFontSize(10);
    doc.setTextColor(...COLORS.success);
    doc.text("No safety issues detected.", marginX + 2, y);
    y += 10;
  } else {
    alerts.forEach((alert) => {
      ensureSpace(16);
      const sevColor = severityColor(alert.severity);

      doc.setFillColor(...sevColor);
      doc.rect(marginX, y - 4, 2, 12, "F");

      doc.setFont(undefined, "bold");
      doc.setFontSize(9.5);
      doc.setTextColor(...COLORS.textDark);
      doc.text(`${alert.type || "Alert"} — ${alert.medicine || ""}`, marginX + 5, y);
      y += 5;

      const msgLines = doc.splitTextToSize(alert.message || "", contentWidth - 8);
      doc.setFont(undefined, "normal");
      doc.setFontSize(9);
      doc.setTextColor(...COLORS.textMuted);
      doc.text(msgLines, marginX + 5, y);
      y += msgLines.length * 4.5 + 6;
    });
  }

  y += 4;

  // -------------------------------------------------------
  // Score Breakdown
  // -------------------------------------------------------
  sectionHeader("AI Prescription Score");

  ensureSpace(20);
  doc.setFont(undefined, "bold");
  doc.setFontSize(24);
  doc.setTextColor(...riskColor(result.score?.risk_level));
  doc.text(`${score}`, marginX, y + 10);
  doc.setFontSize(11);
  doc.setTextColor(...COLORS.textMuted);
  doc.text("/100", marginX + doc.getTextWidth(`${score}`) + 2, y + 10);

  doc.setFont(undefined, "normal");
  doc.setFontSize(10);
  doc.setTextColor(...COLORS.textDark);
  doc.text(`Risk Level: ${result.score?.risk_level || "Unknown"}`, marginX, y + 18);
  y += 26;

  const reasons = result.score?.reasons || [];
  if (reasons.length > 0) {
    doc.setFont(undefined, "bold");
    doc.setFontSize(9.5);
    doc.setTextColor(...COLORS.textDark);
    doc.text("Score Breakdown:", marginX, y);
    y += 6;

    reasons.forEach((reason) => {
      ensureSpace(7);
      doc.setFont(undefined, "normal");
      doc.setFontSize(9);
      doc.setTextColor(...COLORS.textMuted);
      const reasonLines = doc.splitTextToSize(`•  ${reason}`, contentWidth - 4);
      doc.text(reasonLines, marginX + 2, y);
      y += reasonLines.length * 4.5 + 2;
    });
  }

  // -------------------------------------------------------
  // Footer on every page
  // -------------------------------------------------------
  const pageCount = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setDrawColor(...COLORS.border);
    doc.line(marginX, pageHeight - 15, pageWidth - marginX, pageHeight - 15);

    doc.setFont(undefined, "normal");
    doc.setFontSize(7.5);
    doc.setTextColor(...COLORS.textMuted);
    doc.text(
      "Generated by CuraLens AI — This report is AI-assisted and should be reviewed by a healthcare professional.",
      marginX,
      pageHeight - 9
    );
    doc.text(`Page ${i} of ${pageCount}`, pageWidth - marginX, pageHeight - 9, { align: "right" });
  }

  doc.save("CuraLens_Report.pdf");
}
