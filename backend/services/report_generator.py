"""
CareerPath AI - Professional PDF Report Generator
Build For Bharat 2.0 | Intelligent Talent & Workforce Ecosystem
"""

import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def clean_text(val) -> str:
    if val is None:
        return ""
    # Replace unicode rupee symbol with INR for PDF rendering safety
    s = str(val).replace("₹", "INR ")
    return s

def generate_pdf_report(user_profile: dict, gap_analysis: dict, recommendations: list[dict], roadmap: list[dict]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=TA_LEFT
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569')
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e293b')
    )

    bold_body_style = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0f172a')
    )

    story = []

    # Title & Subtitle Header
    story.append(Paragraph("CareerPath AI | Workforce Intelligence Report", title_style))
    story.append(Paragraph("Build For Bharat 2.0 — AI Skill Gap Analysis & Predictive Career Analytics", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3b82f6'), spaceAfter=10))

    # Executive Summary Card
    fit_score = gap_analysis.get('fit_score', 0)
    essential_cov = gap_analysis.get('essential_coverage', 0)
    pred_salary = clean_text(gap_analysis.get('predicted_salary', 'INR 7.5 - 14.0 LPA'))
    
    summary_data = [
        [
            Paragraph("<b>Overall Fit Score</b>", body_style),
            Paragraph("<b>Essential Coverage</b>", body_style),
            Paragraph("<b>ML Predicted CTC (India)</b>", body_style),
        ],
        [
            Paragraph(f"<font size=14 color='#2563eb'><b>{fit_score}%</b></font>", body_style),
            Paragraph(f"<font size=14 color='#059669'><b>{essential_cov}%</b></font>", body_style),
            Paragraph(f"<font size=12 color='#7c3aed'><b>{pred_salary}</b></font>", body_style),
        ]
    ]
    summary_table = Table(summary_data, colWidths=[180, 180, 180])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))

    # Candidate Profile Overview
    story.append(Paragraph("Candidate Profile Snapshot", section_style))
    skills_list = user_profile.get("skills", [])
    skills_preview = ", ".join(skills_list[:15]) if isinstance(skills_list, list) else str(skills_list)
    edu_raw = user_profile.get("education", [])
    if isinstance(edu_raw, list) and edu_raw:
        edu_items = []
        for e in edu_raw:
            if isinstance(e, dict):
                d = e.get("degree", "")
                inst = e.get("institution", "")
                yr = e.get("year", "")
                part = f"{d} ({inst})" if inst else d
                if yr:
                    part += f" - {yr}"
                edu_items.append(part)
            else:
                edu_items.append(str(e))
        edu = "; ".join(edu_items)
    else:
        edu = str(edu_raw) if edu_raw else "Not specified"

    exp_raw = user_profile.get("experience", [])
    if isinstance(exp_raw, list) and exp_raw:
        exp_items = []
        for x in exp_raw:
            if isinstance(x, dict):
                r = x.get("role", "")
                c = x.get("company", "")
                dur = x.get("duration", "")
                part = f"{r} at {c}" if c else r
                if dur:
                    part += f" ({dur})"
                exp_items.append(part)
            else:
                exp_items.append(str(x))
        exp = "; ".join(exp_items)
    elif isinstance(exp_raw, dict):
        if exp_raw.get("role"):
            exp = f"{exp_raw.get('role')} at {exp_raw.get('company', '')}"
        elif exp_raw.get("years"):
            exp = f"{exp_raw.get('years')} Years Experience"
        else:
            exp = "Fresher / Entry Level"
    else:
        exp = str(exp_raw) if exp_raw else "Fresher / Entry Level"
    
    profile_data = [
        [Paragraph("<b>Normalized Skills:</b>", bold_body_style), Paragraph(clean_text(skills_preview) or "None detected", body_style)],
        [Paragraph("<b>Education:</b>", bold_body_style), Paragraph(clean_text(edu), body_style)],
        [Paragraph("<b>Experience:</b>", bold_body_style), Paragraph(clean_text(exp), body_style)],
    ]
    p_table = Table(profile_data, colWidths=[130, 410])
    p_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 10))

    # Skill Gap Breakdown
    story.append(Paragraph("Competency & Skill Gap Analysis", section_style))
    missing_ess = gap_analysis.get('missing_essential', [])
    missing_opt = gap_analysis.get('missing_optional', [])
    matched_skills = gap_analysis.get('matched_skills', [])

    gap_data = [
        [Paragraph("<b>Competency Category</b>", bold_body_style), Paragraph("<b>Identified Skills</b>", bold_body_style)],
        [Paragraph("<font color='#059669'><b>Matched Skills</b></font>", body_style), Paragraph(clean_text(", ".join(matched_skills[:12])) or "None", body_style)],
        [Paragraph("<font color='#dc2626'><b>Missing Essential</b></font>", body_style), Paragraph(clean_text(", ".join(missing_ess[:10])) or "Full match achieved!", body_style)],
        [Paragraph("<font color='#d97706'><b>Missing Optional</b></font>", body_style), Paragraph(clean_text(", ".join(missing_opt[:10])) or "None", body_style)],
    ]
    gap_table = Table(gap_data, colWidths=[140, 400])
    gap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(gap_table)
    story.append(Spacer(1, 10))

    # Top Recommended Career Pathways
    if recommendations:
        story.append(Paragraph("Top Recommended Career Pathways (ML Ranked)", section_style))
        rec_data = [[
            Paragraph("<b>Target Role</b>", bold_body_style),
            Paragraph("<b>Fit Score</b>", bold_body_style),
            Paragraph("<b>Market Intelligence & Explanatory Rationale</b>", bold_body_style)
        ]]
        for rec in recommendations[:5]:
            rec_data.append([
                Paragraph(f"<b>{clean_text(rec.get('role_title', ''))}</b>", body_style),
                Paragraph(f"{rec.get('score', 0):.1f}%", body_style),
                Paragraph(clean_text(rec.get('explanation', '')), body_style)
            ])
        rec_table = Table(rec_data, colWidths=[130, 60, 350])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(rec_table)
        story.append(Spacer(1, 10))

    # Learning Roadmap
    if roadmap:
        story.append(Paragraph("Curated Upskilling & Project Roadmap", section_style))
        rm_data = [[
            Paragraph("<b>Week</b>", bold_body_style),
            Paragraph("<b>Skill</b>", bold_body_style),
            Paragraph("<b>Recommended Course</b>", bold_body_style),
            Paragraph("<b>Platform</b>", bold_body_style),
            Paragraph("<b>Applied Project</b>", bold_body_style)
        ]]
        for entry in roadmap[:6]:
            plat = clean_text(entry.get('platform', ''))
            if entry.get('is_govt_initiative') or entry.get('initiative'):
                init_name = clean_text(entry.get('initiative') or 'Govt Initiative')
                plat = f"{plat}<br/><font color='#c2410c' size='7'><b>[Govt: {init_name}]</b></font>"
            rm_data.append([
                Paragraph(f"W{entry.get('week', 1)}", body_style),
                Paragraph(f"<b>{clean_text(entry.get('skill', ''))}</b>", body_style),
                Paragraph(clean_text(entry.get('course', '')), body_style),
                Paragraph(plat, body_style),
                Paragraph(clean_text(entry.get('project', '')), body_style)
            ])
        rm_table = Table(rm_data, colWidths=[40, 90, 150, 90, 170])
        rm_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#cbd5e1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(rm_table)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
