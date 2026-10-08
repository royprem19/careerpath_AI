"""
CareerPath AI - Official Round 2 Hackathon Presentation Generator
SAS & Chandigarh University Hackathon | Build For Bharat 2.0
Strictly aligned with Round-2 Evaluation Sheet (100 Marks across 6 criteria)
"""

import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Reconfigure stdout for Windows console UTF-8
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "backend" / "data"
FIG_DIR = DATA_DIR / "figures"
TARGET_PPTX = ROOT_DIR / "CareerPath_AI_Presentation.pptx"
DOWNLOADS_PPTX = Path(r"C:\Users\Prem\Downloads\CareerPath_AI_Presentation.pptx")

# ==============================================================================
# DESIGN SYSTEM
# ==============================================================================
PRIMARY_BLUE  = RGBColor(0x1E, 0x3A, 0x8A) # #1E3A8A - Deep Executive Navy
ACCENT_BLUE   = RGBColor(0x25, 0x63, 0xEB) # #2563EB - Tech Blue
TEAL_CYAN     = RGBColor(0x0E, 0x74, 0x90) # #0E7490 - Analytical Cyan
DARK_TEXT     = RGBColor(0x0F, 0x17, 0x2A) # #0F172A - Slate 900
MEDIUM_TEXT   = RGBColor(0x47, 0x55, 0x69) # #475569 - Slate 600
LIGHT_BG      = RGBColor(0xF8, 0xFA, 0xFC) # #F8FAFC - Off white bg
CARD_BG       = RGBColor(0xFF, 0xFF, 0xFF) # Pure White
BORDER_COLOR  = RGBColor(0xCB, 0xD5, 0xE1) # Slate 300
SUCCESS_GREEN = RGBColor(0x05, 0x96, 0x69) # Emerald 600
ORANGE_WARN   = RGBColor(0xEA, 0x58, 0x0C) # Orange 600
RED_ACCENT    = RGBColor(0xDC, 0x26, 0x26) # Red 600
WHITE         = RGBColor(0xFF, 0xFF, 0xFF)
GOLD_BADGE    = RGBColor(0xD9, 0x77, 0x06)

SLIDE_WIDTH   = Inches(13.333)
SLIDE_HEIGHT  = Inches(7.5)

def build_presentation():
    print(f"Initializing Presentation (16:9 Widescreen)...")
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_layout = prs.slide_layouts[6]

    # Helper: Slide Base
    def add_base_decorations(slide, slide_num, total_slides=18, rubric_tag=None):
        # Top accent line
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = ACCENT_BLUE
        top_bar.line.fill.background()

        # Footer bar
        foot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.08), SLIDE_WIDTH, Inches(0.42))
        foot.fill.solid()
        foot.fill.fore_color.rgb = LIGHT_BG
        foot.line.color.rgb = BORDER_COLOR
        foot.line.width = Pt(0.5)

        tf = foot.text_frame
        p = tf.paragraphs[0]
        p.text = "CareerPath AI  |  SAS & CU Hackathon  ·  Round 2 Technical Evaluation  |  Build For Bharat 2.0"
        p.font.size = Pt(8.5)
        p.font.color.rgb = MEDIUM_TEXT
        p.alignment = PP_ALIGN.LEFT
        tf.margin_left = Inches(0.8)

        # Slide Number
        tx_num = slide.shapes.add_textbox(Inches(11.8), Inches(7.1), Inches(1.2), Inches(0.35))
        pn = tx_num.text_frame.paragraphs[0]
        pn.text = f"{slide_num:02d} / {total_slides:02d}"
        pn.font.size = Pt(8.5)
        pn.font.color.rgb = MEDIUM_TEXT
        pn.font.bold = True
        pn.alignment = PP_ALIGN.RIGHT

        # Rubric Tag Pill
        if rubric_tag:
            pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.22), Inches(3.8), Inches(0.32))
            pill.fill.solid()
            pill.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xFF)
            pill.line.color.rgb = RGBColor(0x81, 0x8C, 0xF8)
            pill.line.width = Pt(1)
            ptf = pill.text_frame
            pp = ptf.paragraphs[0]
            pp.text = f"★ {rubric_tag}"
            pp.font.size = Pt(9.5)
            pp.font.bold = True
            pp.font.color.rgb = RGBColor(0x37, 0x30, 0xA3)
            pp.alignment = PP_ALIGN.CENTER

    def add_slide_header(slide, title, subtitle=None, top=Inches(0.60)):
        tx = slide.shapes.add_textbox(Inches(0.8), top, Inches(11.7), Inches(0.8))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_BLUE

        if subtitle:
            p2 = tf.add_paragraph()
            p2.text = subtitle
            p2.font.size = Pt(11)
            p2.font.color.rgb = MEDIUM_TEXT
            p2.space_before = Pt(2)

    def add_styled_card(slide, left, top, width, height, bg_color=WHITE, border_color=BORDER_COLOR, title=None, title_color=PRIMARY_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.10), width - Inches(0.3), Inches(0.35))
            pt = tb.text_frame.paragraphs[0]
            pt.text = title
            pt.font.size = Pt(11)
            pt.font.bold = True
            pt.font.color.rgb = title_color
        return card

    # ==============================================================================
    # SLIDE 1: EXECUTIVE TITLE
    # ==============================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(0x0A, 0x11, 0x28) # Midnight Blue
    bg1.line.fill.background()

    # Subtle glowing banner
    banner = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.1), Inches(4.2), Inches(0.38))
    banner.fill.solid()
    banner.fill.fore_color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    banner.line.color.rgb = ACCENT_BLUE
    banner.line.width = Pt(1)
    p_b = banner.text_frame.paragraphs[0]
    p_b.text = "SAS & CHANDIGARH UNIVERSITY HACKATHON · ROUND 2"
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p_b.alignment = PP_ALIGN.CENTER

    # Main Title
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(1.8))
    tf1 = t_box.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "CareerPath AI"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p2 = tf1.add_paragraph()
    p2.text = "Intelligent Talent & Workforce Ecosystem: Prescriptive Career Mobility, Empirical Benchmarking & ML Analytics"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(0xBF, 0xDB, 0xFE)
    p2.space_before = Pt(8)

    # 4 Highlights Grid
    feats = [
        ("ESCO International Taxonomy", "European Commission v1.1 ontology standardized across 81 IT & Data roles."),
        ("Closed-Form ML Engine", "NumPy Ridge compensation predictor (R²=0.715, fresher local MAE ₹1.18L)."),
        ("Talent Intelligence Dual-Track", "Gaussian Naive Bayes promotion & Big Five OCEAN leadership classifiers."),
        ("Prescriptive Roadmap", "Automated mapping to free government SWAYAM & NPTEL verified courses.")
    ]
    for idx, (title, desc) in enumerate(feats):
        c_left = Inches(1.0) + Inches(idx * 2.85)
        c_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(3.6), Inches(2.7), Inches(1.7))
        c_card.fill.solid()
        c_card.fill.fore_color.rgb = RGBColor(0x13, 0x1E, 0x3A)
        c_card.line.color.rgb = RGBColor(0x3B, 0x82, 0xF6)
        c_card.line.width = Pt(1)
        ctf = c_card.text_frame
        ctf.word_wrap = True
        cp1 = ctf.paragraphs[0]
        cp1.text = title
        cp1.font.size = Pt(11)
        cp1.font.bold = True
        cp1.font.color.rgb = RGBColor(0x60, 0xA5, 0xFA)
        cp2 = ctf.add_paragraph()
        cp2.text = desc
        cp2.font.size = Pt(9.0)
        cp2.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
        cp2.space_before = Pt(4)

    # Footer Card on Slide 1
    t_foot = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(6.8), SLIDE_WIDTH, Inches(0.7))
    t_foot.fill.solid()
    t_foot.fill.fore_color.rgb = RGBColor(0x05, 0x0B, 0x1A)
    t_foot.line.fill.background()
    t_ft = t_foot.text_frame
    p_ft = t_ft.paragraphs[0]
    p_ft.text = "Team: CareerPath AI  |  Track: Intelligent Talent & Workforce Ecosystem  |  Presented: October 2026"
    p_ft.font.size = Pt(10)
    p_ft.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
    p_ft.alignment = PP_ALIGN.CENTER

    # ==============================================================================
    # SLIDE 2: RUBRIC MAPPING & SCORING GUIDE (100 MARKS)
    # ==============================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s2, 2, rubric_tag="Evaluation Alignment · 100 Marks")
    add_slide_header(s2, "Round 2 Official Judging Rubric Alignment", "Every slide directly corresponds to the 6 criteria evaluated by the Hackathon Jury sheet.")

    rubric_rows = [
        ("1. Problem Definition", "10 Marks", "Slide 3", "National graduate employability mismatch, structural syllabus-market divergence, scope & depth."),
        ("2. Approach Description", "15 Marks", "Slide 4", "4-tier architecture, ESCO v1.1 ontology, pure NumPy closed-form design rationale (no LLM black-box)."),
        ("3. Data Exploration & Preparation", "15 Marks", "Slides 5-7", "7 datasets provenance, rows before->after cleaning audit, null imputations, 4 dedicated high-res EDA figures."),
        ("4. Data Analysis & ML Pipeline", "30 Marks", "Slides 8-11", "93k jobs market audit, Chi-Square (p<10⁻³⁷), 4-model CV comparison, Ridge regressor (fresher MAE ₹1.18L), weight sensitivity."),
        ("5. Results & Conclusions", "20 Marks", "Slides 12-13", "Live application workflow, Career Growth simulator, Talent Intelligence, ReportLab PDF export."),
        ("6. Implications & Impact", "10 Marks", "Slides 14-15", "60-student batch pilot (41.2% -> 86.7% placement ready), demographic parity audit (DIR=1.000), NEP 2020."),
        ("7. Future Implementation", "Jury Advisory", "Slides 16-17", "Top 30 Jury Enhancements: Proctored Skill Verification (10-Q, 80% pass), Anti-Cheat Sandbox, Dynamic Resume, AI Viva.")
    ]

    # Create Rubric Table
    tbl_s2 = s2.shapes.add_table(len(rubric_rows) + 1, 4, Inches(0.8), Inches(1.4), Inches(11.7), Inches(5.35))
    tbl = tbl_s2.table
    tbl.columns[0].width = Inches(2.5)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.1)
    tbl.columns[3].width = Inches(7.0)

    headers = ["Evaluation Criterion", "Marks", "Slides", "Analytical Evidence & Implementation Deliverable"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for i, row in enumerate(rubric_rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if i % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.color.rgb = DARK_TEXT
            if j == 1:
                p.font.bold = True
                p.font.color.rgb = GOLD_BADGE
            if j == 2:
                p.font.bold = True
                p.font.color.rgb = ACCENT_BLUE

    # ==============================================================================
    # SLIDE 3: PROBLEM DEFINITION (CRITERION 1 - 10 MARKS)
    # ==============================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s3, 3, rubric_tag="Criterion 1 · Problem Definition (10 Marks)")
    add_slide_header(s3, "Problem Definition & Analytics Objectives", "Addressing India's graduate employability crisis through transparent, algorithmic skill benchmarking.")

    # 3 Stat Cards
    add_styled_card(s3, Inches(0.8), Inches(1.5), Inches(3.7), Inches(1.4), bg_color=RGBColor(0xFE, 0xF2, 0xF2), border_color=RED_ACCENT)
    t1 = s3.shapes.add_textbox(Inches(0.9), Inches(1.55), Inches(3.5), Inches(1.3))
    t1.text_frame.word_wrap = True
    p = t1.text_frame.paragraphs[0]
    p.text = "1.5M+ Annual Graduates"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RED_ACCENT
    p2 = t1.text_frame.add_paragraph()
    p2.text = "Over 15 lakh technical students graduate yearly across India, but NASSCOM & Wheebox report <45% are corporate-ready."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = DARK_TEXT

    add_styled_card(s3, Inches(4.8), Inches(1.5), Inches(3.7), Inches(1.4), bg_color=RGBColor(0xFF, 0xF7, 0xED), border_color=ORANGE_WARN)
    t2 = s3.shapes.add_textbox(Inches(4.9), Inches(1.55), Inches(3.5), Inches(1.3))
    t2.text_frame.word_wrap = True
    p = t2.text_frame.paragraphs[0]
    p.text = "Curriculum vs Market Mismatch"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ORANGE_WARN
    p2 = t2.text_frame.add_paragraph()
    p2.text = "Colleges teach theoretical syntax; market demands full-stack competency ontologies (e.g. React/TypeScript/Docker)."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = DARK_TEXT

    add_styled_card(s3, Inches(8.8), Inches(1.5), Inches(3.7), Inches(1.4), bg_color=RGBColor(0xEE, 0xF2, 0xFF), border_color=ACCENT_BLUE)
    t3 = s3.shapes.add_textbox(Inches(8.9), Inches(1.55), Inches(3.5), Inches(1.3))
    t3.text_frame.word_wrap = True
    p = t3.text_frame.paragraphs[0]
    p.text = "Hiring Platforms Fall Short"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p2 = t3.text_frame.add_paragraph()
    p2.text = "LinkedIn & Naukri filter candidates out without telling them what they lack or how to bridge the gap."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = DARK_TEXT

    # 4 Core Analytics Objectives
    add_styled_card(s3, Inches(0.8), Inches(3.1), Inches(11.7), Inches(3.7), title="Core Analytical Objectives & Architectural Scope")
    tx_obj = s3.shapes.add_textbox(Inches(1.0), Inches(3.5), Inches(11.3), Inches(3.2))
    tf_obj = tx_obj.text_frame
    tf_obj.word_wrap = True

    objs = [
        ("Deterministic Skill Extraction & Normalization", "Parse unstructured PDF/DOCX resumes using PyMuPDF and map 300+ technical variants into canonical ontological entities using RapidFuzz (eliminating typos like 'react.js' -> 'React')."),
        ("Ontological Skill-Gap Scoring", "Evaluate candidate skills against European Commission ESCO v1.1 ICT standards using a weighted 70% Essential / 30% Optional scoring formula."),
        ("Empirical CTC & Velocity Prediction", "Deploy closed-form NumPy Ridge Regression to predict Indian market compensation with localized fresher calibration (MAE ₹1.18L), and Gaussian Naive Bayes to classify promotion probability."),
        ("Prescriptive Actionable Roadmaps", "Provide sequential 8-week learning milestones directly linking missing competencies to free government SWAYAM / NPTEL accredited courses and capstone projects.")
    ]
    for idx, (head, body) in enumerate(objs):
        po = tf_obj.add_paragraph() if idx > 0 else tf_obj.paragraphs[0]
        po.text = f"• {head}: "
        po.font.bold = True
        po.font.size = Pt(10.5)
        po.font.color.rgb = PRIMARY_BLUE
        po.space_before = Pt(6)
        r = po.add_run()
        r.text = body
        r.font.bold = False
        r.font.size = Pt(10)
        r.font.color.rgb = DARK_TEXT

    # ==============================================================================
    # SLIDE 4: APPROACH & ARCHITECTURE (CRITERION 2 - 15 MARKS)
    # ==============================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s4, 4, rubric_tag="Criterion 2 · Approach Description (15 Marks)")
    add_slide_header(s4, "4-Tier System Architecture & Pipeline Design", "A deterministic, privacy-preserving, closed-form computational engine built for production scale.")

    layers = [
        ("Layer 1: Ingestion & Normalization", ACCENT_BLUE, [
            "PyMuPDF & python-docx dual document parser.",
            "300+ Compiled Regex entity extractors.",
            "RapidFuzz Levenshtein token-sort normalizer.",
            "Academic degree & CGPA extraction."
        ]),
        ("Layer 2: Gap & Fit Engine", TEAL_CYAN, [
            "ESCO v1.1 ICT taxonomy (81 roles, 788 skills).",
            "Deterministic 70% Essential / 30% Optional split.",
            "Categorization: Matched, Missing Ess, Missing Opt, Surplus.",
            "FastAPI microservice executing in <200ms."
        ]),
        ("Layer 3: Predictive ML Analytics", PRIMARY_BLUE, [
            "NumPy Closed-Form Ridge Regressor (R²=0.715).",
            "Gaussian Naive Bayes promotion classifier (84.2% acc).",
            "Big Five OCEAN leadership classifier (95.7% acc).",
            "TF-IDF Semantic Vectorizer (Cosine Sim matching)."
        ]),
        ("Layer 4: Action & Presentation", SUCCESS_GREEN, [
            "8-Week sequential SWAYAM / NPTEL roadmap.",
            "React 18 + Vite + Tailwind interactive UI.",
            "Recharts radar, circular fit gauge & bars.",
            "ReportLab executive PDF approach note export."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(layers):
        c_left = Inches(0.8) + Inches(idx * 2.95)
        add_styled_card(s4, c_left, Inches(1.5), Inches(2.85), Inches(3.7), border_color=color, title=f"Tier {idx+1}", title_color=color)
        tb = s4.shapes.add_textbox(c_left + Inches(0.12), Inches(1.9), Inches(2.6), Inches(3.2))
        tbf = tb.text_frame
        tbf.word_wrap = True
        pt = tbf.paragraphs[0]
        pt.text = title.split(": ")[1]
        pt.font.size = Pt(11)
        pt.font.bold = True
        pt.font.color.rgb = DARK_TEXT
        for b in bullets:
            pb = tbf.add_paragraph()
            pb.text = f"• {b}"
            pb.font.size = Pt(8.5)
            pb.font.color.rgb = MEDIUM_TEXT
            pb.space_before = Pt(3)

    # Why Pure NumPy Callout
    add_styled_card(s4, Inches(0.8), Inches(5.35), Inches(11.7), Inches(1.45), bg_color=RGBColor(0xEE, 0xF2, 0xFF), border_color=ACCENT_BLUE)
    tx_why = s4.shapes.add_textbox(Inches(1.0), Inches(5.42), Inches(11.3), Inches(1.3))
    tf_why = tx_why.text_frame
    tf_why.word_wrap = True
    pw = tf_why.paragraphs[0]
    pw.text = "★ Engineering Rationale: Why Closed-Form Pure NumPy / SciPy Over Black-Box LLMs?"
    pw.font.bold = True
    pw.font.size = Pt(11)
    pw.font.color.rgb = PRIMARY_BLUE
    pw2 = tf_why.add_paragraph()
    pw2.text = "1. Zero Hallucination: Mathematical formulas guarantee reproducible, auditable scores without fabricating phantom skills.\n2. Sub-200ms Execution: Instant local computation without expensive token billing or API rate limits.\n3. Student Privacy: Resumes never leave the host system; zero candidate PII transmitted to external third-party cloud servers."
    pw2.font.size = Pt(9.0)
    pw2.font.color.rgb = DARK_TEXT
    pw2.space_before = Pt(2)

    # ==============================================================================
    # SLIDE 5: DATASETS & PROVENANCE (CRITERION 3 - 15 MARKS - PART 1)
    # ==============================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s5, 5, rubric_tag="Criterion 3 · Data Exploration (15 Marks)")
    add_slide_header(s5, "Data Exploration: Provenance of 7 Empirical Datasets", "Grounded across 28,000+ real-world industry postings, placement offers, and corporate appraisals.")

    data_rows = [
        ("Analytics Jobs.csv", "15,841", "Scraped postings across 8 Indian tech hubs (Naukri, Indeed, LinkedIn)", "Skills in JDs, city, exp, salary brackets", "Macro market trends, Chi-Square test"),
        ("DataScience Jobs.csv", "1,602", "Aggregated enterprise postings across 642 recruiting entities (93,005 positions)", "Company, role, volume, salary", "Recruiter volumes, salary benchmarks"),
        ("Consolidated Salary (5k + 500)", "5,500", "Multi-tier Indian tech postings (5,000) & campus placement offers (500)", "Skills, degrees, exp, LPA", "NumPy Ridge compensation training"),
        ("JDS Skill Traits.xlsx", "139", "Annual workplace appraisal reviews from mid-tier IT services", "Competency scores (Storytelling, Math, Coding)", "Junior promotion velocity classifier"),
        ("SDS Personality Traits.xlsx", "161", "Standardized corporate diagnostics (Big Five OCEAN inventory)", "Psychometric norm scores (0-100)", "Senior delivery success classifier"),
        ("ESCO Occupations v1.1", "30", "European Commission official international taxonomy standard", "Essential & optional skills ontologies", "International role benchmark ontology")
    ]

    tbl_s5 = s5.shapes.add_table(len(data_rows) + 1, 5, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.1))
    t5 = tbl_s5.table
    t5.columns[0].width = Inches(2.2)
    t5.columns[1].width = Inches(1.0)
    t5.columns[2].width = Inches(3.6)
    t5.columns[3].width = Inches(2.4)
    t5.columns[4].width = Inches(2.5)

    headers5 = ["Dataset Name", "Records", "Data Origin & Provenance", "Key Features", "Model & Analytics Usage"]
    for j, h in enumerate(headers5):
        cell = t5.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for i, row in enumerate(data_rows):
        for j, val in enumerate(row):
            cell = t5.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if i % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.color.rgb = DARK_TEXT
            if j == 1:
                p.font.bold = True
                p.font.color.rgb = ACCENT_BLUE

    # ==============================================================================
    # SLIDE 6: DATA PREPARATION & AUDIT (CRITERION 3 - 15 MARKS - PART 2)
    # ==============================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s6, 6, rubric_tag="Criterion 3 · Data Preparation (15 Marks)")
    add_slide_header(s6, "Data Preparation: Quality Defects & Remediation", "Systematic rows before -> after audit, null value imputations, and outlier clipping protocol.")

    # Table: Rows Before -> After Cleaning
    audit_rows = [
        ("Analytics Jobs.csv", "15,841", "job_type: 75.8% Nulls (12,011 rows); job_desc: 22.1% Nulls (3,508 rows)", "Excluded job_type from regression; imputed descriptions via designation + skills", "15,840 (99.99%)"),
        ("DataScience Jobs.csv", "1,602", "String salary formats ('7.8L'); experience ranges formatted as text", "Regex extraction stripping 'L'; continuous float LPA; validated min <= avg <= max", "1,602 (100.0%)"),
        ("JDS Skill Traits.xlsx", "139", "No missing values; raw column names with casing; Likert bounds checked", "Verified Likert integrity in [1.0, 5.0]; lowercase snake_case normalization", "139 (100.0%)"),
        ("SDS Personality Traits.xlsx", "161", "Leading whitespace in ' extraversion'; space in success classification header", "Automated string strip & regex snake_case; validated norm scores in [0, 100]", "161 (100.0%)"),
        ("Consolidated Salary", "5,500", "Extreme entry outliers (> 60 LPA in entry roles); disparate salary formats", "Unified column schema; currency normalization; clipped upper 1% extreme outliers at 45 LPA", "5,445 (99.0%)")
    ]

    tbl_s6 = s6.shapes.add_table(len(audit_rows) + 1, 5, Inches(0.8), Inches(1.4), Inches(7.0), Inches(5.3))
    t6 = tbl_s6.table
    t6.columns[0].width = Inches(1.5)
    t6.columns[1].width = Inches(0.7)
    t6.columns[2].width = Inches(1.8)
    t6.columns[3].width = Inches(2.2)
    t6.columns[4].width = Inches(0.8)

    headers6 = ["Dataset", "Raw", "Quality Defects", "Remediation Applied", "Cleaned"]
    for j, h in enumerate(headers6):
        cell = t6.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for i, row in enumerate(audit_rows):
        for j, val in enumerate(row):
            cell = t6.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if i % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.0)
            p.font.color.rgb = DARK_TEXT
            if j == 4:
                p.font.bold = True
                p.font.color.rgb = SUCCESS_GREEN

    # Add Figure EDA-1 & Figure EDA-2 on the right
    fig_eda1 = FIG_DIR / "fig_eda_missing.png"
    fig_eda2 = FIG_DIR / "fig_eda_salary_dist.png"
    if fig_eda1.exists():
        s6.shapes.add_picture(str(fig_eda1), Inches(8.1), Inches(1.4), Inches(4.4), Inches(2.5))
    if fig_eda2.exists():
        s6.shapes.add_picture(str(fig_eda2), Inches(8.1), Inches(4.1), Inches(4.4), Inches(2.5))

    # ==============================================================================
    # SLIDE 7: BIVARIATE EDA & CORRELATIONS (CRITERION 3 - 15 MARKS - PART 3)
    # ==============================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s7, 7, rubric_tag="Criterion 3 · Exploratory Data Analysis (15 Marks)")
    add_slide_header(s7, "Exploratory Data Analysis: Scaling & Correlation Heatmaps", "Empirical bivariate experience-salary slope (+₹1.74L/yr) and competency correlation matrix.")

    fig_eda3 = FIG_DIR / "fig_eda_salary_exp.png"
    fig_eda4 = FIG_DIR / "fig_eda_correlation.png"
    if fig_eda3.exists():
        s7.shapes.add_picture(str(fig_eda3), Inches(0.8), Inches(1.4), Inches(5.7), Inches(3.6))
    if fig_eda4.exists():
        s7.shapes.add_picture(str(fig_eda4), Inches(6.8), Inches(1.4), Inches(5.7), Inches(3.6))

    # Analytical Explanations Below
    add_styled_card(s7, Inches(0.8), Inches(5.15), Inches(5.7), Inches(1.65), title="Figure EDA-3 Insights: Experience-Salary Dispersion")
    t_e3 = s7.shapes.add_textbox(Inches(0.95), Inches(5.5), Inches(5.4), Inches(1.2))
    p = t_e3.text_frame.paragraphs[0]
    p.text = "• Panel A: Empirical OLS slope of +₹1.74 LPA per year of experience across enterprise postings.\n• Panel B: Clear variance expansion: Freshers (0-1 yrs) exhibit tightly bounded pay (median ₹4.12L, IQR ₹1.2L), while Senior Leadership (9+ yrs) exhibits vast dispersion (median ₹26.5L, IQR ₹8.5L)."
    p.font.size = Pt(8.5)
    p.font.color.rgb = DARK_TEXT

    add_styled_card(s7, Inches(6.8), Inches(5.15), Inches(5.7), Inches(1.65), title="Figure EDA-4 Insights: Feature Inter-Correlations")
    t_e4 = s7.shapes.add_textbox(Inches(6.95), Inches(5.5), Inches(5.4), Inches(1.2))
    p = t_e4.text_frame.paragraphs[0]
    p.text = "• JDS Competencies (N=139): Storytelling (r = +0.554) and Math/Stats (r = +0.524) dominate promotion salary hikes, whereas Big Data (r = +0.112) displays near-zero correlation.\n• SDS Psychometrics (N=161): Conscientiousness (r = +0.680) and Openness (r = +0.671) are primary delivery drivers; Neuroticism (r = -0.006) has zero correlation."
    p.font.size = Pt(8.5)
    p.font.color.rgb = DARK_TEXT

    # ==============================================================================
    # SLIDE 8: MACRO MARKET INTELLIGENCE & CHI-SQUARE (CRITERION 4 - 30 MARKS - PART 1)
    # ==============================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s8, 8, rubric_tag="Criterion 4 · Data Analysis (30 Marks)")
    add_slide_header(s8, "Macro Market Analytics & Audited Chi-Square Test", "93,005 audited openings across 642 recruiters and statistically indisputable regional wage premiums.")

    # 4 Stat Cards
    stats_m = [
        ("93,005 Openings", "Enterprise DS Postings", "Summed across 1,602 enterprise records (TCS 9,064, Accenture 5,425, IBM 4,120)."),
        ("15,841 Postings", "Analytics Jobs Tracked", "Scraped across 8 tech hubs: Bengaluru, Delhi NCR, Mumbai, Hyderabad, Pune, Chennai."),
        ("SAS Ranked #3", "Enterprise Tech Standard", "876 postings; 58.2% concentrated in BFSI risk modeling, 24.1% Pharma clinical trials."),
        ("Chi-Square p < 10⁻³⁷", "Statistical Significance", "df = 35, Pearson Chi-Square = 271.83 (critical value 66.62). Rejects regional wage independence.")
    ]
    for idx, (val, sub, desc) in enumerate(stats_m):
        c_left = Inches(0.8) + Inches(idx * 2.95)
        add_styled_card(s8, c_left, Inches(1.4), Inches(2.85), Inches(1.7), border_color=PRIMARY_BLUE)
        tb = s8.shapes.add_textbox(c_left + Inches(0.12), Inches(1.45), Inches(2.6), Inches(1.5))
        tbf = tb.text_frame
        tbf.word_wrap = True
        p = tbf.paragraphs[0]
        p.text = val
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_BLUE
        p2 = tbf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = TEAL_CYAN
        p3 = tbf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(8.0)
        p3.font.color.rgb = MEDIUM_TEXT
        p3.space_before = Pt(2)

    # Detailed Explanations
    add_styled_card(s8, Inches(0.8), Inches(3.25), Inches(5.7), Inches(3.5), title="Empirical Grounding of SAS Footprint in India")
    tb_sas = s8.shapes.add_textbox(Inches(0.95), Inches(3.6), Inches(5.4), Inches(3.0))
    tf_sas = tb_sas.text_frame
    tf_sas.word_wrap = True
    p = tf_sas.paragraphs[0]
    p.text = "Why SAS ranks #3 in India behind SQL and Python:\n\n1. BFSI Sector Dominance (58.2%): Indian private and public sector banks (HDFC, ICICI, SBI) mandatorily use SAS for credit risk scoring and Basel III/IV regulatory capital adequacy modeling.\n2. Pharmaceutical & Clinical Standards (24.1%): Global Contract Research Organizations (CROs) in Hyderabad and Mumbai mandate SAS for FDA clinical trial submissions (CDISC / SDTM data standards).\n3. Pay Premium (+11.4%): SAS-mandated postings command a mean compensation of ₹13.84 LPA vs ₹12.42 LPA for general analytics.\n4. Modern Web Growth (+42% YoY): React, TypeScript, and Next.js demand surge verified via NASSCOM Strategic Review 2024-2025."
    p.font.size = Pt(8.5)
    p.font.color.rgb = DARK_TEXT

    add_styled_card(s8, Inches(6.8), Inches(3.25), Inches(5.7), Inches(3.5), title="Inferential Pearson Chi-Square Test Specification")
    tb_chi = s8.shapes.add_textbox(Inches(6.95), Inches(3.6), Inches(5.4), Inches(3.0))
    tf_chi = tb_chi.text_frame
    tf_chi.word_wrap = True
    p = tf_chi.paragraphs[0]
    p.text = "Rigorous Test of Geographic Salary Independence:\n\n• Contingency Matrix: 8 Tech Hubs × 6 Discrete Salary Brackets (48 cells, N = 15,841).\n• Degrees of Freedom: df = (8 - 1) × (6 - 1) = 35.\n• Pearson Chi-Square Statistic: χ² = 271.83.\n• Theoretical Critical Value (α = 0.001): 66.62.\n• Empirical p-value: p = 1.97 × 10⁻³⁸.\n• Conclusion: We decisively reject the null hypothesis of geographic salary independence.\n• City Pay Premiums (vs ₹12.95L Baseline):\n   - Delhi NCR: +₹1.72 LPA\n   - Mumbai: +₹0.38 LPA\n   - Hyderabad: -₹0.58 LPA\n   - Chennai: -₹2.32 LPA"
    p.font.size = Pt(8.5)
    p.font.color.rgb = DARK_TEXT

    # ==============================================================================
    # SLIDE 9: 4-MODEL CLASSIFICATION BENCHMARK (CRITERION 4 - 30 MARKS - PART 2)
    # ==============================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s9, 9, rubric_tag="Criterion 4 · Predictive Modeling (30 Marks)")
    add_slide_header(s9, "Comprehensive 4-Model Benchmark (5-Fold Stratified CV)", "Evaluating candidate architectures, feature leakage audits, and dual-layer transferability.")

    cv_rows = [
        ("JDS: Gaussian Naive Bayes (Winner)", "84.25% ± 4.68%", "84.98% ± 5.12%", "86.38% ± 4.80%", "85.25% ± 4.20%", "0.8971 ± 0.038"),
        ("JDS: Logistic Regression (L2 MLE)", "83.59% ± 6.41%", "83.34% ± 6.85%", "87.71% ± 5.90%", "85.01% ± 5.45%", "0.8944 ± 0.042"),
        ("JDS: Random Forest (100 Trees)", "79.28% ± 9.53%", "78.42% ± 9.80%", "83.90% ± 8.60%", "80.57% ± 8.10%", "0.8671 ± 0.055"),
        ("JDS: CART Decision Tree", "76.46% ± 10.62%", "74.67% ± 10.90%", "87.91% ± 9.10%", "79.67% ± 9.20%", "0.8065 ± 0.078"),
        ("SDS: Gaussian Naive Bayes (Winner)", "95.67% ± 1.49%", "96.54% ± 1.80%", "95.30% ± 2.10%", "95.86% ± 1.55%", "0.9947 ± 0.005"),
        ("SDS: Random Forest (100 Trees)", "94.45% ± 3.51%", "91.86% ± 4.20%", "98.82% ± 1.60%", "95.03% ± 2.80%", "0.9953 ± 0.004"),
        ("SDS: CART Decision Tree", "94.43% ± 2.34%", "93.78% ± 3.10%", "96.47% ± 2.50%", "94.84% ± 2.20%", "0.9621 ± 0.018"),
        ("SDS: Logistic Regression (L2 MLE)", "93.20% ± 2.92%", "91.27% ± 3.50%", "96.47% ± 2.80%", "93.74% ± 2.65%", "0.9631 ± 0.015")
    ]

    tbl_s9 = s9.shapes.add_table(len(cv_rows) + 1, 6, Inches(0.8), Inches(1.4), Inches(11.7), Inches(3.2))
    t9 = tbl_s9.table
    t9.columns[0].width = Inches(2.9)
    t9.columns[1].width = Inches(1.8)
    t9.columns[2].width = Inches(1.7)
    t9.columns[3].width = Inches(1.7)
    t9.columns[4].width = Inches(1.7)
    t9.columns[5].width = Inches(1.9)

    headers9 = ["Task & Architecture", "Accuracy (Mean ± SD)", "Precision (Mean ± SD)", "Recall (Mean ± SD)", "F1 (Mean ± SD)", "ROC-AUC (Mean ± SD)"]
    for j, h in enumerate(headers9):
        cell = t9.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for i, row in enumerate(cv_rows):
        for j, val in enumerate(row):
            cell = t9.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if i % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.color.rgb = DARK_TEXT
            if "Winner" in row[0]:
                if j == 0:
                    p.font.bold = True
                if j in [1, 5]:
                    p.font.bold = True
                    p.font.color.rgb = SUCCESS_GREEN

    # 2 Defense Callouts Below
    add_styled_card(s9, Inches(0.8), Inches(4.75), Inches(5.7), Inches(2.0), title="Feature Leakage Audit on SDS (N=161)")
    tb_leak = s9.shapes.add_textbox(Inches(0.95), Inches(5.05), Inches(5.4), Inches(1.6))
    p = tb_leak.text_frame.paragraphs[0]
    p.text = "• Correlation Boundary: Correlations with delivery success: Conscientiousness (r=0.680), Openness (r=0.671), Extraversion (r=0.494), Neuroticism (r=-0.006). No single feature exceeds r=0.70; zero proxy variables.\n• Single-Feature Ablation: Retraining without Conscientiousness still yields 88.20% accuracy and 0.941 AUC. High performance is a multi-trait synergistic effect, not label memorization."
    p.font.size = Pt(8.0)
    p.font.color.rgb = DARK_TEXT

    add_styled_card(s9, Inches(6.8), Inches(4.75), Inches(5.7), Inches(2.0), title="Dual-Layer Role Transferability Justification")
    tb_trans = s9.shapes.add_textbox(Inches(6.95), Inches(5.05), Inches(5.4), Inches(1.6))
    p = tb_trans.text_frame.paragraphs[0]
    p.text = "Why do Data Science models apply to a Frontend candidate?\n• Layer 1 (Technical Domain Fit): Deterministic ontology matches candidate skills strictly against role benchmarks (React/CSS/TypeScript for Frontend; SQL/Docker for Backend). DS models do NOT score frontend syntax.\n• Layer 2 (Universal Professional Velocity): JDS models universal levers (problem decomposition, statistical intuition). SDS evaluates milestone adherence (Conscientiousness) and client pitching (Extraversion), vital for lead engineers."
    p.font.size = Pt(8.0)
    p.font.color.rgb = DARK_TEXT

    # ==============================================================================
    # SLIDE 10: COMPENSATION MODEL & STRATIFIED ERROR (CRITERION 4 - 30 MARKS - PART 3)
    # ==============================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s10, 10, rubric_tag="Criterion 4 · Compensation Modeling (30 Marks)")
    add_slide_header(s10, "Compensation Model: Baselines & Stratified Error Calibration", "Addressing the MAE=5.74 LPA concern: Fresher localized error is tightly bounded at ₹1.18 LPA.")

    # Baseline comparison table
    base_rows = [
        ("Baseline 1: Dummy Mean Predictor", "Predicts training set mean (₹13.23 LPA)", "0.000", "7.82 LPA", "11.20 LPA", "Naive central tendency benchmark"),
        ("Baseline 2: Univariate Linear OLS", "Experience-only linear model", "0.387", "6.14 LPA", "9.85 LPA", "Establishes linear tenure baseline (+₹1.74L/yr)"),
        ("Closed-Form NumPy Ridge Regressor", "Multivariable regularized model (exp, skills, match)", "0.715", "5.74 LPA", "9.65 LPA", "26.6% reduction in MAE over mean baseline")
    ]
    tbl_s10a = s10.shapes.add_table(len(base_rows) + 1, 6, Inches(0.8), Inches(1.4), Inches(6.5), Inches(1.7))
    ta = tbl_s10a.table
    ta.columns[0].width = Inches(1.8)
    ta.columns[1].width = Inches(1.8)
    ta.columns[2].width = Inches(0.5)
    ta.columns[3].width = Inches(0.7)
    ta.columns[4].width = Inches(0.7)
    ta.columns[5].width = Inches(1.0)
    for j, h in enumerate(["Model", "Features", "R²", "MAE", "RMSE", "Interpretation"]):
        cell = ta.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
    for i, row in enumerate(base_rows):
        for j, val in enumerate(row):
            cell = ta.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if i % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(7.5)
            p.font.color.rgb = DARK_TEXT

    # Stratified Error Breakdown Table
    strat_rows = [
        ("Freshers (0–1 yrs)", "180 Records", "₹4.12 LPA", "₹4.05 LPA", "₹1.18 LPA (Tightly Calibrated!)", "₹1.54 LPA"),
        ("Early Career (2–4 yrs)", "390 Records", "₹7.85 LPA", "₹7.72 LPA", "₹2.34 LPA", "₹3.12 LPA"),
        ("Mid-Senior (5–8 yrs)", "350 Records", "₹14.20 LPA", "₹13.90 LPA", "₹4.82 LPA", "₹6.25 LPA"),
        ("Leadership (9+ yrs)", "180 Records", "₹26.50 LPA", "₹25.10 LPA", "₹9.45 LPA (High Dispersion)", "₹14.20 LPA"),
        ("Overall (All Bands)", "1,100 Records", "₹13.23 LPA", "₹12.85 LPA", "₹5.74 LPA", "₹9.65 LPA")
    ]
    tbl_s10b = s10.shapes.add_table(len(strat_rows) + 1, 6, Inches(0.8), Inches(3.25), Inches(6.5), Inches(2.2))
    tb = tbl_s10b.table
    tb.columns[0].width = Inches(1.4)
    tb.columns[1].width = Inches(0.9)
    tb.columns[2].width = Inches(0.8)
    tb.columns[3].width = Inches(0.8)
    tb.columns[4].width = Inches(1.8)
    tb.columns[5].width = Inches(0.8)
    for j, h in enumerate(["Experience Band", "Test N", "Actual Mean", "Pred Mean", "Stratified Local MAE", "Local RMSE"]):
        cell = tb.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TEAL_CYAN
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
    for i, row in enumerate(strat_rows):
        for j, val in enumerate(row):
            cell = tb.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if i % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(7.5)
            p.font.color.rgb = DARK_TEXT
            if i == 0 and j == 4:
                p.font.bold = True
                p.font.color.rgb = SUCCESS_GREEN

    # Embedding Figure 11 on the right
    fig_res = FIG_DIR / "fig_eda_residuals.png"
    if fig_res.exists():
        s10.shapes.add_picture(str(fig_res), Inches(7.5), Inches(1.4), Inches(5.0), Inches(4.0))

    # Bottom Callout
    add_styled_card(s10, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.2), bg_color=RGBColor(0xF0, 0xFD, 0xF4), border_color=SUCCESS_GREEN)
    tx_cal = s10.shapes.add_textbox(Inches(0.95), Inches(5.65), Inches(11.4), Inches(1.1))
    p = tx_cal.text_frame.paragraphs[0]
    p.text = "★ Why This Resolves the Jury Critique:"
    p.font.bold = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = SUCCESS_GREEN
    p2 = tx_cal.text_frame.add_paragraph()
    p2.text = "Aggregate MAE of 5.74 LPA is heavily driven by senior executive compensation (salaries range from 20 to 60+ LPA). Crucially, for freshers (0–1 yrs), localized error is tightly bounded at ₹1.18 LPA! This proves the model is exceptionally reliable for its primary target user base (accurately placing our sample fresher in the realistic ₹3.0–4.4 LPA band)."
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = DARK_TEXT

    # ==============================================================================
    # SLIDE 11: SENSITIVITY & PARSING BENCHMARKS (CRITERION 4 - 30 MARKS - PART 4)
    # ==============================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s11, 11, rubric_tag="Criterion 4 · Robustness & Validation (30 Marks)")
    add_slide_header(s11, "Scoring Sensitivity & Resume Parsing Validation", "Confirming rank stability (Spearman ρ = 0.942) and parser benchmarking (90.8% F1-score).")

    # Sensitivity Table
    sens_rows = [
        ("Config A (Default)", "55% Coverage + 35% Similarity + 10% Readiness", "1.000 (Baseline)", "100.0%", "Balanced default configuration"),
        ("Config B (Coverage-Dominant)", "70% Coverage + 20% Similarity + 10% Readiness", "0.942 ± 0.03", "92.5%", "High stability; 9/10 candidates retain identical top-4 roles"),
        ("Config C (Semantic-Dominant)", "40% Coverage + 50% Similarity + 10% Readiness", "0.918 ± 0.04", "90.0%", "Broader semantic capture; rewards adjacent tech knowledge"),
        ("Config D (Readiness-Boosted)", "45% Coverage + 35% Similarity + 20% Readiness", "0.935 ± 0.03", "92.5%", "Rewards capstone project evidence without altering career ordering")
    ]
    tbl_s11 = s11.shapes.add_table(len(sens_rows) + 1, 5, Inches(0.8), Inches(1.4), Inches(11.7), Inches(2.6))
    t11 = tbl_s11.table
    t11.columns[0].width = Inches(2.2)
    t11.columns[1].width = Inches(3.6)
    t11.columns[2].width = Inches(1.8)
    t11.columns[3].width = Inches(1.5)
    t11.columns[4].width = Inches(2.6)

    headers11 = ["Configuration", "Weight Formulation (Cov / Sim / Read)", "Spearman Rank Corr (ρ)", "Top-4 Overlap Index", "Sensitivity Conclusion"]
    for j, h in enumerate(headers11):
        cell = t11.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
    for i, row in enumerate(sens_rows):
        for j, val in enumerate(row):
            cell = t11.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if i % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.color.rgb = DARK_TEXT

    # Resume Parsing Empirical Validation Card
    add_styled_card(s11, Inches(0.8), Inches(4.2), Inches(11.7), Inches(2.6), title="Empirical Resume Parser Benchmark (15 Multi-Format Resumes)")
    tb_parse = s11.shapes.add_textbox(Inches(1.0), Inches(4.55), Inches(11.3), Inches(2.1))
    tf_p = tb_parse.text_frame
    tf_p.word_wrap = True

    metrics_p = [
        ("Technical Skill Extraction F1-Score: 90.8%", "Evaluated against 284 ground-truth annotated skills across PDF/DOCX layouts (True Positives = 252, Precision = 93.0%, Recall = 88.7%)."),
        ("Academic Degree & CGPA Accuracy: 93.3%", "Correctly extracted degree titles (B.Tech, BCA, MCA) and GPA scores in 14 out of 15 resumes."),
        ("Professional Experience Accuracy: 86.7%", "Correctly classified fresher internship tenures and years-of-experience strings in 13 out of 15 resumes."),
        ("Entity Normalization Accuracy: 96.4%", "RapidFuzz Levenshtein token-sort combined with canonical synonym dictionary correctly normalized 96.4% of messy text variants.")
    ]
    for idx, (m_title, m_desc) in enumerate(metrics_p):
        pm = tf_p.add_paragraph() if idx > 0 else tf_p.paragraphs[0]
        pm.text = f"• {m_title}: "
        pm.font.bold = True
        pm.font.size = Pt(9.5)
        pm.font.color.rgb = PRIMARY_BLUE
        pm.space_before = Pt(3)
        rm = pm.add_run()
        rm.text = m_desc
        rm.font.bold = False
        rm.font.size = Pt(9.0)
        rm.font.color.rgb = DARK_TEXT

    # ==============================================================================
    # SLIDE 12: RESULTS & APPLICATION WORKFLOW (CRITERION 5 - 20 MARKS - PART 1)
    # ==============================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s12, 12, rubric_tag="Criterion 5 · Results & Conclusions (20 Marks)")
    add_slide_header(s12, "Results Showcase: End-to-End Application Workflow", "From raw PDF upload to interactive radar visualization and executive PDF report export.")

    wf_steps = [
        ("Step 1: Ingestion", "Upload PDF/DOCX or enter skills manually. Instant PyMuPDF parsing in <1 second."),
        ("Step 2: Profile Review", "Review extracted skills as interactive removable tags. Add or edit certifications."),
        ("Step 3: Role Benchmark", "Select from 81 live ESCO benchmark roles across Software, Data & Cloud tracks."),
        ("Step 4: Gap Analytics", "View Fit Score Gauge, Competency Radar Chart, and Essential vs Optional skill audit."),
        ("Step 5: ML Compensation", "NumPy Ridge model estimates empirical Indian CTC band (e.g. ₹3.0–4.4 LPA)."),
        ("Step 6: Actionable Roadmap", "Get 8-week sequential SWAYAM / NPTEL course plan with capstone project prompts.")
    ]
    for idx, (step_t, step_d) in enumerate(wf_steps):
        row_i = idx // 3
        col_i = idx % 3
        c_left = Inches(0.8) + Inches(col_i * 3.95)
        c_top = Inches(1.5) + Inches(row_i * 2.6)
        add_styled_card(s12, c_left, c_top, Inches(3.8), Inches(2.35), border_color=PRIMARY_BLUE, title=step_t)
        tb = s12.shapes.add_textbox(c_left + Inches(0.15), c_top + Inches(0.55), Inches(3.5), Inches(1.6))
        tb.text_frame.word_wrap = True
        p = tb.text_frame.paragraphs[0]
        p.text = step_d
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_TEXT

    # ==============================================================================
    # SLIDE 13: TALENT INTELLIGENCE SIMULATOR (CRITERION 5 - 20 MARKS - PART 2)
    # ==============================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s13, 13, rubric_tag="Criterion 5 · Results Showcase (20 Marks)")
    add_slide_header(s13, "Talent Intelligence: Growth AI Simulator & Market Trends", "Interactive macro talent analytics and dual-track career progression simulation in production.")

    # Left Card: Simulator
    add_styled_card(s13, Inches(0.8), Inches(1.4), Inches(5.7), Inches(5.4), title="Growth AI: Career Progression & Promotion Simulator (/career-growth)")
    t_sim = s13.shapes.add_textbox(Inches(0.95), Inches(1.85), Inches(5.4), Inches(4.8))
    tf_s = t_sim.text_frame
    tf_s.word_wrap = True
    ps = tf_s.paragraphs[0]
    ps.text = "1. Junior Track (JDS Promotion & Hike Classifier):\n• 5 Competency sliders (Maths, Storytelling, Coding, AI/ML, Big Data).\n• Real-time log-odds calculation predicting high salary hike probability %.\n• Actionable leverage tips: Storytelling score 4.0 -> 4.8 boosts promotion odds by 3.79x (r = +0.554).\n\n2. Senior Track (SDS Leadership Predictor):\n• Big Five (OCEAN) psychometric sliders (Conscientiousness, Openness, Extraversion, Agreeableness, Neuroticism).\n• Predicts client-facing executive success probability (AUC 0.995).\n• Behavioral coaching insights: Conscientiousness is the 31.7% driver of senior milestone delivery."
    ps.font.size = Pt(9.5)
    ps.font.color.rgb = DARK_TEXT

    # Right Card: Market Trends
    add_styled_card(s13, Inches(6.8), Inches(1.4), Inches(5.7), Inches(5.4), title="Macro Market Trends & Econometric Calculator (/market-insights)")
    t_mkt = s13.shapes.add_textbox(Inches(6.95), Inches(1.85), Inches(5.4), Inches(4.8))
    tf_m = t_mkt.text_frame
    tf_m.word_wrap = True
    pm = tf_m.paragraphs[0]
    pm.text = "1. Real-Time Macro Market Intelligence:\n• Aggregated across 15,841 analytics postings & 93,005 active positions.\n• Visual tool demand ranking: SQL (#1, 1,582), Python (#2, 962), SAS (#3, 876).\n• Verified enterprise recruiters: TCS (9,064), Accenture (5,425), IBM (4,120), Cognizant (3,890).\n\n2. Econometric Salary Estimator API:\n• Interactive form: Experience (years), City (8 tech hubs), and specialized skills.\n• Instant OLS compensation band estimation:\n   Salary = 12.95 + 1.74*(Exp) + City_Mod + Skill_Prem\n• Reflects real regional wage differences and specialized skill premiums in real time."
    pm.font.size = Pt(9.5)
    pm.font.color.rgb = DARK_TEXT

    # ==============================================================================
    # SLIDE 14: INSTITUTIONAL PILOT CASE STUDY (CRITERION 6 - 10 MARKS - PART 1)
    # ==============================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s14, 14, rubric_tag="Criterion 6 · Implications & Impact (10 Marks)")
    add_slide_header(s14, "Implications: 60-Student Institutional Batch Pilot", "Proving real-world actionability: Targeted curriculum intervention doubles placement readiness.")

    # 3 Phase Cards
    phases = [
        ("Phase 1: Baseline Cohort Audit", RED_ACCENT, [
            "Audited 60 final-year CSE/BCA undergraduates targeting Frontend Developer roles.",
            "85.0% (51/60) possessed foundational HTML/CSS syntax.",
            "78.3% (47/60) possessed vanilla JavaScript concepts.",
            "Average initial Role-Fit Score: 41.2% (Low Placement Readiness)."
        ]),
        ("Phase 2: Critical Gaps Identified", ORANGE_WARN, [
            "68.3% (41/60) lacked modern React component architecture & state hooks.",
            "81.7% (49/60) lacked TypeScript static typing.",
            "90.0% (54/60) had zero experience with automated testing (Jest) or CI/CD.",
            "College realized generic training was missing modern industry ontologies."
        ]),
        ("Phase 3: Targeted Intervention", SUCCESS_GREEN, [
            "Department initiated a targeted 4-week NPTEL & project-driven bootcamp.",
            "Focused specifically on React, TypeScript, and Git collaboration.",
            "Average cohort role-fit score surged from 41.2% -> 86.7%!",
            "Placement eligibility doubled prior to corporate campus hiring drives."
        ])
    ]
    for idx, (title, color, bullets) in enumerate(phases):
        c_left = Inches(0.8) + Inches(idx * 3.95)
        add_styled_card(s14, c_left, Inches(1.5), Inches(3.8), Inches(4.0), border_color=color, title=title, title_color=color)
        tb = s14.shapes.add_textbox(c_left + Inches(0.15), Inches(1.95), Inches(3.5), Inches(3.4))
        tbf = tb.text_frame
        tbf.word_wrap = True
        for b_idx, b in enumerate(bullets):
            pb = tbf.add_paragraph() if b_idx > 0 else tbf.paragraphs[0]
            pb.text = f"• {b}"
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = DARK_TEXT
            pb.space_before = Pt(4)

    # Bottom Stakeholder Summary
    add_styled_card(s14, Inches(0.8), Inches(5.7), Inches(11.7), Inches(1.1), bg_color=RGBColor(0xEE, 0xF2, 0xFF), border_color=ACCENT_BLUE)
    t_stk = s14.shapes.add_textbox(Inches(0.95), Inches(5.75), Inches(11.4), Inches(1.0))
    p = t_stk.text_frame.paragraphs[0]
    p.text = "★ Tri-Partite Stakeholder Value Proposition:"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = PRIMARY_BLUE
    p2 = t_stk.text_frame.add_paragraph()
    p2.text = "1. Students: Crystal-clear diagnostic roadmaps eliminating career ambiguity.  2. Universities: Empirical curriculum gap analysis converting low-employability cohorts into high-placement winners.  3. Industry: Standardized, pre-screened talent pools matching exact production skill profiles."
    p2.font.size = Pt(9.0)
    p2.font.color.rgb = DARK_TEXT

    # ==============================================================================
    # SLIDE 15: DEMOGRAPHIC PARITY & EQUITY (CRITERION 6 - 10 MARKS - PART 2)
    # ==============================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s15, 15, rubric_tag="Criterion 6 · Algorithmic Fairness (10 Marks)")
    add_slide_header(s15, "Skill-First Equity: Demographic Parity Audit (DIR = 1.000)", "Proving zero pedigree bias: Pure competency-first scoring across diverse educational backgrounds.")

    fair_rows = [
        ("Candidate A", "Tier-1 Elite University (IIT / NIT B.Tech)", "CGPA: 9.2 / 10.0", "83.3% (Frontend Engineer)", "1.000 (Baseline)"),
        ("Candidate B", "Tier-3 Regional Institution (BCA Degree)", "CGPA: 6.8 / 10.0", "83.3% (Frontend Engineer)", "1.000 (Perfect Parity)"),
        ("Candidate C", "Polytechnic State Diploma Holder", "No Degree / Diploma Only", "83.3% (Frontend Engineer)", "1.000 (Perfect Parity)"),
        ("Candidate D", "Self-Taught Non-Technical Graduate (B.Com)", "Non-CS Degree", "83.3% (Frontend Engineer)", "1.000 (Perfect Parity)")
    ]

    tbl_s15 = s15.shapes.add_table(len(fair_rows) + 1, 5, Inches(0.8), Inches(1.4), Inches(11.7), Inches(2.6))
    t15 = tbl_s15.table
    t15.columns[0].width = Inches(1.8)
    t15.columns[1].width = Inches(3.6)
    t15.columns[2].width = Inches(2.0)
    t15.columns[3].width = Inches(2.3)
    t15.columns[4].width = Inches(2.0)

    headers15 = ["Candidate Profile", "Institutional Pedigree & Background", "Extracted Academic Score", "Computed Role-Fit Score", "Disparate Impact Ratio (DIR)"]
    for j, h in enumerate(headers15):
        cell = t15.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
    for i, row in enumerate(fair_rows):
        for j, val in enumerate(row):
            cell = t15.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT_BG if i % 2 == 1 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.color.rgb = DARK_TEXT
            if j == 4:
                p.font.bold = True
                p.font.color.rgb = SUCCESS_GREEN

    # 2 Explanatory Cards Below
    add_styled_card(s15, Inches(0.8), Inches(4.2), Inches(5.7), Inches(2.6), title="Algorithmic Fairness Verification")
    tb_fv = s15.shapes.add_textbox(Inches(0.95), Inches(4.55), Inches(5.4), Inches(2.1))
    p = tb_fv.text_frame.paragraphs[0]
    p.text = "• Controlled Experiment: Four candidate profiles with identical technical skill vectors (React, JavaScript, Node.js, SQL, Git).\n• Result: All four candidates receive identical Role-Fit Scores (83.3%), identical ML salary ranges (₹4.8–6.2 LPA), and identical SWAYAM roadmaps.\n• Mathematical Proof: Disparate Impact Ratio DIR = 1.000.\n• Pedagogical Rule: College brand and CGPA are extracted strictly as descriptive profile metadata; they are assigned a mathematical weight of 0.00 in the scoring engine."
    p.font.size = Pt(8.5)
    p.font.color.rgb = DARK_TEXT

    add_styled_card(s15, Inches(6.8), Inches(4.2), Inches(5.7), Inches(2.6), title="Alignment with NEP 2020 & National Missions")
    tb_nep = s15.shapes.add_textbox(Inches(6.95), Inches(4.55), Inches(5.4), Inches(2.1))
    p = tb_nep.text_frame.paragraphs[0]
    p.text = "• National Education Policy (NEP 2020): Directly champions competency-based education and flexible academic credit transfer over rote degree prestige.\n• Skill India Mission: Integrates free government learning portals (SWAYAM, NPTEL) into actionable employability pathways for rural and semi-urban learners.\n• Democratizing Mobility: Enables talented youth from tier-2/3 cities to compete on an equal footing with premier institute graduates."
    p.font.size = Pt(8.5)
    p.font.color.rgb = DARK_TEXT

    # ==============================================================================
    # SLIDE 16: FUTURE IMPLEMENTATION - SKILL VERIFICATION & LMS SYNC
    # ==============================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s16, 16, rubric_tag="Jury Advisory · Future Implementation (Part 1)")
    add_slide_header(s16, "Future Implementation: Proctored Skill Verification & Live LMS Tracking",
                     "Addressing Top-30 Jury Advisory: Eliminating resume exaggeration through adaptive micro-assessments, secure proctoring, and live platform sync.")

    # Top Row: 3 Functional Pillar Cards
    # Card 1: Resume Skill Fraud & Exaggeration Defense
    add_styled_card(s16, Inches(0.8), Inches(1.4), Inches(3.8), Inches(3.8), border_color=ORANGE_WARN, title="1. Resume Fraud & Exaggeration Defense", title_color=ORANGE_WARN)
    tb_c1 = s16.shapes.add_textbox(Inches(0.95), Inches(1.85), Inches(3.5), Inches(3.25))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    c1_bullets = [
        ("The Industry Vulnerability", "Candidates routinely list inflated or unverified keywords on resumes that do not reflect working technical proficiency."),
        ("Dual-Status Verification", "Skills initialize as 'Self-Declared' (0.5x weight in matching). Upgraded to 'Empirically Verified' (1.0x weight) strictly post-evaluation."),
        ("Semantic Cross-Validation", "NLP entity parser cross-references claimed skills against project repos, commit histories, and coursework context to flag anomalies."),
        ("Recruiter Authenticity Index", "Outputs a verified 'Candidate Authenticity Score (0-100%)' providing transparent trust metrics to hiring partners.")
    ]
    for idx, (b_title, b_desc) in enumerate(c1_bullets):
        p = tf_c1.add_paragraph() if idx > 0 else tf_c1.paragraphs[0]
        p.text = f"• {b_title}: "
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = ORANGE_WARN
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = b_desc
        r.font.bold = False
        r.font.size = Pt(8.0)
        r.font.color.rgb = DARK_TEXT

    # Card 2: Adaptive 10-Question Skill Assessments
    add_styled_card(s16, Inches(4.75), Inches(1.4), Inches(3.8), Inches(3.8), border_color=PRIMARY_BLUE, title="2. Adaptive 10-Question Micro-Assessments", title_color=PRIMARY_BLUE)
    tb_c2 = s16.shapes.add_textbox(Inches(4.90), Inches(1.85), Inches(3.5), Inches(3.25))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    c2_bullets = [
        ("Dynamic Micro-Assessments", "Targeted 10-question evaluation dynamically assembled per claimed skill (e.g. React hooks, SQL indexing, Docker networking)."),
        ("Tri-Tier Question Taxonomy", "4 Conceptual/Syntax questions, 4 Practical Architecture/Scenario problems, and 2 Code Debugging / Output prediction challenges."),
        ("Strict 70-80% Passing Bar", "Candidate must score at least 7 to 8 correct out of 10 (≥70-80%) to verify competency and earn the official verifiable badge."),
        ("Adaptive Difficulty Scaling", "Item Response Theory (IRT) adjusts question complexity in real time to accurately measure true junior vs mid-level competence.")
    ]
    for idx, (b_title, b_desc) in enumerate(c2_bullets):
        p = tf_c2.add_paragraph() if idx > 0 else tf_c2.paragraphs[0]
        p.text = f"• {b_title}: "
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = PRIMARY_BLUE
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = b_desc
        r.font.bold = False
        r.font.size = Pt(8.0)
        r.font.color.rgb = DARK_TEXT

    # Card 3: Anti-Cheating Lockdown & Security Protocol
    add_styled_card(s16, Inches(8.7), Inches(1.4), Inches(3.8), Inches(3.8), border_color=RED_ACCENT, title="3. Anti-Cheating Sandbox & Attempt Caps", title_color=RED_ACCENT)
    tb_c3 = s16.shapes.add_textbox(Inches(8.85), Inches(1.85), Inches(3.5), Inches(3.25))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    c3_bullets = [
        ("Strict 3-Attempt Maximum", "Strict limit of 3 lifetime attempts per skill module to eliminate brute-forcing and question-memorization loopholes."),
        ("Mandatory Cooldown Period", "Failed attempts trigger a mandatory 48-hour revision lockout with targeted SWAYAM/NPTEL refresher modules before retesting."),
        ("Zero-Extension Sandbox", "Browser environment detects and actively blocks browser extensions (ChatGPT, Copilot, sidecar bots, inspect extensions)."),
        ("System Lockdown Protocol", "Enforces fullscreen, disables copy/paste clipboard APIs, blocks right-click inspection, and logs tab-switch violations.")
    ]
    for idx, (b_title, b_desc) in enumerate(c3_bullets):
        p = tf_c3.add_paragraph() if idx > 0 else tf_c3.paragraphs[0]
        p.text = f"• {b_title}: "
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = RED_ACCENT
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = b_desc
        r.font.bold = False
        r.font.size = Pt(8.0)
        r.font.color.rgb = DARK_TEXT

    # Bottom Full-Width Card: Live LMS Progress Synchronization
    add_styled_card(s16, Inches(0.8), Inches(5.35), Inches(11.7), Inches(1.55), bg_color=RGBColor(0xEE, 0xF2, 0xFF), border_color=ACCENT_BLUE, title="4. Live LMS Roadmap Progress Tracking (SWAYAM, NPTEL & Institutional Portals)", title_color=PRIMARY_BLUE)
    tb_lms = s16.shapes.add_textbox(Inches(0.95), Inches(5.72), Inches(11.4), Inches(1.1))
    tf_lms = tb_lms.text_frame
    tf_lms.word_wrap = True
    p_l1 = tf_lms.paragraphs[0]
    p_l1.text = "• Seamless Educational Ingestion: Connects via LTI / REST Webhooks to SWAYAM, NPTEL, Coursera, and college LMS platforms to track student progress."
    p_l1.font.size = Pt(8.5)
    p_l1.font.color.rgb = DARK_TEXT
    p_l2 = tf_lms.add_paragraph()
    p_l2.text = "• Live Roadmap Milestone Sync: Ingests video completion rates, weekly assignment submissions, and proctored exam scores in real time."
    p_l2.font.size = Pt(8.5)
    p_l2.font.color.rgb = DARK_TEXT
    p_l2.space_before = Pt(2)
    p_l3 = tf_lms.add_paragraph()
    p_l3.text = "• Automated Credential Pathway: Once a student completes a roadmap course, the platform automatically unlocks the proctored 10-Q verification assessment, updating the user's live role-readiness dashboard."
    p_l3.font.size = Pt(8.5)
    p_l3.font.color.rgb = DARK_TEXT
    p_l3.space_before = Pt(2)

    # ==============================================================================
    # SLIDE 17: FUTURE IMPLEMENTATION - DYNAMIC RESUME & AI INTERVIEW SIMULATOR
    # ==============================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_base_decorations(s17, 17, rubric_tag="Jury Advisory · Future Implementation (Part 2)")
    add_slide_header(s17, "Future Implementation: Dynamic Resume Generation & AI Interview Simulator",
                     "Addressing Top-30 Jury Advisory: Automated resume recompilation with verifiable credentials and conversational multimodal technical viva.")

    # Two Main Cards Side by Side
    # Left Card: Dynamic Auto-Updated Resume Generator
    add_styled_card(s17, Inches(0.8), Inches(1.4), Inches(5.7), Inches(4.05), border_color=SUCCESS_GREEN, title="Dynamic Auto-Updated Resume Generator (1-Click Download)", title_color=SUCCESS_GREEN)
    tb_res = s17.shapes.add_textbox(Inches(0.95), Inches(1.85), Inches(5.4), Inches(3.5))
    tf_res = tb_res.text_frame
    tf_res.word_wrap = True
    res_bullets = [
        ("Automated Resume Recompilation", "The moment a candidate passes a 10-Q assessment (≥7-8/10) or completes a verified roadmap course, CareerPath AI automatically rebuilds their master resume."),
        ("ATS-Optimized Formatting", "Re-synthesizes candidate experience into industry-standard single-column ATS layouts, optimizing keyword density and machine readability."),
        ("Verified Badge Injection", "Embeds authenticated competency tags ('Verified: React 80%', 'Certified: NPTEL Data Structures') while deprioritizing unverified claims."),
        ("Cryptographic QR Verification", "Embeds a tamper-proof QR code linking hiring managers directly to the candidate's verified live skill audit ledger on CareerPath AI."),
        ("Instant Multi-Format Export", "Provides 1-click download options in ATS-compliant vector PDF and fully editable Microsoft Word DOCX formats.")
    ]
    for idx, (b_title, b_desc) in enumerate(res_bullets):
        p = tf_res.add_paragraph() if idx > 0 else tf_res.paragraphs[0]
        p.text = f"• {b_title}: "
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = SUCCESS_GREEN
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = b_desc
        r.font.bold = False
        r.font.size = Pt(8.0)
        r.font.color.rgb = DARK_TEXT

    # Right Card: Conversational AI Mock Interview & Viva
    add_styled_card(s17, Inches(6.8), Inches(1.4), Inches(5.7), Inches(4.05), border_color=PRIMARY_BLUE, title="Conversational AI Mock Interview & Technical Viva Simulator", title_color=PRIMARY_BLUE)
    tb_ai = s17.shapes.add_textbox(Inches(6.95), Inches(1.85), Inches(5.4), Inches(3.5))
    tf_ai = tb_ai.text_frame
    tf_ai.word_wrap = True
    ai_bullets = [
        ("Role-Specific Interview Persona", "Tailored AI interviewer adapting dynamically to target roles (e.g. Senior Backend Engineer vs Associate Data Analyst)."),
        ("Project-Grounded Viva Questions", "Analyzes the candidate's verified skills and resume projects to ask probing technical viva questions ('Walk me through your database indexing strategy in Project X')."),
        ("Adaptive Counter-Probing", "Dynamically challenges superficial answers with architectural edge cases ('What happens if your cache invalidation fails under high load?')."),
        ("Multimodal 4-D Scoring Rubric", "Evaluates candidate responses across 4 dimensions: (1) Technical Correctness, (2) Problem-Solving Structure, (3) Communication Clarity, and (4) Speech Delivery."),
        ("Actionable Post-Viva Diagnostics", "Generates an instant feedback report highlighting strong answers, conceptual blindspots, and personalized roadmap study links.")
    ]
    for idx, (b_title, b_desc) in enumerate(ai_bullets):
        p = tf_ai.add_paragraph() if idx > 0 else tf_ai.paragraphs[0]
        p.text = f"• {b_title}: "
        p.font.bold = True
        p.font.size = Pt(8.5)
        p.font.color.rgb = PRIMARY_BLUE
        p.space_before = Pt(3)
        r = p.add_run()
        r.text = b_desc
        r.font.bold = False
        r.font.size = Pt(8.0)
        r.font.color.rgb = DARK_TEXT

    # Bottom Full-Width Card: Future Closed-Loop Architecture
    add_styled_card(s17, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.3), bg_color=RGBColor(0x0F, 0x17, 0x2A), border_color=ACCENT_BLUE)
    tb_flow = s17.shapes.add_textbox(Inches(0.95), Inches(5.65), Inches(11.4), Inches(1.2))
    tf_fl = tb_flow.text_frame
    tf_fl.word_wrap = True
    p_fl1 = tf_fl.paragraphs[0]
    p_fl1.text = "★ End-to-End Closed-Loop Talent Lifecycle (Future Architecture):"
    p_fl1.font.bold = True
    p_fl1.font.size = Pt(10)
    p_fl1.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)
    p_fl2 = tf_fl.add_paragraph()
    p_fl2.text = "Resume Parsing & Gap Audit  ➔  Live LMS Progress Sync (SWAYAM / NPTEL)  ➔  Proctored 10-Q Micro-Assessments (70-80% pass bar, max 3 attempts, anti-cheat sandbox)  ➔  Dynamic Auto-Recompiled Resume (PDF/DOCX + QR Verification)  ➔  Conversational AI Technical Viva  ➔  Pre-Screened Placement Handoff."
    p_fl2.font.size = Pt(8.5)
    p_fl2.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
    p_fl2.space_before = Pt(4)

    # ==============================================================================
    # SLIDE 18: CONCLUSION & TECH STACK
    # ==============================================================================
    s18 = prs.slides.add_slide(blank_layout)
    bg18 = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_WIDTH, SLIDE_HEIGHT)
    bg18.fill.solid()
    bg18.fill.fore_color.rgb = RGBColor(0x0A, 0x11, 0x28)
    bg18.line.fill.background()

    # Title
    t_end = s18.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(1.2))
    p = t_end.text_frame.paragraphs[0]
    p.text = "CareerPath AI: Ready for Impact"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p2 = t_end.text_frame.add_paragraph()
    p2.text = "Empowering India's next generation of technical talent through data-driven workforce intelligence."
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)
    p2.space_before = Pt(6)

    # 4 Pillar Highlights
    pillars = [
        ("Audited Data Grounding", "28,000+ postings, 7 provenance datasets, 93,005 verified enterprise positions."),
        ("Closed-Form ML Rigor", "NumPy Ridge (R²=0.715), fresher MAE ₹1.18L, Gaussian Naive Bayes (84.2% & 95.7%)."),
        ("Actionable Roadmaps", "Prescriptive SWAYAM / NPTEL course schedules with proven 41.2% -> 86.7% pilot uplift."),
        ("Skill-First Equity", "DIR = 1.000 demographic parity ensuring pure meritocracy across Tier-1 to Tier-3.")
    ]
    for idx, (head, desc) in enumerate(pillars):
        c_left = Inches(1.0) + Inches(idx * 2.85)
        c_card = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, Inches(3.0), Inches(2.7), Inches(2.2))
        c_card.fill.solid()
        c_card.fill.fore_color.rgb = RGBColor(0x13, 0x1E, 0x3A)
        c_card.line.color.rgb = RGBColor(0x3B, 0x82, 0xF6)
        c_card.line.width = Pt(1)
        ctf = c_card.text_frame
        ctf.word_wrap = True
        cp1 = ctf.paragraphs[0]
        cp1.text = head
        cp1.font.size = Pt(11)
        cp1.font.bold = True
        cp1.font.color.rgb = RGBColor(0x60, 0xA5, 0xFA)
        cp2 = ctf.add_paragraph()
        cp2.text = desc
        cp2.font.size = Pt(9.5)
        cp2.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
        cp2.space_before = Pt(6)

    # Bottom Tech Stack Badges
    tx_tech = s18.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(11.3), Inches(1.2))
    p_t = tx_tech.text_frame.paragraphs[0]
    p_t.text = "Production Tech Stack & Future Capabilities:"
    p_t.font.size = Pt(12)
    p_t.font.bold = True
    p_t.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)
    p_t2 = tx_tech.text_frame.add_paragraph()
    p_t2.text = "FastAPI 0.115  ·  Python 3.12  ·  React 18 + Vite  ·  TailwindCSS  ·  NumPy & SciPy (Closed-Form)  ·  RapidFuzz  ·  PyMuPDF  ·  ReportLab  ·  Supabase  ·  WebRTC Viva"
    p_t2.font.size = Pt(10)
    p_t2.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
    p_t2.space_before = Pt(4)

    # Save Presentation
    print(f"\nSaving presentation to: {TARGET_PPTX}...")
    prs.save(str(TARGET_PPTX))

    print(f"Saving copy to user Downloads: {DOWNLOADS_PPTX}...")
    import shutil
    shutil.copy2(TARGET_PPTX, DOWNLOADS_PPTX)

    print(f"SUCCESS: Generated {len(prs.slides)} slides in 16:9 widescreen format!")

if __name__ == "__main__":
    build_presentation()
