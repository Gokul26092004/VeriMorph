import os
from pathlib import Path

def export_pdf(title: str, text_content: str, output_path: str) -> str:
    """
    Exports content to PDF report.
    Uses reportlab if installed, with a clean HTML/printable fallback.
    """
    path = Path(output_path)
    os.makedirs(path.parent, exist_ok=True)

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        doc = SimpleDocTemplate(str(path), pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
        styles = getSampleStyleSheet()
        
        story = []
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=14
        )
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155'),
            spaceAfter=8
        )

        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))

        for para in text_content.split("\n\n"):
            clean_para = para.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
            if clean_para.strip():
                story.append(Paragraph(clean_para, body_style))

        doc.build(story)
        return str(path)
    except Exception:
        # Fallback to HTML document formatted for PDF printing
        fallback_path = path.with_suffix(".html")
        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 40px; color: #1e293b; line-height: 1.6; max-width: 800px; margin: 0 auto; }}
    h1 {{ color: #0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; }}
    pre {{ background: #f8fafc; padding: 15px; border-radius: 6px; border: 1px solid #e2e8f0; white-space: pre-wrap; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <pre>{text_content}</pre>
</body>
</html>"""
        with open(fallback_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return str(fallback_path)
