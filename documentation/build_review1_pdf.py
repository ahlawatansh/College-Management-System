import os
import sys

# Ensure matplotlib uses a writable temp cache directory
os.environ["MPLCONFIGDIR"] = "/tmp/mpl_config"
os.makedirs("/tmp/mpl_config", exist_ok=True)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_OUTPUT_PATH = os.path.join(BASE_DIR, "documentation", "REVIEW_1_REPORT.pdf")
ER_IMG_PATH = os.path.join(BASE_DIR, "diagrams", "er_diagram.jpg")

print(f"Generating PDF Report at: {PDF_OUTPUT_PATH}")

with PdfPages(PDF_OUTPUT_PATH) as pdf:
    # -------------------------------------------------------------------------
    # PAGE 1: COVER PAGE
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(8.5, 11), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Background header banner
    ax.fill_between([0, 1], [0.82, 0.82], [1, 1], color='#0d1b2a')
    ax.fill_between([0, 1], [0.80, 0.80], [0.82, 0.82], color='#00a896')

    # University & Department text
    ax.text(0.5, 0.94, "VELLORE INSTITUTE OF TECHNOLOGY", color='white', fontsize=16, weight='bold', ha='center', va='center')
    ax.text(0.5, 0.90, "School of Computer Science and Engineering", color='#e0e1dd', fontsize=12, ha='center', va='center')
    ax.text(0.5, 0.86, "BCSE302L – DATABASE SYSTEMS (LAB COURSE PROJECT)", color='#02c39a', fontsize=11, weight='bold', ha='center', va='center')

    # Project Title
    ax.text(0.5, 0.72, "COLLEGE MANAGEMENT SYSTEM", color='#0d1b2a', fontsize=22, weight='bold', ha='center', va='center')
    ax.text(0.5, 0.68, "A Normalized, High-Integrity Relational Database System", color='#415a77', fontsize=13, style='italic', ha='center', va='center')
    ax.text(0.5, 0.65, "REVIEW I REPORT: Problem Definition, ER Modeling & Relational Schema", color='#1b263b', fontsize=11, weight='bold', ha='center', va='center')

    # Divider
    ax.plot([0.15, 0.85], [0.62, 0.62], color='#778da9', lw=1.5)

    # Faculty In-Charge Box
    ax.text(0.5, 0.56, "FACULTY IN-CHARGE:", color='#0d1b2a', fontsize=11, weight='bold', ha='center')
    ax.text(0.5, 0.525, "Course Instructor", color='#1b4965', fontsize=14, weight='bold', ha='center')
    ax.text(0.5, 0.495, "School of Computer Science and Engineering", color='#555555', fontsize=10, ha='center')

    # Project Team Box
    ax.text(0.5, 0.43, "STUDENT DEVELOPMENT TEAM", color='#0d1b2a', fontsize=12, weight='bold', ha='center')
    team_data = [
        ("ANSH", "REG_01", "B.Tech Data Engineering", "Lead Architect & Schema Specialist"),
        ("Student 2", "REG_02", "B.Tech Computer Science", "PL/SQL Backend & Stored Logic Developer"),
        ("Student 3", "REG_03", "B.Tech Data Engineering", "Analytical Queries & Transaction Automation")
    ]
    y_pos = 0.38
    for name, reg, deg, role in team_data:
        ax.text(0.20, y_pos, f"• {name}", fontsize=11, weight='bold', color='#0d1b2a')
        ax.text(0.48, y_pos, f"Reg No: {reg}", fontsize=10, weight='bold', color='#1b4965')
        ax.text(0.23, y_pos - 0.025, f"{deg} | Role: {role}", fontsize=9, color='#666666')
        y_pos -= 0.06

    # Footer note
    ax.fill_between([0, 1], [0, 0], [0.08, 0.08], color='#0d1b2a')
    ax.text(0.5, 0.04, "ACADEMIC YEAR 2025–2026 | VIT CHENNAI / VELLORE", color='white', fontsize=10, weight='bold', ha='center', va='center')

    pdf.savefig(fig)
    plt.close()

    # -------------------------------------------------------------------------
    # PAGE 2: PROBLEM STATEMENT & SCOPE
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(8.5, 11), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Top Header
    ax.fill_between([0, 1], [0.93, 0.93], [1, 1], color='#1b263b')
    ax.text(0.08, 0.96, "1. PROBLEM DEFINITION & SCOPE", color='white', fontsize=14, weight='bold', va='center')
    ax.text(0.92, 0.96, "BCSE302L - REVIEW I", color='#02c39a', fontsize=11, weight='bold', ha='right', va='center')

    y = 0.88
    ax.text(0.08, y, "1.1 Problem Statement & Background", fontsize=12, weight='bold', color='#0d1b2a')
    y -= 0.03
    p1 = (
        "Higher educational institutions coordinate hundreds of simultaneous academic operations encompassing\n"
        "student admissions, curriculum maintenance, course section allocations, continuous grade evaluations, and\n"
        "fee reconciliations. Legacy or unstructured spreadsheet-driven records suffer from data duplication, lack of\n"
        "referential integrity, inconsistent grading schemes, and phantom course enrollments exceeding class limits."
    )
    ax.text(0.08, y, p1, fontsize=9.5, color='#333333', va='top', linespacing=1.3)

    y -= 0.11
    ax.text(0.08, y, "1.2 Project Objectives", fontsize=12, weight='bold', color='#0d1b2a')
    y -= 0.03
    p2 = (
        "1. Normalized Relational Design: Implement an 8-table relational architecture adhering strictly to BCNF/3NF.\n"
        "2. Strict Declarative Integrity: Enforce Primary Keys, Foreign Keys, NOT NULL, UNIQUE, and CHECK constraints.\n"
        "3. Automated Business Logic: Implement PL/SQL procedures, functions, reactive triggers, and explicit cursors.\n"
        "4. Real-World Demonstrability: Support 5 major real-world transactions spanning enrollment, fees, and grading."
    )
    ax.text(0.08, y, p2, fontsize=9.5, color='#333333', va='top', linespacing=1.3)

    y -= 0.11
    ax.text(0.08, y, "1.3 Functional Stakeholder Roles", fontsize=12, weight='bold', color='#0d1b2a')
    y -= 0.035

    roles = [
        ("Students", "Browse catalog courses, enroll in active sections, inspect grade transcripts, and pay tuition fees."),
        ("Faculty", "Access enrolled student rosters, monitor section quotas, and enter/update official exam evaluations."),
        ("Deans & HODs", "Oversee departmental curricula, monitor faculty payroll expenditures, and audit academic metrics."),
        ("Finance Office", "Process tuition receipts across UPI/Cards/Net Banking and identify outstanding fee defaulters.")
    ]
    for r_title, r_desc in roles:
        ax.text(0.10, y, f"• {r_title}:", fontsize=10, weight='bold', color='#1b4965')
        ax.text(0.24, y, r_desc, fontsize=9.5, color='#444444')
        y -= 0.035

    y -= 0.02
    ax.text(0.08, y, "1.4 System Architecture Flow", fontsize=12, weight='bold', color='#0d1b2a')
    y -= 0.04
    ax.text(0.5, y, "[User Action]  →  [Application Layer]  →  [SQL / PL/SQL Logic]  →  [Relational Engine]  →  [ACID Result]",
            fontsize=10, weight='bold', color='#0077b6', ha='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#e0f2fe", edgecolor="#0077b6", lw=1.2))

    pdf.savefig(fig)
    plt.close()

    # -------------------------------------------------------------------------
    # PAGE 3: 8 ENTITIES & RELATIONAL SCHEMA
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(8.5, 11), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    ax.fill_between([0, 1], [0.93, 0.93], [1, 1], color='#1b263b')
    ax.text(0.08, 0.96, "2. 8-TABLE RELATIONAL SCHEMA & CONSTRAINTS", color='white', fontsize=14, weight='bold', va='center')
    ax.text(0.92, 0.96, "BCSE302L - REVIEW I", color='#02c39a', fontsize=11, weight='bold', ha='right', va='center')

    tables_info = [
        ("1. DEPARTMENT", "dept_id (PK), dept_name (UQ, NN), dept_code (UQ, NN), building (NN), budget (CHECK > 0), established_year (CHECK 1950..2026)"),
        ("2. FACULTY", "faculty_id (PK), first_name (NN), last_name (NN), email (UQ, NN), phone (UQ, NN), hire_date (NN), designation (CHECK), salary (CHECK >= 25k), dept_id (FK -> DEPARTMENT)"),
        ("3. STUDENT", "student_id (PK), reg_no (UQ, NN), first_name (NN), last_name (NN), email (UQ, NN), phone (UQ, NN), dob (NN), gender (CHECK), dept_id (FK -> DEPARTMENT), current_semester (CHECK 1..8), status (CHECK)"),
        ("4. COURSE", "course_id (PK), course_code (UQ, NN), course_title (NN), credits (CHECK 1..6), dept_id (FK -> DEPARTMENT), course_level (CHECK)"),
        ("5. COURSE_OFFERING", "offering_id (PK), course_id (FK -> COURSE), faculty_id (FK -> FACULTY), academic_year (NN), semester (CHECK 1..8), classroom (NN), max_capacity (CHECK >= 10), current_enrolled (CHECK), UNIQUE(course, faculty, year, sem)"),
        ("6. ENROLLMENT", "enrollment_id (PK), student_id (FK -> STUDENT), offering_id (FK -> COURSE_OFFERING), enrollment_date (DEFAULT), status (CHECK 'Enrolled','Completed','Dropped'), UNIQUE(student_id, offering_id)"),
        ("7. EXAM_RESULT", "result_id (PK), enrollment_id (FK -> ENROLLMENT, UQ), marks_obtained (CHECK 0..100), grade (CHECK 'S'..'F'), exam_date (DEFAULT), remarks (DEFAULT)"),
        ("8. FEE_PAYMENT", "payment_id (PK), student_id (FK -> STUDENT), amount_paid (CHECK > 0), payment_date (DEFAULT), payment_method (CHECK), transaction_ref (UQ, NN), payment_status (CHECK)")
    ]

    y = 0.88
    for t_name, t_schema in tables_info:
        ax.text(0.08, y, t_name, fontsize=10.5, weight='bold', color='#0077b6')
        ax.text(0.08, y - 0.025, t_schema, fontsize=8.5, color='#222222', style='italic')
        ax.plot([0.08, 0.92], [y - 0.045, y - 0.045], color='#e2e8f0', lw=0.8)
        y -= 0.075

    y -= 0.01
    ax.text(0.08, y, "Normalization Analysis Summary", fontsize=11, weight='bold', color='#0d1b2a')
    y -= 0.03
    norm_text = (
        "• 1NF: Every attribute is atomic; no repeating groups or multi-valued fields.\n"
        "• 2NF: All tables have single-attribute surrogate keys; zero partial dependencies.\n"
        "• 3NF & BCNF: All non-key attributes depend solely on candidate keys. No transitive functional dependencies."
    )
    ax.text(0.08, y, norm_text, fontsize=9, color='#333333', va='top', linespacing=1.3)

    pdf.savefig(fig)
    plt.close()

    # -------------------------------------------------------------------------
    # PAGE 4: ER DIAGRAM SHOWCASE
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(8.5, 11), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    ax.fill_between([0, 1], [0.93, 0.93], [1, 1], color='#1b263b')
    ax.text(0.08, 0.96, "3. ENTITY-RELATIONSHIP (ER) DIAGRAM", color='white', fontsize=14, weight='bold', va='center')
    ax.text(0.92, 0.96, "BCSE302L - REVIEW I", color='#02c39a', fontsize=11, weight='bold', ha='right', va='center')

    # Embed generated image
    if os.path.exists(ER_IMG_PATH):
        img = mpimg.imread(ER_IMG_PATH)
        ax.imshow(img, extent=[0.08, 0.92, 0.45, 0.88], aspect='auto')

    y = 0.40
    ax.text(0.08, y, "Cardinalities & Relationship Summary:", fontsize=11, weight='bold', color='#0d1b2a')
    y -= 0.03
    cards = [
        "1. DEPARTMENT (1) to (N) STUDENT & FACULTY: Home department governance.",
        "2. DEPARTMENT (1) to (N) COURSE: Curricular catalog ownership.",
        "3. FACULTY (1) to (N) COURSE_OFFERING: Teaching section instruction.",
        "4. COURSE (1) to (N) COURSE_OFFERING: Curriculum term offerings.",
        "5. STUDENT (M) to (N) COURSE_OFFERING: Resolved via ENROLLMENT with UNIQUE(student, offering).",
        "6. ENROLLMENT (1) to (1) EXAM_RESULT: Official semester examination transcript.",
        "7. STUDENT (1) to (N) FEE_PAYMENT: Institutional tuition transaction receipts."
    ]
    for c in cards:
        ax.text(0.08, y, c, fontsize=9, color='#333333')
        y -= 0.035

    pdf.savefig(fig)
    plt.close()

    # -------------------------------------------------------------------------
    # PAGE 5: REVIEW I VIVA PREPARATION & SIGN-OFF
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(8.5, 11), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    ax.fill_between([0, 1], [0.93, 0.93], [1, 1], color='#1b263b')
    ax.text(0.08, 0.96, "4. VIVA DEFENSE & FACULTY SIGN-OFF", color='white', fontsize=14, weight='bold', va='center')
    ax.text(0.92, 0.96, "BCSE302L - REVIEW I", color='#02c39a', fontsize=11, weight='bold', ha='right', va='center')

    y = 0.88
    viva_qa = [
        ("Q: Why separate COURSE from COURSE_OFFERING?",
         "A: A catalog course represents an invariant syllabus item. A course offering represents a specific term section (venue, time, instructor, capacity). Separating them avoids repeating course titles and credits, preserving 3NF."),
        ("Q: How do you enforce class size limits?",
         "A: Via COURSE_OFFERING(max_capacity, current_enrolled) with CHECK constraints, plus PL/SQL procedure Enroll_Student_Proc that aborts registration when current_enrolled >= max_capacity."),
        ("Q: Why is EXAM_RESULT mapped 1:1 to ENROLLMENT?",
         "A: A student must be officially registered to take an exam. Mapping to ENROLLMENT with a UNIQUE constraint guarantees referential integrity without duplicating student and offering keys.")
    ]

    for q, a in viva_qa:
        ax.text(0.08, y, q, fontsize=10, weight='bold', color='#1b4965')
        ax.text(0.08, y - 0.025, a, fontsize=9, color='#333333', linespacing=1.2)
        y -= 0.09

    y -= 0.05
    ax.text(0.08, y, "FACULTY EVALUATION RUBRIC (REVIEW I)", fontsize=11, weight='bold', color='#0d1b2a')
    y -= 0.04
    ax.text(0.08, y, "• Problem Definition & Institutional Scope (20%):  [   / 20 ]", fontsize=9.5, color='#444444')
    y -= 0.03
    ax.text(0.08, y, "• Entity-Relationship Diagram & Cardinalities (30%): [   / 30 ]", fontsize=9.5, color='#444444')
    y -= 0.03
    ax.text(0.08, y, "• Relational Schema & BCNF Normalization (30%):       [   / 30 ]", fontsize=9.5, color='#444444')
    y -= 0.03
    ax.text(0.08, y, "• Viva Defense & Technical Justification (20%):     [   / 20 ]", fontsize=9.5, color='#444444')

    y -= 0.08
    ax.plot([0.08, 0.40], [y, y], color='#333333', lw=1)
    ax.plot([0.60, 0.92], [y, y], color='#333333', lw=1)
    ax.text(0.24, y - 0.025, "Student Team Signature", fontsize=9, ha='center', color='#555555')
    ax.text(0.76, y - 0.025, "Faculty Signature (Course Instructor)", fontsize=9, ha='center', color='#555555')

    pdf.savefig(fig)
    plt.close()

print("Review 1 PDF Generated Successfully!")
