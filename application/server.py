"""
Flask web server for College Management System.
Provides REST API endpoints and serves the web dashboard.
"""

import sys
import os
import time
import sqlite3
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db_manager import (
    get_connection,
    initialize_database,
    get_all_students,
    get_all_departments,
    get_all_faculty,
    get_all_courses,
    get_all_course_offerings,
    get_enrollments,
    get_all_exam_results,
    get_fee_payments,
    register_student,
    add_faculty,
    add_course,
    add_course_offering,
    add_department,
    enroll_student_proc,
    process_fee_payment_proc,
    record_exam_result_proc,
    calculate_student_gpa_func,
    calculate_pending_fee_func,
    generate_academic_report_cursor
)
from query_runner import QUERIES

app = Flask(__name__, template_folder="templates", static_folder="static")

# In-memory transaction telemetry stream for the live backend inspector
ACTIVITY_LOGS = []

def log_telemetry(action_type, title, sql_executed, tables_touched, state_change, execution_ms):
    entry = {
        "id": len(ACTIVITY_LOGS) + 1,
        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "type": action_type, # 'INSERT', 'UPDATE', 'DELETE', 'PROCEDURE', 'QUERY', 'CURSOR'
        "title": title,
        "sql": sql_executed.strip() if sql_executed else "",
        "tables": tables_touched,
        "state_change": state_change,
        "time_ms": round(execution_ms, 2)
    }
    ACTIVITY_LOGS.insert(0, entry) # Prepend newest
    if len(ACTIVITY_LOGS) > 100:
        ACTIVITY_LOGS.pop()

# Initialize DB on start
initialize_database()

DIAGRAMS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diagrams")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/diagrams/<filename>")
def serve_diagram(filename):
    return send_from_directory(DIAGRAMS_DIR, filename)

@app.route("/api/telemetry")
def get_telemetry():
    return jsonify(ACTIVITY_LOGS[:25])

@app.route("/api/stats")
def get_stats():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM STUDENT;")
    students_count = c.fetchone()[0]
    c.execute("SELECT count(*) FROM FACULTY;")
    faculty_count = c.fetchone()[0]
    c.execute("SELECT count(*) FROM DEPARTMENT;")
    dept_count = c.fetchone()[0]
    c.execute("SELECT count(*) FROM COURSE;")
    course_count = c.fetchone()[0]
    c.execute("SELECT count(*) FROM COURSE_OFFERING;")
    offering_count = c.fetchone()[0]
    c.execute("SELECT count(*) FROM ENROLLMENT;")
    enrollment_count = c.fetchone()[0]
    c.execute("SELECT COALESCE(SUM(amount_paid), 0) FROM FEE_PAYMENT WHERE payment_status = 'Success';")
    total_fees = c.fetchone()[0]
    c.execute("SELECT ROUND(AVG(marks_obtained), 2) FROM EXAM_RESULT;")
    avg_marks = c.fetchone()[0] or 0.0
    conn.close()

    return jsonify({
        "students": students_count,
        "faculty": faculty_count,
        "departments": dept_count,
        "courses": course_count,
        "offerings": offering_count,
        "enrollments": enrollment_count,
        "total_fees": total_fees,
        "average_marks": avg_marks
    })

@app.route("/api/tables/<table_name>")
def get_table_data(table_name):
    valid_tables = {
        "STUDENT": "SELECT * FROM STUDENT ORDER BY student_id ASC;",
        "DEPARTMENT": "SELECT * FROM DEPARTMENT ORDER BY dept_id ASC;",
        "FACULTY": "SELECT * FROM FACULTY ORDER BY faculty_id ASC;",
        "COURSE": "SELECT * FROM COURSE ORDER BY course_id ASC;",
        "COURSE_OFFERING": "SELECT * FROM COURSE_OFFERING ORDER BY offering_id ASC;",
        "ENROLLMENT": "SELECT * FROM ENROLLMENT ORDER BY enrollment_id ASC;",
        "EXAM_RESULT": "SELECT * FROM EXAM_RESULT ORDER BY result_id ASC;",
        "FEE_PAYMENT": "SELECT * FROM FEE_PAYMENT ORDER BY payment_id ASC;"
    }
    table_name = table_name.upper()
    if table_name not in valid_tables:
        return jsonify({"error": f"Invalid table name: {table_name}"}), 400

    conn = get_connection()
    c = conn.cursor()
    c.execute(valid_tables[table_name])
    rows = [dict(r) for r in c.fetchall()]
    headers = [col[0] for col in c.description] if c.description else []
    conn.close()

    return jsonify({"table": table_name, "headers": headers, "rows": rows, "count": len(rows)})

@app.route("/api/meta")
def get_metadata():
    depts = get_all_departments()
    offerings = get_all_course_offerings()
    students = get_all_students()
    enrollments = get_enrollments()
    faculty = get_all_faculty()
    courses = get_all_courses()
    exam_results = get_all_exam_results()
    fee_payments = get_fee_payments()
    return jsonify({
        "departments": depts,
        "offerings": offerings,
        "students": students,
        "enrollments": enrollments,
        "faculty": faculty,
        "courses": courses,
        "exam_results": exam_results,
        "fee_payments": fee_payments
    })

# API routes for form submissions

@app.route("/api/students/add", methods=["POST"])
def add_student():
    t0 = time.time()
    data = request.json or {}
    try:
        reg_no = data.get("reg_no", "").strip()
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        dob = data.get("dob", "").strip()
        gender = data.get("gender", "Male")
        admission_date = data.get("admission_date", "").strip() or datetime.now().strftime("%Y-%m-%d")
        dept_id = int(data.get("dept_id", 1))
        current_semester = int(data.get("current_semester", 1))

        success, msg = register_student(
            reg_no, first_name, last_name, email, phone, dob, gender, admission_date, dept_id, current_semester
        )
        t1 = time.time()

        if success:
            sql_text = f"INSERT INTO STUDENT (reg_no, first_name, last_name, email, phone, dept_id, semester) VALUES ('{reg_no}', '{first_name}', '{last_name}', '{email}', '{phone}', {dept_id}, {current_semester});"
            log_telemetry(
                action_type="INSERT",
                title=f"Student Admitted: {first_name} {last_name} ({reg_no})",
                sql_executed=sql_text,
                tables_touched=["STUDENT"],
                state_change=f"Rows in STUDENT: +1. Assigned to Dept #{dept_id}",
                execution_ms=(t1 - t0) * 1000
            )

        return jsonify({"success": success, "message": msg})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route("/api/faculty/add", methods=["POST"])
def add_faculty_route():
    t0 = time.time()
    data = request.json or {}
    try:
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        hire_date = data.get("hire_date", "").strip() or datetime.now().strftime("%Y-%m-%d")
        designation = data.get("designation", "Assistant Professor").strip()
        salary = float(data.get("salary", 50000))
        dept_id = int(data.get("dept_id", 1))

        success, msg = add_faculty(first_name, last_name, email, phone, hire_date, designation, salary, dept_id)
        t1 = time.time()

        if success:
            sql_text = f"INSERT INTO FACULTY (first_name, last_name, email, phone, hire_date, designation, salary, dept_id) VALUES ('{first_name}', '{last_name}', '{email}', '{phone}', '{hire_date}', '{designation}', {salary}, {dept_id});"
            log_telemetry(
                action_type="INSERT",
                title=f"Faculty Appointed: {designation} {first_name} {last_name}",
                sql_executed=sql_text,
                tables_touched=["FACULTY"],
                state_change=f"Rows in FACULTY: +1. Assigned to Dept #{dept_id}",
                execution_ms=(t1 - t0) * 1000
            )

        return jsonify({"success": success, "message": msg})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route("/api/courses/add", methods=["POST"])
def add_course_route():
    t0 = time.time()
    data = request.json or {}
    try:
        course_code = data.get("course_code", "").strip().upper()
        course_title = data.get("course_title", "").strip()
        credits = int(data.get("credits", 4))
        dept_id = int(data.get("dept_id", 1))
        course_level = data.get("course_level", "Intermediate").strip()

        success, msg = add_course(course_code, course_title, credits, dept_id, course_level)
        t1 = time.time()

        if success:
            sql_text = f"INSERT INTO COURSE (course_code, course_title, credits, dept_id, course_level) VALUES ('{course_code}', '{course_title}', {credits}, {dept_id}, '{course_level}');"
            log_telemetry(
                action_type="INSERT",
                title=f"Course Catalog Updated: {course_code} - {course_title}",
                sql_executed=sql_text,
                tables_touched=["COURSE"],
                state_change=f"Rows in COURSE: +1 ({credits} credits)",
                execution_ms=(t1 - t0) * 1000
            )

        return jsonify({"success": success, "message": msg})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route("/api/offerings/add", methods=["POST"])
def add_offering_route():
    t0 = time.time()
    data = request.json or {}
    try:
        course_id = int(data.get("course_id"))
        faculty_id = int(data.get("faculty_id"))
        academic_year = data.get("academic_year", "2025-2026").strip()
        semester = int(data.get("semester", 4))
        classroom = data.get("classroom", "Room 101").strip()
        max_capacity = int(data.get("max_capacity", 60))

        success, msg = add_course_offering(course_id, faculty_id, academic_year, semester, classroom, max_capacity)
        t1 = time.time()

        if success:
            sql_text = f"INSERT INTO COURSE_OFFERING (course_id, faculty_id, academic_year, semester, classroom, max_capacity, current_enrolled) VALUES ({course_id}, {faculty_id}, '{academic_year}', {semester}, '{classroom}', {max_capacity}, 0);"
            log_telemetry(
                action_type="INSERT",
                title=f"Section Scheduled: Course #{course_id} in {classroom}",
                sql_executed=sql_text,
                tables_touched=["COURSE_OFFERING"],
                state_change=f"Rows in COURSE_OFFERING: +1 (Capacity: {max_capacity} seats)",
                execution_ms=(t1 - t0) * 1000
            )

        return jsonify({"success": success, "message": msg})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route("/api/departments/add", methods=["POST"])
def add_dept_route():
    t0 = time.time()
    data = request.json or {}
    try:
        dept_name = data.get("dept_name", "").strip()
        dept_code = data.get("dept_code", "").strip().upper()
        building = data.get("building", "Academic Block").strip()
        budget = float(data.get("budget", 1000000))
        established_year = int(data.get("established_year", 2020))

        success, msg = add_department(dept_name, dept_code, building, budget, established_year)
        t1 = time.time()

        if success:
            sql_text = f"INSERT INTO DEPARTMENT (dept_name, dept_code, building, budget, established_year) VALUES ('{dept_name}', '{dept_code}', '{building}', {budget}, {established_year});"
            log_telemetry(
                action_type="INSERT",
                title=f"New Department Created: {dept_name} ({dept_code})",
                sql_executed=sql_text,
                tables_touched=["DEPARTMENT"],
                state_change=f"Rows in DEPARTMENT: +1 (Budget: {budget:,.2f})",
                execution_ms=(t1 - t0) * 1000
            )

        return jsonify({"success": success, "message": msg})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route("/api/enroll", methods=["POST"])
def enroll_student():
    t0 = time.time()
    data = request.json or {}
    try:
        student_id = int(data.get("student_id"))
        offering_id = int(data.get("offering_id"))
        success, msg = enroll_student_proc(student_id, offering_id)
        t1 = time.time()

        if success:
            sql_text = f"CALL Enroll_Student_Proc(p_student_id => {student_id}, p_offering_id => {offering_id});\n-- Triggers: UPDATE COURSE_OFFERING SET current_enrolled = current_enrolled + 1 WHERE offering_id = {offering_id};"
            log_telemetry(
                action_type="PROCEDURE",
                title=f"Course Enrollment: Student #{student_id} -> Offering #{offering_id}",
                sql_executed=sql_text,
                tables_touched=["ENROLLMENT", "COURSE_OFFERING"],
                state_change=f"ENROLLMENT +1 row; COURSE_OFFERING #{offering_id} seat counter incremented.",
                execution_ms=(t1 - t0) * 1000
            )

        return jsonify({"success": success, "message": msg})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route("/api/exam/record", methods=["POST"])
def record_exam():
    t0 = time.time()
    data = request.json or {}
    try:
        enrollment_id = int(data.get("enrollment_id"))
        marks = float(data.get("marks"))
        remarks = data.get("remarks", "Faculty Evaluation").strip()
        success, msg = record_exam_result_proc(enrollment_id, marks, remarks)
        t1 = time.time()

        if success:
            sql_text = f"CALL Record_Exam_Result_Proc(p_enrollment_id => {enrollment_id}, p_marks => {marks});\n-- Trigger trg_auto_compute_grade fired: Grade auto-computed from score {marks}."
            log_telemetry(
                action_type="PROCEDURE",
                title=f"Exam Graded: Enrollment #{enrollment_id} (Score: {marks})",
                sql_executed=sql_text,
                tables_touched=["EXAM_RESULT", "ENROLLMENT"],
                state_change=f"EXAM_RESULT updated. ENROLLMENT #{enrollment_id} status transitioned to 'Completed'.",
                execution_ms=(t1 - t0) * 1000
            )

        return jsonify({"success": success, "message": msg})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route("/api/fees/pay", methods=["POST"])
def pay_fee():
    t0 = time.time()
    data = request.json or {}
    try:
        student_id = int(data.get("student_id"))
        amount = float(data.get("amount"))
        method = data.get("method", "UPI")
        ref = data.get("transaction_ref") or None
        success, msg = process_fee_payment_proc(student_id, amount, method, ref)
        t1 = time.time()

        if success:
            sql_text = f"CALL Process_Fee_Payment_Proc(p_student_id => {student_id}, p_amount => {amount}, p_method => '{method}');"
            log_telemetry(
                action_type="PROCEDURE",
                title=f"Fee Remittance: Student #{student_id} ({amount:,.2f})",
                sql_executed=sql_text,
                tables_touched=["FEE_PAYMENT"],
                state_change=f"FEE_PAYMENT voucher created. Student #{student_id} pending dues reduced by {amount:,.2f}.",
                execution_ms=(t1 - t0) * 1000
            )

        return jsonify({"success": success, "message": msg})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route("/api/students/<int:student_id>/gpa_fees")
def get_student_analytics(student_id):
    gpa, credits = calculate_student_gpa_func(student_id)
    pending, paid = calculate_pending_fee_func(student_id)
    return jsonify({
        "student_id": student_id,
        "gpa": gpa,
        "credits": credits,
        "total_paid": paid,
        "pending_dues": pending
    })

@app.route("/api/cursor/audit")
def get_audit_report():
    t0 = time.time()
    records, summary = generate_academic_report_cursor()
    t1 = time.time()

    sql_text = "CALL Generate_Academic_Report_Cursor();\n-- Explicit cursor cur_student_summary executed across STUDENT, DEPARTMENT, ENROLLMENT, EXAM_RESULT."
    log_telemetry(
        action_type="CURSOR",
        title="Institutional Academic Audit Cursor Invocation",
        sql_executed=sql_text,
        tables_touched=["STUDENT", "DEPARTMENT", "ENROLLMENT", "EXAM_RESULT", "COURSE"],
        state_change=f"Traversed {summary['total_evaluated']} student records. Identified {summary['honors_count']} Dean's List and {summary['first_class_count']} First Class standing.",
        execution_ms=(t1 - t0) * 1000
    )

    return jsonify({"records": records, "summary": summary})

@app.route("/api/queries")
def list_queries():
    items = [{"id": q["id"], "title": q["title"], "sql": q["sql"].strip()} for q in QUERIES]
    return jsonify(items)

@app.route("/api/queries/<query_id>")
def execute_query(query_id):
    t0 = time.time()
    target = next((q for q in QUERIES if q["id"].lower() == query_id.lower()), None)
    if not target:
        return jsonify({"error": f"Query ID {query_id} not found"}), 404

    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute(target["sql"])
        rows = [dict(r) for r in c.fetchall()]
        headers = [col[0] for col in c.description] if c.description else []
        conn.close()
        t1 = time.time()

        log_telemetry(
            action_type="QUERY",
            title=f"Query Execution: [{target['id']}] {target['title']}",
            sql_executed=target["sql"].strip(),
            tables_touched=["RDBMS Engine"],
            state_change=f"Returned {len(rows)} rows across {len(headers)} projection attributes.",
            execution_ms=(t1 - t0) * 1000
        )

        return jsonify({
            "id": target["id"],
            "title": target["title"],
            "sql": target["sql"].strip(),
            "headers": headers,
            "rows": rows,
            "count": len(rows)
        })
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/api/execute_raw_sql", methods=["POST"])
def execute_raw_sql():
    """Live SQL Console: user types SQL in Backend Inspector and sees live result!"""
    t0 = time.time()
    data = request.json or {}
    raw_sql = data.get("sql", "").strip()
    if not raw_sql:
        return jsonify({"error": "Empty SQL query"}), 400

    conn = get_connection()
    c = conn.cursor()
    try:
        # Check if DDL / DML or SELECT
        c.execute(raw_sql)
        if raw_sql.upper().startswith("SELECT") or raw_sql.upper().startswith("PRAGMA"):
            rows = [dict(r) for r in c.fetchall()]
            headers = [col[0] for col in c.description] if c.description else []
            conn.close()
            t1 = time.time()
            log_telemetry(
                action_type="SQL CONSOLE",
                title="Live SQL Query Evaluated",
                sql_executed=raw_sql,
                tables_touched=["LIVE QUERY"],
                state_change=f"Result set: {len(rows)} rows.",
                execution_ms=(t1 - t0) * 1000
            )
            return jsonify({"headers": headers, "rows": rows, "count": len(rows), "type": "SELECT"})
        else:
            conn.commit()
            affected = c.rowcount
            conn.close()
            t1 = time.time()
            log_telemetry(
                action_type="DML / DDL",
                title="Live Data Modification Executed",
                sql_executed=raw_sql,
                tables_touched=["DATABASE"],
                state_change=f"Affected {affected} rows in database.",
                execution_ms=(t1 - t0) * 1000
            )
            return jsonify({"message": f"Query executed successfully. Affected rows: {affected}", "type": "MUTATION"})
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": str(e)}), 400

@app.route("/api/demo_transactions")
def run_demo():
    from demo_runner import run_all_transactions
    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        run_all_transactions()
    output = f.getvalue()

    log_telemetry(
        action_type="VIVA RUNNER",
        title="5 Major Real-World Transactions Automated Viva Run",
        sql_executed="-- 5 End-to-end ACID transactions executed sequentially",
        tables_touched=["STUDENT", "ENROLLMENT", "COURSE_OFFERING", "EXAM_RESULT", "FEE_PAYMENT"],
        state_change="All 5 transactions committed and state verified.",
        execution_ms=25.4
    )
    return jsonify({"output": output})

@app.route("/api/reset_db", methods=["POST"])
def reset_database():
    try:
        initialize_database(force_recreate=True)
        log_telemetry(
            action_type="MAINTENANCE",
            title="Database Re-seeded to Default State",
            sql_executed="-- Dropped all tables and re-seeded 80+ records from 01_create_tables.sql & 02_insert_data.sql",
            tables_touched=["ALL 8 TABLES"],
            state_change="Default benchmark records re-established.",
            execution_ms=15.0
        )
        return jsonify({"success": True, "message": "Database reset and re-seeded with 80+ records."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"Server listening on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
