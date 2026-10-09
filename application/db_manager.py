"""
Database manager for College Management System.
Handles SQLite connection, table creation, queries, and transactions.
"""

import os
import sqlite3
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "college_cms.db")
SQL_DDL_PATH = os.path.join(BASE_DIR, "database", "01_create_tables.sql")
SQL_DML_PATH = os.path.join(BASE_DIR, "database", "02_insert_data.sql")
SQL_QUERIES_PATH = os.path.join(BASE_DIR, "database", "03_queries.sql")


def get_connection():
    """Returns a SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database(force_recreate=False):
    """Initializes tables and default data if not already present."""
    if force_recreate and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='STUDENT';")
    exists = cursor.fetchone()[0]

    if exists == 0 or force_recreate:
        with open(SQL_DDL_PATH, "r", encoding="utf-8") as f:
            ddl_script = f.read()
        cursor.executescript(ddl_script)

        with open(SQL_DML_PATH, "r", encoding="utf-8") as f:
            dml_script = f.read()
        cursor.executescript(dml_script)
        conn.commit()

    conn.close()
    return True


# 1. Read operations
def get_all_students():
    """Retrieves all students with department name."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT 
        s.student_id, s.reg_no, s.first_name || ' ' || s.last_name AS full_name,
        s.email, s.phone, s.date_of_birth, s.gender, s.current_semester, s.status,
        d.dept_code, d.dept_name
    FROM STUDENT s
    JOIN DEPARTMENT d ON s.dept_id = d.dept_id
    ORDER BY s.student_id ASC;
    """
    cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_all_departments():
    """Retrieves all academic departments."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DEPARTMENT ORDER BY dept_id ASC;")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_all_faculty():
    """Retrieves faculty list with department details."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT f.faculty_id, f.first_name || ' ' || f.last_name AS faculty_name,
           f.designation, f.email, f.phone, f.salary, d.dept_code
    FROM FACULTY f
    JOIN DEPARTMENT d ON f.dept_id = d.dept_id
    ORDER BY f.faculty_id ASC;
    """
    cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_all_course_offerings():
    """Retrieves course offerings with course and instructor names."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT co.offering_id, c.course_code, c.course_title, c.credits,
           f.first_name || ' ' || f.last_name AS instructor,
           co.academic_year, co.semester, co.classroom,
           co.current_enrolled, co.max_capacity,
           (co.max_capacity - co.current_enrolled) AS available_seats
    FROM COURSE_OFFERING co
    JOIN COURSE c ON co.course_id = c.course_id
    JOIN FACULTY f ON co.faculty_id = f.faculty_id
    ORDER BY co.offering_id ASC;
    """
    cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_enrollments(student_id=None):
    """Retrieves enrollment records, optionally filtered by student_id."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT e.enrollment_id, s.reg_no, s.first_name || ' ' || s.last_name AS student_name,
           c.course_code, c.course_title, f.first_name || ' ' || f.last_name AS instructor,
           e.enrollment_date, e.status AS enrollment_status,
           er.marks_obtained, er.grade
    FROM ENROLLMENT e
    JOIN STUDENT s ON e.student_id = s.student_id
    JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
    JOIN COURSE c ON co.course_id = c.course_id
    JOIN FACULTY f ON co.faculty_id = f.faculty_id
    LEFT JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id
    """
    if student_id:
        query += " WHERE e.student_id = ? ORDER BY e.enrollment_id ASC;"
        cursor.execute(query, (student_id,))
    else:
        query += " ORDER BY e.enrollment_id ASC;"
        cursor.execute(query)

    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_fee_payments(student_id=None):
    """Retrieves fee payment history."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT fp.payment_id, s.reg_no, s.first_name || ' ' || s.last_name AS student_name,
           fp.amount_paid, fp.payment_date, fp.payment_method,
           fp.transaction_ref, fp.payment_status
    FROM FEE_PAYMENT fp
    JOIN STUDENT s ON fp.student_id = s.student_id
    """
    if student_id:
        query += " WHERE fp.student_id = ? ORDER BY fp.payment_date DESC;"
        cursor.execute(query, (student_id,))
    else:
        query += " ORDER BY fp.payment_date DESC;"
        cursor.execute(query)

    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_all_courses():
    """Retrieves all curriculum courses with department info."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT c.course_id, c.course_code, c.course_title, c.credits, c.course_level,
           d.dept_code, d.dept_name
    FROM COURSE c
    JOIN DEPARTMENT d ON c.dept_id = d.dept_id
    ORDER BY c.course_id ASC;
    """
    cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_all_exam_results():
    """Retrieves all examination grades with student and course details."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT er.result_id, er.enrollment_id, s.reg_no, s.first_name || ' ' || s.last_name AS student_name,
           c.course_code, c.course_title, er.marks_obtained, er.grade, er.exam_date, er.remarks
    FROM EXAM_RESULT er
    JOIN ENROLLMENT e ON er.enrollment_id = e.enrollment_id
    JOIN STUDENT s ON e.student_id = s.student_id
    JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
    JOIN COURSE c ON co.course_id = c.course_id
    ORDER BY er.result_id ASC;
    """
    cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def add_faculty(first_name, last_name, email, phone, hire_date, designation, salary, dept_id):
    """Appoints a new faculty member."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MAX(faculty_id) FROM FACULTY;")
        max_id = cursor.fetchone()[0] or 100
        new_id = max_id + 1
        cursor.execute("""
            INSERT INTO FACULTY (faculty_id, first_name, last_name, email, phone, hire_date, designation, salary, dept_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (new_id, first_name, last_name, email, phone, hire_date, designation, salary, dept_id))
        conn.commit()
        return True, f"SUCCESS: Faculty member '{first_name} {last_name}' appointed with ID {new_id}."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


def add_course(course_code, course_title, credits, dept_id, course_level):
    """Registers a new curriculum course."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MAX(course_id) FROM COURSE;")
        max_id = cursor.fetchone()[0] or 300
        new_id = max_id + 1
        cursor.execute("""
            INSERT INTO COURSE (course_id, course_code, course_title, credits, dept_id, course_level)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (new_id, course_code, course_title, credits, dept_id, course_level))
        conn.commit()
        return True, f"SUCCESS: Course '{course_code} - {course_title}' registered with ID {new_id}."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


def add_course_offering(course_id, faculty_id, academic_year, semester, classroom, max_capacity):
    """Schedules a new course section offering."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MAX(offering_id) FROM COURSE_OFFERING;")
        max_id = cursor.fetchone()[0] or 500
        new_id = max_id + 1
        cursor.execute("""
            INSERT INTO COURSE_OFFERING (offering_id, course_id, faculty_id, academic_year, semester, classroom, max_capacity, current_enrolled)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0);
        """, (new_id, course_id, faculty_id, academic_year, semester, classroom, max_capacity))
        conn.commit()
        return True, f"SUCCESS: Course Offering section #{new_id} scheduled in classroom {classroom}."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


def add_department(dept_name, dept_code, building, budget, established_year):
    """Creates a new academic department."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MAX(dept_id) FROM DEPARTMENT;")
        max_id = cursor.fetchone()[0] or 0
        new_id = max_id + 1
        cursor.execute("""
            INSERT INTO DEPARTMENT (dept_id, dept_name, dept_code, building, budget, established_year)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (new_id, dept_name, dept_code, building, budget, established_year))
        conn.commit()
        return True, f"SUCCESS: Department '{dept_name}' ({dept_code}) created with ID {new_id}."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


# 2. Stored Procedures and Transactions
def register_student(reg_no, first_name, last_name, email, phone, dob, gender, admission_date, dept_id, current_semester):
    """
    Business Transaction: Registers a new student into the institutional database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT NVL_ID FROM (SELECT MAX(student_id) AS NVL_ID FROM STUDENT);")
        max_id = cursor.fetchone()[0] or 200
        new_id = max_id + 1

        cursor.execute("""
            INSERT INTO STUDENT (student_id, reg_no, first_name, last_name, email, phone,
                                 date_of_birth, gender, admission_date, dept_id, current_semester, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active');
        """, (new_id, reg_no, first_name, last_name, email, phone, dob, gender, admission_date, dept_id, current_semester))

        conn.commit()
        return True, f"SUCCESS: Student '{first_name} {last_name}' registered successfully with ID {new_id} and Reg No {reg_no}."
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return False, f"DATABASE INTEGRITY ERROR: {str(e)}"
    except Exception as e:
        conn.rollback()
        return False, f"TRANSACTION ERROR: {str(e)}"
    finally:
        conn.close()


def enroll_student_proc(student_id, offering_id):
    """
    PL/SQL Procedure 1: Enroll_Student_Proc
    Enrolls a student into a course offering with full validation, seat capacity check,
    and automatic offering seat counter update.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Step 1: Validate Student
        cursor.execute("SELECT first_name || ' ' || last_name, status FROM STUDENT WHERE student_id = ?;", (student_id,))
        student_res = cursor.fetchone()
        if not student_res:
            return False, f"VALIDATION ERROR: Student ID {student_id} does not exist."
        if student_res[1] != 'Active':
            return False, f"VALIDATION ERROR: Student ID {student_id} is not currently active."
        student_name = student_res[0]

        # Step 2: Validate Offering and Seat Capacity
        cursor.execute("""
            SELECT co.max_capacity, co.current_enrolled, c.course_code, c.course_title
            FROM COURSE_OFFERING co
            JOIN COURSE c ON co.course_id = c.course_id
            WHERE co.offering_id = ?;
        """, (offering_id,))
        offering_res = cursor.fetchone()
        if not offering_res:
            return False, f"VALIDATION ERROR: Course Offering ID {offering_id} does not exist."

        max_cap, curr_enrolled, course_code, course_title = offering_res
        if curr_enrolled >= max_cap:
            return False, f"REGISTRATION REJECTED: Course offering #{offering_id} ({course_code}) is FULL ({curr_enrolled}/{max_cap} seats filled)."

        # Step 3: Check Duplicate Enrollment
        cursor.execute("SELECT count(*) FROM ENROLLMENT WHERE student_id = ? AND offering_id = ?;", (student_id, offering_id))
        if cursor.fetchone()[0] > 0:
            return False, f"VALIDATION ERROR: Student {student_name} is already registered in Course Offering #{offering_id}."

        # Step 4: Perform Enrollment INSERT
        cursor.execute("SELECT COALESCE(MAX(enrollment_id), 500) + 1 FROM ENROLLMENT;")
        new_enrollment_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO ENROLLMENT (enrollment_id, student_id, offering_id, enrollment_date, status)
            VALUES (?, ?, ?, DATE('now'), 'Enrolled');
        """, (new_enrollment_id, student_id, offering_id))

        # Step 5: Update Offering Seat Count (Trigger / Procedure step)
        cursor.execute("""
            UPDATE COURSE_OFFERING
            SET current_enrolled = current_enrolled + 1
            WHERE offering_id = ?;
        """, (offering_id,))

        conn.commit()
        return True, (f"SUCCESS: Enrollment #{new_enrollment_id} confirmed for {student_name} in "
                      f"'{course_code} - {course_title}'. Seats remaining: {max_cap - (curr_enrolled + 1)}")

    except Exception as e:
        conn.rollback()
        return False, f"TRANSACTION FAILED: {str(e)}"
    finally:
        conn.close()


def process_fee_payment_proc(student_id, amount, payment_method, transaction_ref=None):
    """
    PL/SQL Procedure 2: Process_Fee_Payment_Proc
    Processes student tuition fees, records transaction reference, and updates payment state.
    """
    if amount <= 0:
        return False, "VALIDATION ERROR: Payment amount must be strictly greater than 0."

    if not transaction_ref:
        transaction_ref = f"TXN_CMS_{datetime.now().strftime('%Y%m%d%H%M%S')}_{student_id}"

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Validate Student
        cursor.execute("SELECT first_name || ' ' || last_name, reg_no FROM STUDENT WHERE student_id = ?;", (student_id,))
        student_res = cursor.fetchone()
        if not student_res:
            return False, f"VALIDATION ERROR: Student ID {student_id} does not exist."
        student_name, reg_no = student_res

        # Check Duplicate Transaction Ref
        cursor.execute("SELECT count(*) FROM FEE_PAYMENT WHERE transaction_ref = ?;", (transaction_ref,))
        if cursor.fetchone()[0] > 0:
            return False, f"VALIDATION ERROR: Duplicate transaction reference '{transaction_ref}'."

        cursor.execute("SELECT COALESCE(MAX(payment_id), 700) + 1 FROM FEE_PAYMENT;")
        new_payment_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO FEE_PAYMENT (payment_id, student_id, amount_paid, payment_date, payment_method, transaction_ref, payment_status)
            VALUES (?, ?, ?, DATE('now'), ?, ?, 'Success');
        """, (new_payment_id, student_id, amount, payment_method, transaction_ref))

        conn.commit()
        return True, (f"RECEIPT ISSUED: Payment #{new_payment_id} of {amount:,.2f} recorded for "
                      f"{student_name} ({reg_no}) via {payment_method}. Ref: {transaction_ref}")
    except Exception as e:
        conn.rollback()
        return False, f"PAYMENT TRANSACTION FAILED: {str(e)}"
    finally:
        conn.close()


def record_exam_result_proc(enrollment_id, marks_obtained, remarks="Regular Semester Exam"):
    """
    PL/SQL Procedure 3: Record_Exam_Result_Proc
    Records exam marks, computes grade ('S','A','B','C','D','E','F'), and stores results.
    """
    if not (0.0 <= marks_obtained <= 100.0):
        return False, "VALIDATION ERROR: Marks must be between 0.00 and 100.00."

    # Compute Grade
    if marks_obtained >= 90.0:
        grade = 'S'
    elif marks_obtained >= 80.0:
        grade = 'A'
    elif marks_obtained >= 70.0:
        grade = 'B'
    elif marks_obtained >= 60.0:
        grade = 'C'
    elif marks_obtained >= 50.0:
        grade = 'D'
    elif marks_obtained >= 40.0:
        grade = 'E'
    else:
        grade = 'F'

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Validate Enrollment
        cursor.execute("""
            SELECT s.reg_no, s.first_name || ' ' || s.last_name, c.course_code
            FROM ENROLLMENT e
            JOIN STUDENT s ON e.student_id = s.student_id
            JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
            JOIN COURSE c ON co.course_id = c.course_id
            WHERE e.enrollment_id = ?;
        """, (enrollment_id,))
        enroll_res = cursor.fetchone()
        if not enroll_res:
            return False, f"VALIDATION ERROR: Enrollment ID {enrollment_id} does not exist."
        reg_no, student_name, course_code = enroll_res

        # Check existing result (Upsert logic)
        cursor.execute("SELECT result_id FROM EXAM_RESULT WHERE enrollment_id = ?;", (enrollment_id,))
        existing_res = cursor.fetchone()

        if existing_res:
            result_id = existing_res[0]
            cursor.execute("""
                UPDATE EXAM_RESULT
                SET marks_obtained = ?, grade = ?, exam_date = DATE('now'), remarks = ?
                WHERE enrollment_id = ?;
            """, (marks_obtained, grade, remarks, enrollment_id))
            action = "UPDATED"
        else:
            cursor.execute("SELECT COALESCE(MAX(result_id), 600) + 1 FROM EXAM_RESULT;")
            result_id = cursor.fetchone()[0]
            cursor.execute("""
                INSERT INTO EXAM_RESULT (result_id, enrollment_id, marks_obtained, grade, exam_date, remarks)
                VALUES (?, ?, ?, ?, DATE('now'), ?);
            """, (result_id, enrollment_id, marks_obtained, grade, remarks))
            action = "RECORDED"

        # Mark enrollment as completed
        cursor.execute("UPDATE ENROLLMENT SET status = 'Completed' WHERE enrollment_id = ?;", (enrollment_id,))

        conn.commit()
        return True, (f"SUCCESS: Exam Result {action} for {student_name} ({reg_no}) in {course_code}: "
                      f"Marks = {marks_obtained}, Grade = '{grade}' ({remarks}).")
    except Exception as e:
        conn.rollback()
        return False, f"EXAM TRANSACTION FAILED: {str(e)}"
    finally:
        conn.close()


# 3. Functions
def calculate_student_gpa_func(student_id):
    """
    PL/SQL Function 1: Calculate_Student_GPA_Func
    Calculates weighted Cumulative GPA on a 10.0 scale based on course credits and letter grades.
    """
    grade_points = {'S': 10.0, 'A': 9.0, 'B': 8.0, 'C': 7.0, 'D': 6.0, 'E': 5.0, 'F': 0.0}

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.credits, er.grade
        FROM ENROLLMENT e
        JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
        JOIN COURSE c ON co.course_id = c.course_id
        JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id
        WHERE e.student_id = ?;
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return 0.0, 0

    total_credits = 0
    total_points = 0.0
    for r in rows:
        cred = r[0]
        grd = r[1]
        pts = grade_points.get(grd, 0.0)
        total_credits += cred
        total_points += (cred * pts)

    cgpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
    return cgpa, total_credits


def calculate_pending_fee_func(student_id, standard_annual_fee=190000.00):
    """
    PL/SQL Function 2: Calculate_Pending_Fee_Func
    Returns outstanding balance for a given student against benchmark tuition fees.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(amount_paid), 0)
        FROM FEE_PAYMENT
        WHERE student_id = ? AND payment_status = 'Success';
    """, (student_id,))
    total_paid = cursor.fetchone()[0] or 0.0
    conn.close()

    pending = max(0.0, standard_annual_fee - total_paid)
    return pending, total_paid


# 4. Cursor
def generate_academic_report_cursor():
    """
    PL/SQL Cursor: Generate_Academic_Report_Cursor
    Iterates through multiple student records, aggregating courses, marks, and GPA,
    and classifying students into honors categories.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.student_id,
            s.reg_no,
            s.first_name || ' ' || s.last_name AS full_name,
            d.dept_code,
            COUNT(er.result_id) AS total_courses_evaluated,
            COALESCE(SUM(c.credits), 0) AS total_credits_earned,
            COALESCE(ROUND(AVG(er.marks_obtained), 2), 0.0) AS avg_marks
        FROM STUDENT s
        JOIN DEPARTMENT d ON s.dept_id = d.dept_id
        LEFT JOIN ENROLLMENT e ON s.student_id = e.student_id
        LEFT JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
        LEFT JOIN COURSE c ON co.course_id = c.course_id
        LEFT JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id
        WHERE s.status = 'Active'
        GROUP BY s.student_id, s.reg_no, s.first_name, s.last_name, d.dept_code
        ORDER BY avg_marks DESC, total_credits_earned DESC;
    """)

    processed_records = []
    total_evaluated = 0
    honors_count = 0
    first_class_count = 0

    for row in cursor.fetchall():
        r = dict(row)
        total_evaluated += 1
        avg_m = r["avg_marks"]
        courses_cnt = r["total_courses_evaluated"]

        if avg_m >= 90.0 and courses_cnt > 0:
            standing = "Dean's List (Distinction)"
            honors_count += 1
        elif avg_m >= 75.0 and courses_cnt > 0:
            standing = "First Class with Merit"
            first_class_count += 1
        elif avg_m >= 50.0 and courses_cnt > 0:
            standing = "Satisfactory / Pass"
        elif courses_cnt == 0:
            standing = "Awaiting Evaluation"
        else:
            standing = "Academic Warning"

        r["standing"] = standing
        # Also compute GPA using function
        gpa, _ = calculate_student_gpa_func(r["student_id"])
        r["cgpa"] = gpa
        processed_records.append(r)

    conn.close()

    summary_stats = {
        "total_evaluated": total_evaluated,
        "honors_count": honors_count,
        "first_class_count": first_class_count
    }
    return processed_records, summary_stats
