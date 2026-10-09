-- SQL Queries for College Management System

-- Query 1: Active students sorted by name
SELECT 
    student_id, 
    reg_no, 
    first_name || ' ' || last_name AS full_name, 
    email, 
    current_semester, 
    admission_date
FROM STUDENT
WHERE status = 'Active' AND current_semester >= 4
ORDER BY last_name ASC, first_name ASC;

-- Query 2: Students with their department
SELECT 
    s.student_id,
    s.reg_no,
    s.first_name || ' ' || s.last_name AS student_name,
    d.dept_name,
    d.dept_code,
    d.building
FROM STUDENT s
INNER JOIN DEPARTMENT d ON s.dept_id = d.dept_id
ORDER BY d.dept_code, s.reg_no;

-- Query 3: Faculty members sorted by salary
SELECT 
    f.faculty_id,
    f.first_name || ' ' || f.last_name AS faculty_name,
    f.designation,
    f.email,
    f.salary,
    d.dept_name
FROM FACULTY f
INNER JOIN DEPARTMENT d ON f.dept_id = d.dept_id
ORDER BY f.salary DESC;

-- Query 4: Course offerings with faculty details
SELECT 
    co.offering_id,
    c.course_code,
    c.course_title,
    c.credits,
    f.first_name || ' ' || f.last_name AS instructor,
    co.classroom,
    co.current_enrolled || ' / ' || co.max_capacity AS seat_utilization
FROM COURSE_OFFERING co
INNER JOIN COURSE c ON co.course_id = c.course_id
INNER JOIN FACULTY f ON co.faculty_id = f.faculty_id
WHERE co.academic_year = '2025-2026'
ORDER BY c.course_code;

-- Query 5: Student enrollments with course and faculty
SELECT 
    e.enrollment_id,
    s.reg_no,
    s.first_name || ' ' || s.last_name AS student_name,
    c.course_code,
    c.course_title,
    f.first_name || ' ' || f.last_name AS instructor,
    e.status AS enrollment_status
FROM ENROLLMENT e
INNER JOIN STUDENT s ON e.student_id = s.student_id
INNER JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
INNER JOIN COURSE c ON co.course_id = c.course_id
INNER JOIN FACULTY f ON co.faculty_id = f.faculty_id
ORDER BY c.course_code, s.reg_no;

-- Query 6: Average, min, max marks per course
SELECT 
    c.course_code,
    c.course_title,
    COUNT(er.result_id) AS total_graded_students,
    ROUND(AVG(er.marks_obtained), 2) AS average_marks,
    MIN(er.marks_obtained) AS lowest_marks,
    MAX(er.marks_obtained) AS highest_marks
FROM COURSE c
INNER JOIN COURSE_OFFERING co ON c.course_id = co.course_id
INNER JOIN ENROLLMENT e ON co.offering_id = e.offering_id
INNER JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id
GROUP BY c.course_code, c.course_title
ORDER BY average_marks DESC;

-- Query 7: Departments with 2 or more students
SELECT 
    d.dept_id,
    d.dept_code,
    d.dept_name,
    COUNT(s.student_id) AS total_students
FROM DEPARTMENT d
INNER JOIN STUDENT s ON d.dept_id = s.dept_id
GROUP BY d.dept_id, d.dept_code, d.dept_name
HAVING COUNT(s.student_id) >= 2
ORDER BY total_students DESC;

-- Query 8: Total faculty salary per department
SELECT 
    d.dept_name,
    d.budget,
    COUNT(f.faculty_id) AS faculty_count,
    ROUND(SUM(f.salary), 2) AS total_monthly_payroll,
    ROUND(AVG(f.salary), 2) AS average_faculty_salary
FROM DEPARTMENT d
LEFT JOIN FACULTY f ON d.dept_id = f.dept_id
GROUP BY d.dept_id, d.dept_name, d.budget
ORDER BY total_monthly_payroll DESC;

-- Query 9: Highest scoring student
SELECT 
    s.reg_no,
    s.first_name || ' ' || s.last_name AS student_name,
    c.course_code,
    c.course_title,
    er.marks_obtained,
    er.grade,
    er.remarks
FROM EXAM_RESULT er
INNER JOIN ENROLLMENT e ON er.enrollment_id = e.enrollment_id
INNER JOIN STUDENT s ON e.student_id = s.student_id
INNER JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
INNER JOIN COURSE c ON co.course_id = c.course_id
WHERE er.marks_obtained = (SELECT MAX(marks_obtained) FROM EXAM_RESULT);

-- Query 10: Students scoring above course average
SELECT 
    s.reg_no,
    s.first_name || ' ' || s.last_name AS student_name,
    c.course_code,
    er.marks_obtained
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

-- Query 11: Faculty in Block A or Block B
SELECT 
    faculty_id,
    first_name || ' ' || last_name AS faculty_name,
    email,
    designation
FROM FACULTY
WHERE dept_id IN (
    SELECT dept_id 
    FROM DEPARTMENT 
    WHERE building IN ('Block A', 'Block B')
);

-- Query 12: Courses without enrollments
SELECT 
    c.course_id,
    c.course_code,
    c.course_title,
    d.dept_name
FROM COURSE c
INNER JOIN DEPARTMENT d ON c.dept_id = d.dept_id
WHERE NOT EXISTS (
    SELECT 1 
    FROM COURSE_OFFERING co
    INNER JOIN ENROLLMENT e ON co.offering_id = e.offering_id
    WHERE co.course_id = c.course_id
);

-- Query 13: Total fee paid and balance for each student
SELECT 
    s.student_id,
    s.reg_no,
    s.first_name || ' ' || s.last_name AS student_name,
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

-- Query 14: Count of students per grade
SELECT 
    grade,
    COUNT(*) AS total_students_awarded,
    ROUND(AVG(marks_obtained), 2) AS average_marks_in_grade,
    MIN(marks_obtained) AS min_mark,
    MAX(marks_obtained) AS max_mark
FROM EXAM_RESULT
GROUP BY grade
ORDER BY average_marks_in_grade DESC;

-- Query 15: Student transcript view
SELECT 
    s.reg_no,
    s.first_name || ' ' || s.last_name AS student_name,
    c.course_code,
    c.course_title,
    c.credits,
    er.marks_obtained,
    er.grade,
    er.remarks
FROM STUDENT s
INNER JOIN ENROLLMENT e ON s.student_id = e.student_id
INNER JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
INNER JOIN COURSE c ON co.course_id = c.course_id
INNER JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id
ORDER BY s.reg_no, c.course_code;

-- Query 16: Fee collection by payment method
SELECT 
    payment_method,
    COUNT(payment_id) AS transaction_count,
    ROUND(SUM(amount_paid), 2) AS total_revenue_collected,
    ROUND(AVG(amount_paid), 2) AS average_transaction_amount
FROM FEE_PAYMENT
WHERE payment_status = 'Success'
GROUP BY payment_method
ORDER BY total_revenue_collected DESC;

-- Query 17: Update exam marks for re-evaluation
UPDATE EXAM_RESULT
SET marks_obtained = 95.00,
    grade = 'S',
    remarks = 'Score updated post review by Course Coordinator'
WHERE enrollment_id = 501;

-- Query 18: Delete dummy enrollment record
DELETE FROM ENROLLMENT
WHERE enrollment_id = 999;
