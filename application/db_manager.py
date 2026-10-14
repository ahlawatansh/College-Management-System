import os
import sqlite3
from datetime import datetime, date
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'college_cms.db')
SQL_DDL_PATH = os.path.join(BASE_DIR, 'database', '01_create_tables.sql')
SQL_DML_PATH = os.path.join(BASE_DIR, 'database', '02_insert_data.sql')
SQL_QUERIES_PATH = os.path.join(BASE_DIR, 'database', '03_queries.sql')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def initialize_database(force_recreate=False):
    if force_recreate and os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='STUDENT';")
    exists = cursor.fetchone()[0]
    if exists == 0 or force_recreate:
        with open(SQL_DDL_PATH, 'r', encoding='utf-8') as f:
            ddl_script = f.read()
        cursor.executescript(ddl_script)
        with open(SQL_DML_PATH, 'r', encoding='utf-8') as f:
            dml_script = f.read()
        cursor.executescript(dml_script)
        conn.commit()
    conn.close()
    return True

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    query = "\n    SELECT \n        s.student_id, s.reg_no, s.first_name || ' ' || s.last_name AS full_name,\n        s.email, s.phone, s.date_of_birth, s.gender, s.current_semester, s.status,\n        d.dept_code, d.dept_name\n    FROM STUDENT s\n    JOIN DEPARTMENT d ON s.dept_id = d.dept_id\n    ORDER BY s.student_id ASC;\n    "
    cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_all_departments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM DEPARTMENT ORDER BY dept_id ASC;')
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_all_faculty():
    conn = get_connection()
    cursor = conn.cursor()
    query = "\n    SELECT f.faculty_id, f.first_name || ' ' || f.last_name AS faculty_name,\n           f.designation, f.email, f.phone, f.salary, d.dept_code\n    FROM FACULTY f\n    JOIN DEPARTMENT d ON f.dept_id = d.dept_id\n    ORDER BY f.faculty_id ASC;\n    "
    cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_all_course_offerings():
    conn = get_connection()
    cursor = conn.cursor()
    query = "\n    SELECT co.offering_id, c.course_code, c.course_title, c.credits,\n           f.first_name || ' ' || f.last_name AS instructor,\n           co.academic_year, co.semester, co.classroom,\n           co.current_enrolled, co.max_capacity,\n           (co.max_capacity - co.current_enrolled) AS available_seats\n    FROM COURSE_OFFERING co\n    JOIN COURSE c ON co.course_id = c.course_id\n    JOIN FACULTY f ON co.faculty_id = f.faculty_id\n    ORDER BY co.offering_id ASC;\n    "
    cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_enrollments(student_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "\n    SELECT e.enrollment_id, s.reg_no, s.first_name || ' ' || s.last_name AS student_name,\n           c.course_code, c.course_title, f.first_name || ' ' || f.last_name AS instructor,\n           e.enrollment_date, e.status AS enrollment_status,\n           er.marks_obtained, er.grade\n    FROM ENROLLMENT e\n    JOIN STUDENT s ON e.student_id = s.student_id\n    JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id\n    JOIN COURSE c ON co.course_id = c.course_id\n    JOIN FACULTY f ON co.faculty_id = f.faculty_id\n    LEFT JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id\n    "
    if student_id:
        query += ' WHERE e.student_id = ? ORDER BY e.enrollment_id ASC;'
        cursor.execute(query, (student_id,))
    else:
        query += ' ORDER BY e.enrollment_id ASC;'
        cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_fee_payments(student_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "\n    SELECT fp.payment_id, s.reg_no, s.first_name || ' ' || s.last_name AS student_name,\n           fp.amount_paid, fp.payment_date, fp.payment_method,\n           fp.transaction_ref, fp.payment_status\n    FROM FEE_PAYMENT fp\n    JOIN STUDENT s ON fp.student_id = s.student_id\n    "
    if student_id:
        query += ' WHERE fp.student_id = ? ORDER BY fp.payment_date DESC;'
        cursor.execute(query, (student_id,))
    else:
        query += ' ORDER BY fp.payment_date DESC;'
        cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_all_courses():
    conn = get_connection()
    cursor = conn.cursor()
    query = '\n    SELECT c.course_id, c.course_code, c.course_title, c.credits, c.course_level,\n           d.dept_code, d.dept_name\n    FROM COURSE c\n    JOIN DEPARTMENT d ON c.dept_id = d.dept_id\n    ORDER BY c.course_id ASC;\n    '
    cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_all_exam_results():
    conn = get_connection()
    cursor = conn.cursor()
    query = "\n    SELECT er.result_id, er.enrollment_id, s.reg_no, s.first_name || ' ' || s.last_name AS student_name,\n           c.course_code, c.course_title, er.marks_obtained, er.grade, er.exam_date, er.remarks\n    FROM EXAM_RESULT er\n    JOIN ENROLLMENT e ON er.enrollment_id = e.enrollment_id\n    JOIN STUDENT s ON e.student_id = s.student_id\n    JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id\n    JOIN COURSE c ON co.course_id = c.course_id\n    ORDER BY er.result_id ASC;\n    "
    cursor.execute(query)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def add_faculty(first_name, last_name, email, phone, hire_date, designation, salary, dept_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT MAX(faculty_id) FROM FACULTY;')
        max_id = cursor.fetchone()[0] or 100
        new_id = max_id + 1
        cursor.execute('\n            INSERT INTO FACULTY (faculty_id, first_name, last_name, email, phone, hire_date, designation, salary, dept_id)\n            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);\n        ', (new_id, first_name, last_name, email, phone, hire_date, designation, salary, dept_id))
        conn.commit()
        return (True, f"SUCCESS: Faculty member '{first_name} {last_name}' appointed with ID {new_id}.")
    except Exception as e:
        conn.rollback()
        return (False, str(e))
    finally:
        conn.close()

def add_course(course_code, course_title, credits, dept_id, course_level):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT MAX(course_id) FROM COURSE;')
        max_id = cursor.fetchone()[0] or 300
        new_id = max_id + 1
        cursor.execute('\n            INSERT INTO COURSE (course_id, course_code, course_title, credits, dept_id, course_level)\n            VALUES (?, ?, ?, ?, ?, ?);\n        ', (new_id, course_code, course_title, credits, dept_id, course_level))
        conn.commit()
        return (True, f"SUCCESS: Course '{course_code} - {course_title}' registered with ID {new_id}.")
    except Exception as e:
        conn.rollback()
        return (False, str(e))
    finally:
        conn.close()

def add_course_offering(course_id, faculty_id, academic_year, semester, classroom, max_capacity):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT MAX(offering_id) FROM COURSE_OFFERING;')
        max_id = cursor.fetchone()[0] or 500
        new_id = max_id + 1
        cursor.execute('\n            INSERT INTO COURSE_OFFERING (offering_id, course_id, faculty_id, academic_year, semester, classroom, max_capacity, current_enrolled)\n            VALUES (?, ?, ?, ?, ?, ?, ?, 0);\n        ', (new_id, course_id, faculty_id, academic_year, semester, classroom, max_capacity))
        conn.commit()
        return (True, f'SUCCESS: Course Offering section #{new_id} scheduled in classroom {classroom}.')
    except Exception as e:
        conn.rollback()
        return (False, str(e))
    finally:
        conn.close()

def add_department(dept_name, dept_code, building, budget, established_year):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT MAX(dept_id) FROM DEPARTMENT;')
        max_id = cursor.fetchone()[0] or 0
        new_id = max_id + 1
        cursor.execute('\n            INSERT INTO DEPARTMENT (dept_id, dept_name, dept_code, building, budget, established_year)\n            VALUES (?, ?, ?, ?, ?, ?);\n        ', (new_id, dept_name, dept_code, building, budget, established_year))
        conn.commit()
        return (True, f"SUCCESS: Department '{dept_name}' ({dept_code}) created with ID {new_id}.")
    except Exception as e:
        conn.rollback()
        return (False, str(e))
    finally:
        conn.close()

def register_student(reg_no, first_name, last_name, email, phone, dob, gender, admission_date, dept_id, current_semester):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT NVL_ID FROM (SELECT MAX(student_id) AS NVL_ID FROM STUDENT);')
        max_id = cursor.fetchone()[0] or 200
        new_id = max_id + 1
        cursor.execute("\n            INSERT INTO STUDENT (student_id, reg_no, first_name, last_name, email, phone,\n                                 date_of_birth, gender, admission_date, dept_id, current_semester, status)\n            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Active');\n        ", (new_id, reg_no, first_name, last_name, email, phone, dob, gender, admission_date, dept_id, current_semester))
        conn.commit()
        return (True, f"SUCCESS: Student '{first_name} {last_name}' registered successfully with ID {new_id} and Reg No {reg_no}.")
    except sqlite3.IntegrityError as e:
        conn.rollback()
        return (False, f'DATABASE INTEGRITY ERROR: {str(e)}')
    except Exception as e:
        conn.rollback()
        return (False, f'TRANSACTION ERROR: {str(e)}')
    finally:
        conn.close()

def enroll_student_proc(student_id, offering_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT first_name || ' ' || last_name, status FROM STUDENT WHERE student_id = ?;", (student_id,))
        student_res = cursor.fetchone()
        if not student_res:
            return (False, f'VALIDATION ERROR: Student ID {student_id} does not exist.')
        if student_res[1] != 'Active':
            return (False, f'VALIDATION ERROR: Student ID {student_id} is not currently active.')
        student_name = student_res[0]
        cursor.execute('\n            SELECT co.max_capacity, co.current_enrolled, c.course_code, c.course_title\n            FROM COURSE_OFFERING co\n            JOIN COURSE c ON co.course_id = c.course_id\n            WHERE co.offering_id = ?;\n        ', (offering_id,))
        offering_res = cursor.fetchone()
        if not offering_res:
            return (False, f'VALIDATION ERROR: Course Offering ID {offering_id} does not exist.')
        max_cap, curr_enrolled, course_code, course_title = offering_res
        if curr_enrolled >= max_cap:
            return (False, f'REGISTRATION REJECTED: Course offering #{offering_id} ({course_code}) is FULL ({curr_enrolled}/{max_cap} seats filled).')
        cursor.execute('SELECT count(*) FROM ENROLLMENT WHERE student_id = ? AND offering_id = ?;', (student_id, offering_id))
        if cursor.fetchone()[0] > 0:
            return (False, f'VALIDATION ERROR: Student {student_name} is already registered in Course Offering #{offering_id}.')
        cursor.execute('SELECT COALESCE(MAX(enrollment_id), 500) + 1 FROM ENROLLMENT;')
        new_enrollment_id = cursor.fetchone()[0]
        cursor.execute("\n            INSERT INTO ENROLLMENT (enrollment_id, student_id, offering_id, enrollment_date, status)\n            VALUES (?, ?, ?, DATE('now'), 'Enrolled');\n        ", (new_enrollment_id, student_id, offering_id))
        cursor.execute('\n            UPDATE COURSE_OFFERING\n            SET current_enrolled = current_enrolled + 1\n            WHERE offering_id = ?;\n        ', (offering_id,))
        conn.commit()
        return (True, f"SUCCESS: Enrollment #{new_enrollment_id} confirmed for {student_name} in '{course_code} - {course_title}'. Seats remaining: {max_cap - (curr_enrolled + 1)}")
    except Exception as e:
        conn.rollback()
        return (False, f'TRANSACTION FAILED: {str(e)}')
    finally:
        conn.close()

def process_fee_payment_proc(student_id, amount, payment_method, transaction_ref=None):
    if amount <= 0:
        return (False, 'VALIDATION ERROR: Payment amount must be strictly greater than 0.')
    if not transaction_ref:
        transaction_ref = f"TXN_CMS_{datetime.now().strftime('%Y%m%d%H%M%S')}_{student_id}"
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT first_name || ' ' || last_name, reg_no FROM STUDENT WHERE student_id = ?;", (student_id,))
        student_res = cursor.fetchone()
        if not student_res:
            return (False, f'VALIDATION ERROR: Student ID {student_id} does not exist.')
        student_name, reg_no = student_res
        cursor.execute('SELECT count(*) FROM FEE_PAYMENT WHERE transaction_ref = ?;', (transaction_ref,))
        if cursor.fetchone()[0] > 0:
            return (False, f"VALIDATION ERROR: Duplicate transaction reference '{transaction_ref}'.")
        cursor.execute('SELECT COALESCE(MAX(payment_id), 700) + 1 FROM FEE_PAYMENT;')
        new_payment_id = cursor.fetchone()[0]
        cursor.execute("\n            INSERT INTO FEE_PAYMENT (payment_id, student_id, amount_paid, payment_date, payment_method, transaction_ref, payment_status)\n            VALUES (?, ?, ?, DATE('now'), ?, ?, 'Success');\n        ", (new_payment_id, student_id, amount, payment_method, transaction_ref))
        conn.commit()
        return (True, f'RECEIPT ISSUED: Payment #{new_payment_id} of {amount:,.2f} recorded for {student_name} ({reg_no}) via {payment_method}. Ref: {transaction_ref}')
    except Exception as e:
        conn.rollback()
        return (False, f'PAYMENT TRANSACTION FAILED: {str(e)}')
    finally:
        conn.close()

def record_exam_result_proc(enrollment_id, marks_obtained, remarks='Regular Semester Exam'):
    if not 0.0 <= marks_obtained <= 100.0:
        return (False, 'VALIDATION ERROR: Marks must be between 0.00 and 100.00.')
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
        cursor.execute("\n            SELECT s.reg_no, s.first_name || ' ' || s.last_name, c.course_code\n            FROM ENROLLMENT e\n            JOIN STUDENT s ON e.student_id = s.student_id\n            JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id\n            JOIN COURSE c ON co.course_id = c.course_id\n            WHERE e.enrollment_id = ?;\n        ", (enrollment_id,))
        enroll_res = cursor.fetchone()
        if not enroll_res:
            return (False, f'VALIDATION ERROR: Enrollment ID {enrollment_id} does not exist.')
        reg_no, student_name, course_code = enroll_res
        cursor.execute('SELECT result_id FROM EXAM_RESULT WHERE enrollment_id = ?;', (enrollment_id,))
        existing_res = cursor.fetchone()
        if existing_res:
            result_id = existing_res[0]
            cursor.execute("\n                UPDATE EXAM_RESULT\n                SET marks_obtained = ?, grade = ?, exam_date = DATE('now'), remarks = ?\n                WHERE enrollment_id = ?;\n            ", (marks_obtained, grade, remarks, enrollment_id))
            action = 'UPDATED'
        else:
            cursor.execute('SELECT COALESCE(MAX(result_id), 600) + 1 FROM EXAM_RESULT;')
            result_id = cursor.fetchone()[0]
            cursor.execute("\n                INSERT INTO EXAM_RESULT (result_id, enrollment_id, marks_obtained, grade, exam_date, remarks)\n                VALUES (?, ?, ?, ?, DATE('now'), ?);\n            ", (result_id, enrollment_id, marks_obtained, grade, remarks))
            action = 'RECORDED'
        cursor.execute("UPDATE ENROLLMENT SET status = 'Completed' WHERE enrollment_id = ?;", (enrollment_id,))
        conn.commit()
        return (True, f"SUCCESS: Exam Result {action} for {student_name} ({reg_no}) in {course_code}: Marks = {marks_obtained}, Grade = '{grade}' ({remarks}).")
    except Exception as e:
        conn.rollback()
        return (False, f'EXAM TRANSACTION FAILED: {str(e)}')
    finally:
        conn.close()

def calculate_student_gpa_func(student_id):
    grade_points = {'S': 10.0, 'A': 9.0, 'B': 8.0, 'C': 7.0, 'D': 6.0, 'E': 5.0, 'F': 0.0}
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('\n        SELECT c.credits, er.grade\n        FROM ENROLLMENT e\n        JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id\n        JOIN COURSE c ON co.course_id = c.course_id\n        JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id\n        WHERE e.student_id = ?;\n    ', (student_id,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return (0.0, 0)
    total_credits = 0
    total_points = 0.0
    for r in rows:
        cred = r[0]
        grd = r[1]
        pts = grade_points.get(grd, 0.0)
        total_credits += cred
        total_points += cred * pts
    cgpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
    return (cgpa, total_credits)

def calculate_pending_fee_func(student_id, standard_annual_fee=190000.0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("\n        SELECT COALESCE(SUM(amount_paid), 0)\n        FROM FEE_PAYMENT\n        WHERE student_id = ? AND payment_status = 'Success';\n    ", (student_id,))
    total_paid = cursor.fetchone()[0] or 0.0
    conn.close()
    pending = max(0.0, standard_annual_fee - total_paid)
    return (pending, total_paid)

def generate_academic_report_cursor():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("\n        SELECT \n            s.student_id,\n            s.reg_no,\n            s.first_name || ' ' || s.last_name AS full_name,\n            d.dept_code,\n            COUNT(er.result_id) AS total_courses_evaluated,\n            COALESCE(SUM(c.credits), 0) AS total_credits_earned,\n            COALESCE(ROUND(AVG(er.marks_obtained), 2), 0.0) AS avg_marks\n        FROM STUDENT s\n        JOIN DEPARTMENT d ON s.dept_id = d.dept_id\n        LEFT JOIN ENROLLMENT e ON s.student_id = e.student_id\n        LEFT JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id\n        LEFT JOIN COURSE c ON co.course_id = c.course_id\n        LEFT JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id\n        WHERE s.status = 'Active'\n        GROUP BY s.student_id, s.reg_no, s.first_name, s.last_name, d.dept_code\n        ORDER BY avg_marks DESC, total_credits_earned DESC;\n    ")
    processed_records = []
    total_evaluated = 0
    honors_count = 0
    first_class_count = 0
    for row in cursor.fetchall():
        r = dict(row)
        total_evaluated += 1
        avg_m = r['avg_marks']
        courses_cnt = r['total_courses_evaluated']
        if avg_m >= 90.0 and courses_cnt > 0:
            standing = "Dean's List (Distinction)"
            honors_count += 1
        elif avg_m >= 75.0 and courses_cnt > 0:
            standing = 'First Class with Merit'
            first_class_count += 1
        elif avg_m >= 50.0 and courses_cnt > 0:
            standing = 'Satisfactory / Pass'
        elif courses_cnt == 0:
            standing = 'Awaiting Evaluation'
        else:
            standing = 'Academic Warning'
        r['standing'] = standing
        gpa, _ = calculate_student_gpa_func(r['student_id'])
        r['cgpa'] = gpa
        processed_records.append(r)
    conn.close()
    summary_stats = {'total_evaluated': total_evaluated, 'honors_count': honors_count, 'first_class_count': first_class_count}
    return (processed_records, summary_stats)
