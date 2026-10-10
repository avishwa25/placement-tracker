import io
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


def build_applications_pdf(student_name, applications):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), title="Applications")
    styles = getSampleStyleSheet()
    cell = styles["BodyText"]

    def p(text):
        # escape() stops user text like "<b>" from breaking the PDF
        return Paragraph(escape(str(text or "")), cell)

    story = [
        Paragraph(f"Job applications: {escape(student_name)}", styles["Title"]),
        Spacer(1, 12),
    ]

    data = [["Company", "Role", "Applied on", "Status", "Notes"]]
    for a in applications:
        data.append([
            p(a["company_name"]),
            p(a["job_role"]),
            p(a["applied_on"]),
            p(a["status"]),
            p(a["notes"]),
        ])

    table = Table(data, repeatRows=1, colWidths=[140, 140, 80, 80, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4e79a7")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer