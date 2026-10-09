"""
College Management System - CLI Application
Terminal interface for testing database operations.
"""


import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db_manager import (
    initialize_database,
    get_connection,
    get_all_students,
    get_all_departments,
    get_all_faculty,
    get_all_course_offerings,
    get_enrollments,
    get_fee_payments,
    register_student,
    enroll_student_proc,
    process_fee_payment_proc,
    record_exam_result_proc,
    calculate_student_gpa_func,
    calculate_pending_fee_func,
    generate_academic_report_cursor
)
from demo_runner import run_all_transactions
from query_runner import run_all_queries


def print_header(title):
    print("\n" + "=" * 80)
    print(f" {title.center(78)} ")
    print("=" * 80)


def print_table(headers, rows):
    if not rows:
        print("  [No records found]")
        return
    col_widths = [max(len(str(h)), max((len(str(row[i])) for row in rows), default=0)) for i, h in enumerate(headers)]
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    print(header_line)
    print(separator)
    for row in rows:
        print(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))
    print(f"Total Records: {len(rows)}")


def handle_view_students():
    print_header("STUDENT ROSTER")
    students = get_all_students()
    headers = ["ID", "REG NO", "FULL NAME", "DEPT", "SEM", "EMAIL", "STATUS"]
    rows = [[s["student_id"], s["reg_no"], s["full_name"], s["dept_code"], s["current_semester"], s["email"], s["status"]] for s in students]
    print_table(headers, rows)


def handle_register_student():
    print_header("REGISTER NEW STUDENT (TRANSACTION 1)")
    try:
        reg_no = input("Enter Registration No (e.g. 24BCS0123): ").strip()
        first_name = input("Enter First Name: ").strip()
        last_name = input("Enter Last Name: ").strip()
        email = input("Enter Email: ").strip()
        phone = input("Enter Phone: ").strip()
        dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
        gender = input("Enter Gender (Male/Female/Other): ").strip()
        admission_date = input("Enter Admission Date (YYYY-MM-DD): ").strip()
        
        # Display departments
        depts = get_all_departments()
        print("\nAvailable Departments:")
        for d in depts:
            print(f"  {d['dept_id']}: {d['dept_code']} - {d['dept_name']}")
        dept_id = int(input("Select Department ID: ").strip())
        current_semester = int(input("Enter Current Semester (1-8): ").strip())

        success, msg = register_student(
            reg_no, first_name, last_name, email, phone, dob, gender, admission_date, dept_id, current_semester
        )
        print("\n" + ("[*] " if success else "[!] ") + msg)
    except Exception as e:
        print(f"[!] Input Error: {e}")


def handle_view_course_offerings():
    print_header("COURSE CATALOG & TERM OFFERINGS")
    offerings = get_all_course_offerings()
    headers = ["OFFERING ID", "COURSE CODE", "COURSE TITLE", "CREDITS", "INSTRUCTOR", "ROOM", "ENROLLED", "MAX", "SEATS LEFT"]
    rows = [[
        o["offering_id"], o["course_code"], o["course_title"], o["credits"],
        o["instructor"], o["classroom"], o["current_enrolled"], o["max_capacity"], o["available_seats"]
    ] for o in offerings]
    print_table(headers, rows)


def handle_enroll_student():
    print_header("ENROLL STUDENT IN COURSE (TRANSACTION 2 - PROCEDURE)")
    try:
        student_id = int(input("Enter Student ID (e.g. 201): ").strip())
        offering_id = int(input("Enter Course Offering ID (e.g. 401): ").strip())
        success, msg = enroll_student_proc(student_id, offering_id)
        print("\n" + ("[*] " if success else "[!] ") + msg)
    except Exception as e:
        print(f"[!] Error: {e}")


def handle_view_enrollments():
    print_header("COURSE ENROLLMENTS")
    enrollments = get_enrollments()
    headers = ["ENROLL ID", "REG NO", "STUDENT", "COURSE CODE", "COURSE TITLE", "INSTRUCTOR", "STATUS", "MARKS", "GRADE"]
    rows = [[
        e["enrollment_id"], e["reg_no"], e["student_name"], e["course_code"],
        e["course_title"], e["instructor"], e["enrollment_status"],
        e["marks_obtained"] if e["marks_obtained"] is not None else "Pending",
        e["grade"] if e["grade"] is not None else "-"
    ] for e in enrollments]
    print_table(headers, rows)


def handle_record_exam_result():
    print_header("RECORD / UPDATE EXAM RESULT (TRANSACTION 3 - PROCEDURE)")
    try:
        enrollment_id = int(input("Enter Enrollment ID to Grade (e.g. 501): ").strip())
        marks = float(input("Enter Marks Obtained (0.00 - 100.00): ").strip())
        remarks = input("Enter Faculty Remarks (optional): ").strip()
        if not remarks:
            remarks = "Continuous Assessment Evaluation"
        success, msg = record_exam_result_proc(enrollment_id, marks, remarks)
        print("\n" + ("[*] " if success else "[!] ") + msg)
    except Exception as e:
        print(f"[!] Error: {e}")


def handle_process_fee_payment():
    print_header("PROCESS FEE PAYMENT (TRANSACTION 4 - PROCEDURE)")
    try:
        student_id = int(input("Enter Student ID: ").strip())
        amount = float(input("Enter Amount to Pay (): ").strip())
        print("Payment Methods: [1] UPI | [2] Net Banking | [3] Credit Card | [4] Debit Card")
        method_opt = input("Select Method (1-4): ").strip()
        methods = {"1": "UPI", "2": "Net Banking", "3": "Credit Card", "4": "Debit Card"}
        method = methods.get(method_opt, "UPI")
        success, msg = process_fee_payment_proc(student_id, amount, method)
        print("\n" + ("[*] " if success else "[!] ") + msg)
    except Exception as e:
        print(f"[!] Error: {e}")


def handle_view_fees():
    print_header("FEE PAYMENT TRANSACTIONS & BALANCE")
    payments = get_fee_payments()
    headers = ["PAYMENT ID", "REG NO", "STUDENT", "AMOUNT ()", "DATE", "METHOD", "TRANSACTION REF", "STATUS"]
    rows = [[
        p["payment_id"], p["reg_no"], p["student_name"], f"{p['amount_paid']:,.2f}",
        p["payment_date"], p["payment_method"], p["transaction_ref"], p["payment_status"]
    ] for p in payments]
    print_table(headers, rows)


def handle_student_gpa():
    print_header("STUDENT GPA & DUES CALCULATOR (PL/SQL FUNCTIONS)")
    try:
        student_id = int(input("Enter Student ID: ").strip())
        gpa, credits = calculate_student_gpa_func(student_id)
        pending, paid = calculate_pending_fee_func(student_id)
        print("-" * 60)
        print(f"  Student ID          : {student_id}")
        print(f"  Cumulative GPA      : {gpa} / 10.0")
        print(f"  Total Credits       : {credits}")
        print(f"  Total Fees Paid     : {paid:,.2f}")
        print(f"  Pending Tuition Dues: {pending:,.2f}")
        print("-" * 60)
    except Exception as e:
        print(f"[!] Error: {e}")


def handle_academic_report():
    print_header("INSTITUTIONAL ACADEMIC AUDIT REPORT (TRANSACTION 5 - CURSOR)")
    records, summary = generate_academic_report_cursor()
    headers = ["REG NO", "STUDENT NAME", "DEPT", "COURSES", "CREDITS", "AVG MARKS", "CGPA", "HONORS STANDING"]
    rows = [[
        r["reg_no"], r["full_name"], r["dept_code"], r["total_courses_evaluated"],
        r["total_credits_earned"], f"{r['avg_marks']:.2f}", f"{r['cgpa']:.2f}", r["standing"]
    ] for r in records]
    print_table(headers, rows)
    print("\nAudit Summary:")
    print(f"  - Total Students Evaluated: {summary['total_evaluated']}")
    print(f"  - Dean's List (Distinction): {summary['honors_count']}")
    print(f"  - First Class with Merit   : {summary['first_class_count']}")


def main_menu():
    initialize_database()

    while True:
        print("\n" + "=" * 60)
        print("          COLLEGE MANAGEMENT SYSTEM")
        print("=" * 60)
        print("  [1]  View All Students")
        print("  [2]  Register New Student                     (Transaction 1 - INSERT)")
        print("  [3]  View Course Catalog & Term Offerings")
        print("  [4]  Enroll Student in Course Offering        (Transaction 2 - Procedure)")
        print("  [5]  View Student Enrollments & Rosters")
        print("  [6]  Record / Update Exam Result              (Transaction 3 - Procedure)")
        print("  [7]  Process Student Fee Payment              (Transaction 4 - Procedure)")
        print("  [8]  View Fee Transactions & Balances")
        print("  [9]  Calculate Student GPA & Pending Fees     (Functions 1 & 2)")
        print("  [10] Generate Academic Audit Report           (Transaction 5 - Cursor)")
        print("  [11] Run All 16 SQL Analytical Queries        (Review II Queries)")
        print("  [12] Run All 5 Real-World Transactions Demo   (Review III / Viva 1-Click)")
        print("  [13] Reset Database to Fresh Default State")
        print("  [0]  Exit")
        print("=" * 80)

        choice = input("Enter selection [0-13]: ").strip()

        if choice == "1":
            handle_view_students()
        elif choice == "2":
            handle_register_student()
        elif choice == "3":
            handle_view_course_offerings()
        elif choice == "4":
            handle_enroll_student()
        elif choice == "5":
            handle_view_enrollments()
        elif choice == "6":
            handle_record_exam_result()
        elif choice == "7":
            handle_process_fee_payment()
        elif choice == "8":
            handle_view_fees()
        elif choice == "9":
            handle_student_gpa()
        elif choice == "10":
            handle_academic_report()
        elif choice == "11":
            run_all_queries()
        elif choice == "12":
            run_all_transactions()
        elif choice == "13":
            confirm = input("Are you sure you want to reset the database? (y/n): ").strip().lower()
            if confirm == "y":
                initialize_database(force_recreate=True)
                print("[*] Database successfully re-created and populated with default seed data.")
        elif choice == "0":
            print("\nExiting College Management System. Goodbye!\n")
            break
        else:
            print("[!] Invalid selection. Please enter a number between 0 and 13.")


if __name__ == "__main__":
    main_menu()
