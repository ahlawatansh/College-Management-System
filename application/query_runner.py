"""
Query Runner for College Management System
Executes the 16 SQL queries and prints the results.
"""


import sys
import os
# Pure Python ASCII formatting

# Add application directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db_manager import get_connection, initialize_database

QUERIES = [
    {
        "id": "Q1",
        "title": "Active Undergraduate Students (WHERE + ORDER BY)",
        "sql": """
            SELECT student_id, reg_no, first_name || ' ' || last_name AS full_name, 
                   email, current_semester, admission_date
            FROM STUDENT
            WHERE status = 'Active' AND current_semester >= 4
            ORDER BY last_name ASC, first_name ASC;
        """
    },
    {
        "id": "Q2",
        "title": "Students with Department Details (Two-Table INNER JOIN)",
        "sql": """
            SELECT s.student_id, s.reg_no, s.first_name || ' ' || s.last_name AS student_name,
                   d.dept_name, d.dept_code, d.building
            FROM STUDENT s
            INNER JOIN DEPARTMENT d ON s.dept_id = d.dept_id
            ORDER BY d.dept_code, s.reg_no;
        """
    },
    {
        "id": "Q3",
        "title": "Faculty Roster by Salary (INNER JOIN + ORDER BY DESC)",
        "sql": """
            SELECT f.faculty_id, f.first_name || ' ' || f.last_name AS faculty_name,
                   f.designation, f.salary, d.dept_code
            FROM FACULTY f
            INNER JOIN DEPARTMENT d ON f.dept_id = d.dept_id
            ORDER BY f.salary DESC;
        """
    },
    {
        "id": "Q4",
        "title": "Course Offerings with Faculty & Venue (Three-Table JOIN)",
        "sql": """
            SELECT co.offering_id, c.course_code, c.course_title, c.credits,
                   f.first_name || ' ' || f.last_name AS instructor,
                   co.classroom, co.current_enrolled || ' / ' || co.max_capacity AS seats
            FROM COURSE_OFFERING co
            INNER JOIN COURSE c ON co.course_id = c.course_id
            INNER JOIN FACULTY f ON co.faculty_id = f.faculty_id
            WHERE co.academic_year = '2025-2026'
            ORDER BY c.course_code;
        """
    },
    {
        "id": "Q5",
        "title": "Student Course Enrollment Roster (Four-Table JOIN)",
        "sql": """
            SELECT e.enrollment_id, s.reg_no, s.first_name || ' ' || s.last_name AS student,
                   c.course_code, c.course_title, f.first_name || ' ' || f.last_name AS instructor,
                   e.status
            FROM ENROLLMENT e
            INNER JOIN STUDENT s ON e.student_id = s.student_id
            INNER JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
            INNER JOIN COURSE c ON co.course_id = c.course_id
            INNER JOIN FACULTY f ON co.faculty_id = f.faculty_id
            ORDER BY c.course_code, s.reg_no;
        """
    },
    {
        "id": "Q6",
        "title": "Course-Wise Grade Statistics (Aggregations: AVG, MIN, MAX, COUNT)",
        "sql": """
            SELECT c.course_code, c.course_title,
                   COUNT(er.result_id) AS total_graded,
                   ROUND(AVG(er.marks_obtained), 2) AS avg_marks,
                   MIN(er.marks_obtained) AS lowest_marks,
                   MAX(er.marks_obtained) AS highest_marks
            FROM COURSE c
            INNER JOIN COURSE_OFFERING co ON c.course_id = co.course_id
            INNER JOIN ENROLLMENT e ON co.offering_id = e.offering_id
            INNER JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id
            GROUP BY c.course_code, c.course_title
            ORDER BY avg_marks DESC;
        """
    },
    {
        "id": "Q7",
        "title": "Departments Having >= 2 Students (GROUP BY + HAVING)",
        "sql": """
            SELECT d.dept_id, d.dept_code, d.dept_name,
                   COUNT(s.student_id) AS total_students
            FROM DEPARTMENT d
            INNER JOIN STUDENT s ON d.dept_id = s.dept_id
            GROUP BY d.dept_id, d.dept_code, d.dept_name
            HAVING COUNT(s.student_id) >= 2
            ORDER BY total_students DESC;
        """
    },
    {
        "id": "Q8",
        "title": "Department Payroll vs Budget Analysis (LEFT JOIN + SUM + AVG)",
        "sql": """
            SELECT d.dept_name, d.budget,
                   COUNT(f.faculty_id) AS faculty_count,
                   ROUND(SUM(f.salary), 2) AS monthly_payroll,
                   ROUND(AVG(f.salary), 2) AS avg_salary
            FROM DEPARTMENT d
            LEFT JOIN FACULTY f ON d.dept_id = f.dept_id
            GROUP BY d.dept_id, d.dept_name, d.budget
            ORDER BY monthly_payroll DESC;
        """
    },
    {
        "id": "Q9",
        "title": "Top-Scoring Student in the University (Nested Subquery with MAX)",
        "sql": """
            SELECT s.reg_no, s.first_name || ' ' || s.last_name AS student_name,
                   c.course_code, c.course_title, er.marks_obtained, er.grade, er.remarks
            FROM EXAM_RESULT er
            INNER JOIN ENROLLMENT e ON er.enrollment_id = e.enrollment_id
            INNER JOIN STUDENT s ON e.student_id = s.student_id
            INNER JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
            INNER JOIN COURSE c ON co.course_id = c.course_id
            WHERE er.marks_obtained = (SELECT MAX(marks_obtained) FROM EXAM_RESULT);
        """
    },
    {
        "id": "Q10",
        "title": "Students Scoring Strictly Above Course Average (Correlated Subquery)",
        "sql": """
            SELECT s.reg_no, s.first_name || ' ' || s.last_name AS student_name,
                   c.course_code, er.marks_obtained
            FROM EXAM_RESULT er
            INNER JOIN ENROLLMENT e ON er.enrollment_id = e.enrollment_id
            INNER JOIN STUDENT s ON e.student_id = s.student_id
            INNER JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
            INNER JOIN COURSE c ON co.course_id = c.course_id
            WHERE er.marks_obtained > (
                SELECT AVG(inner_er.marks_obtained)
                FROM EXAM_RESULT inner_er
                INNER JOIN ENROLLMENT inner_e ON inner_er.enrollment_id = inner_e.enrollment_id
                INNER JOIN COURSE_OFFERING inner_co ON inner_e.offering_id = inner_co.offering_id
                WHERE inner_co.course_id = c.course_id
            )
            ORDER BY er.marks_obtained DESC;
        """
    },
    {
        "id": "Q11",
        "title": "Faculty in Academic Blocks (Subquery with IN)",
        "sql": """
            SELECT faculty_id, first_name || ' ' || last_name AS faculty_name,
                   email, designation
            FROM FACULTY
            WHERE dept_id IN (
                SELECT dept_id FROM DEPARTMENT WHERE building IN ('Block A', 'Block B')
            );
        """
    },
    {
        "id": "Q12",
        "title": "Courses Without Active Enrollments (Subquery with NOT EXISTS)",
        "sql": """
            SELECT c.course_id, c.course_code, c.course_title, d.dept_name
            FROM COURSE c
            INNER JOIN DEPARTMENT d ON c.dept_id = d.dept_id
            WHERE NOT EXISTS (
                SELECT 1 FROM COURSE_OFFERING co
                INNER JOIN ENROLLMENT e ON co.offering_id = e.offering_id
                WHERE co.course_id = c.course_id
            );
        """
    },
    {
        "id": "Q13",
        "title": "Student Fee Payment Status & Balance (CASE Statement + Aggregation)",
        "sql": """
            SELECT s.student_id, s.reg_no, s.first_name || ' ' || s.last_name AS student_name,
                   COALESCE(SUM(fp.amount_paid), 0) AS total_fees_paid,
                   CASE 
                       WHEN COALESCE(SUM(fp.amount_paid), 0) >= 190000.00 THEN 'Fully Paid'
                       WHEN COALESCE(SUM(fp.amount_paid), 0) > 0 THEN 'Partial Dues'
                       ELSE 'Unpaid'
                   END AS payment_status,
                   (190000.00 - COALESCE(SUM(fp.amount_paid), 0)) AS balance_amount
            FROM STUDENT s
            LEFT JOIN FEE_PAYMENT fp ON s.student_id = fp.student_id
            GROUP BY s.student_id, s.reg_no, s.first_name, s.last_name
            ORDER BY balance_amount ASC;
        """
    },
    {
        "id": "Q14",
        "title": "Grade Distribution Summary Across University",
        "sql": """
            SELECT grade, COUNT(*) AS students_count,
                   ROUND(AVG(marks_obtained), 2) AS avg_score,
                   MIN(marks_obtained) AS min_mark,
                   MAX(marks_obtained) AS max_mark
            FROM EXAM_RESULT
            GROUP BY grade
            ORDER BY avg_score DESC;
        """
    },
    {
        "id": "Q15",
        "title": "Multi-Table Academic Transcript View",
        "sql": """
            SELECT s.reg_no, s.first_name || ' ' || s.last_name AS student,
                   c.course_code, c.course_title, c.credits,
                   er.marks_obtained, er.grade, er.remarks
            FROM STUDENT s
            INNER JOIN ENROLLMENT e ON s.student_id = e.student_id
            INNER JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
            INNER JOIN COURSE c ON co.course_id = c.course_id
            INNER JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id
            ORDER BY s.reg_no, c.course_code;
        """
    },
    {
        "id": "Q16",
        "title": "Institutional Revenue Breakdown by Payment Method",
        "sql": """
            SELECT payment_method,
                   COUNT(payment_id) AS transactions_count,
                   ROUND(SUM(amount_paid), 2) AS total_revenue,
                   ROUND(AVG(amount_paid), 2) AS avg_transaction
            FROM FEE_PAYMENT
            WHERE payment_status = 'Success'
            GROUP BY payment_method
            ORDER BY total_revenue DESC;
        """
    }
]


def run_all_queries():
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()

    print("\nRunning SQL Queries...")

    for item in QUERIES:
        print(f"\n[{item['id']}] {item['title']}")
        print("-" * 60)
        try:
            cursor.execute(item['sql'])
            rows = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]
            table_data = [[r[h] for h in headers] for r in rows]

            col_widths = [max(len(str(h)), max((len(str(row[i])) for row in table_data), default=0)) for i, h in enumerate(headers)]
            header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
            separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
            print(header_line)
            print(separator)
            for row in table_data:
                print(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))
            print(f"Total Rows: {len(rows)}")
        except Exception as e:
            print(f"Execution Error: {e}")

    conn.close()
    print("\nDone running all queries.\n")


if __name__ == "__main__":
    run_all_queries()
