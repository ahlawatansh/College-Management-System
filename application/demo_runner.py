"""
Real-world transactions demo script for College Management System.
Demonstrates:
  1. Register a student
  2. Enroll in course offering
  3. Record exam marks
  4. Process fee payment
  5. Generate academic report using cursor
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db_manager import (
    initialize_database,
    get_connection,
    register_student,
    enroll_student_proc,
    record_exam_result_proc,
    process_fee_payment_proc,
    calculate_student_gpa_func,
    calculate_pending_fee_func,
    generate_academic_report_cursor
)


def run_all_transactions():
    initialize_database()

    print("\n" + "=" * 70)
    print("      COLLEGE MANAGEMENT SYSTEM - REAL-WORLD TRANSACTIONS DEMO")
    print("=" * 70)

    # 1. Register a new student
    print("\n--- 1. Register New Student ---")
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM STUDENT;")
    count_before = c.fetchone()[0]
    conn.close()
    print(f"Total students before: {count_before}")

    success, msg = register_student(
        reg_no="REG_21",
        first_name="Student",
        last_name="21",
        email="student21@college.edu",
        phone="9811223399",
        dob="2004-09-15",
        gender="Male",
        admission_date="2024-07-15",
        dept_id=2,
        current_semester=4
    )
    print(f"Result: {msg}")

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT student_id, reg_no, first_name || ' ' || last_name, email, current_semester, status FROM STUDENT WHERE reg_no = 'REG_21';")
    new_student = c.fetchone()
    conn.close()
    print(f"Verified in DB -> ID: {new_student[0]} | Reg: {new_student[1]} | Name: {new_student[2]}")
    student_id = new_student[0]

    # 2. Enroll student in course offering
    print("\n--- 2. Enroll Student in Course Offering ---")
    offering_id = 404
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT current_enrolled, max_capacity FROM COURSE_OFFERING WHERE offering_id = ?;", (offering_id,))
    curr_seats_before, max_cap = c.fetchone()
    conn.close()
    print(f"Offering #{offering_id} seats before: {curr_seats_before}/{max_cap}")

    success, msg = enroll_student_proc(student_id=student_id, offering_id=offering_id)
    print(f"Result: {msg}")

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT current_enrolled FROM COURSE_OFFERING WHERE offering_id = ?;", (offering_id,))
    curr_seats_after = c.fetchone()[0]
    c.execute("""
        SELECT e.enrollment_id, s.reg_no, c.course_code, c.course_title, e.status
        FROM ENROLLMENT e
        JOIN STUDENT s ON e.student_id = s.student_id
        JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
        JOIN COURSE c ON co.course_id = c.course_id
        WHERE e.student_id = ? AND e.offering_id = ?;
    """, (student_id, offering_id))
    enrollment_row = c.fetchone()
    conn.close()
    print(f"Offering #{offering_id} seats after: {curr_seats_after}/{max_cap}")
    print(f"Enrollment ID: {enrollment_row[0]} | Course: {enrollment_row[2]} | Status: {enrollment_row[4]}")
    enrollment_id = enrollment_row[0]

    # 3. Record examination result
    print("\n--- 3. Record Exam Result ---")
    marks = 92.50
    success, msg = record_exam_result_proc(
        enrollment_id=enrollment_id,
        marks_obtained=marks,
        remarks="Good performance"
    )
    print(f"Result: {msg}")

    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT er.result_id, er.marks_obtained, er.grade, er.exam_date, er.remarks
        FROM EXAM_RESULT er
        WHERE er.enrollment_id = ?;
    """, (enrollment_id,))
    res_row = c.fetchone()
    conn.close()
    print(f"Result ID: {res_row[0]} | Marks: {res_row[1]} | Grade: {res_row[2]} | Remarks: {res_row[4]}")

    # 4. Process fee payment
    print("\n--- 4. Process Fee Payment ---")
    pending_before, paid_before = calculate_pending_fee_func(student_id)
    print(f"Student {student_id} Paid Before: {paid_before:,.2f} | Pending: {pending_before:,.2f}")

    amount = 95000.00
    success, msg = process_fee_payment_proc(
        student_id=student_id,
        amount=amount,
        payment_method="UPI",
        transaction_ref=f"TXN_26"
    )
    print(f"Result: {msg}")

    pending_after, paid_after = calculate_pending_fee_func(student_id)
    print(f"Student {student_id} Paid After: {paid_after:,.2f} | Pending: {pending_after:,.2f}")

    # 5. Generate academic report via cursor
    print("\n--- 5. Generate Academic Performance Report ---")
    records, summary = generate_academic_report_cursor()
    print(f"{'REG NO':<12} {'STUDENT NAME':<18} {'DEPT':<6} {'COURSES':<8} {'CREDITS':<8} {'AVG MARKS':<10} {'CGPA':<6} {'STATUS'}")
    print("-" * 80)
    for r in records[:8]:
        print(f"{r['reg_no']:<12} {r['full_name']:<18} {r['dept_code']:<6} {r['total_courses_evaluated']:<8} "
              f"{r['total_credits_earned']:<8} {r['avg_marks']:<10.2f} {r['cgpa']:<6.2f} {r['standing']}")
    print("-" * 80)
    print(f"Total Evaluated: {summary['total_evaluated']} | Distinction: {summary['honors_count']} | First Class: {summary['first_class_count']}")

    print("\n" + "=" * 70)
    print(" All transactions executed successfully!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_all_transactions()
