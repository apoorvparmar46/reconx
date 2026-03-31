from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from datetime import datetime
import whois
import dns.resolver
import requests
import hashlib

def generate_report(target, output_file="reconx_report.pdf"):
    doc = SimpleDocTemplate(output_file, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#00FF41'),
        spaceAfter=10
    )

    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#00BFFF'),
        spaceAfter=6
    )

    # Title
    story.append(Paragraph("🕵️ ReconX OSINT Report", title_style))
    story.append(Paragraph(f"Target: {target}", styles['Normal']))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 0.3 * inch))

    # WHOIS Section
    story.append(Paragraph("WHOIS Information", header_style))
    try:
        w = whois.whois(target)
        whois_data = [
            ["Field", "Value"],
            ["Domain", str(w.domain_name)],
            ["Registrar", str(w.registrar)],
            ["Created", str(w.creation_date)],
            ["Expires", str(w.expiration_date)],
            ["Name Servers", str(w.name_servers)],
        ]
        t = Table(whois_data, colWidths=[2 * inch, 4 * inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ]))
        story.append(t)
    except Exception as e:
        story.append(Paragraph(f"WHOIS failed: {e}", styles['Normal']))

    story.append(Spacer(1, 0.3 * inch))

    # DNS Section
    story.append(Paragraph("DNS Records", header_style))
    dns_data = [["Type", "Value"]]
    for record in ["A", "MX", "TXT", "NS"]:
        try:
            answers = dns.resolver.resolve(target, record)
            for r in answers:
                dns_data.append([record, str(r)])
        except:
            dns_data.append([record, "Not found"])

    t2 = Table(dns_data, colWidths=[1 * inch, 5 * inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.3 * inch))

    # IP Section
    story.append(Paragraph("IP Intelligence", header_style))
    try:
        response = requests.get(f"http://ip-api.com/json/{target}")
        data = response.json()
        ip_data = [
            ["Field", "Value"],
            ["IP", data.get("query", "N/A")],
            ["Country", data.get("country", "N/A")],
            ["City", data.get("city", "N/A")],
            ["ISP", data.get("isp", "N/A")],
            ["Org", data.get("org", "N/A")],
        ]
        t3 = Table(ip_data, colWidths=[2 * inch, 4 * inch])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ]))
        story.append(t3)
    except Exception as e:
        story.append(Paragraph(f"IP lookup failed: {e}", styles['Normal']))

    doc.build(story)
    print(f"\n✅ Report saved as: {output_file}\n")