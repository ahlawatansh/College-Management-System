-- Real-World Transactions Demonstration for College Management System

-- Transaction 1: Register a new student
-- Check count before
SELECT COUNT(*) AS total_students_before FROM STUDENT;

-- Insert new student (Student 21)
INSERT INTO STUDENT (student_id, reg_no, first_name, last_name, email, phone, date_of_birth, gender, admission_date, dept_id, current_semester, status)
VALUES (221, 'REG_21', 'Student', '21', 'student21@college.edu', '9811223399', '2004-09-15', 'Male', '2024-07-15', 2, 4, 'Active');

-- Verify inserted student
SELECT student_id, reg_no, first_name || ' ' || last_name AS student_name, email, dept_id, status 
FROM STUDENT 
WHERE student_id = 221;


-- Transaction 2: Enroll student in a course offering
-- Check seats before
SELECT offering_id, course_id, current_enrolled, max_capacity 
FROM COURSE_OFFERING 
WHERE offering_id = 404;

-- Insert enrollment record
INSERT INTO ENROLLMENT (enrollment_id, student_id, offering_id, enrollment_date, status)
VALUES (526, 221, 404, CURRENT_DATE, 'Enrolled');

-- Verify enrollment record
SELECT e.enrollment_id, s.reg_no, s.first_name || ' ' || s.last_name AS student, c.course_code, c.course_title, e.status
FROM ENROLLMENT e
JOIN STUDENT s ON e.student_id = s.student_id
JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
JOIN COURSE c ON co.course_id = c.course_id
WHERE e.enrollment_id = 526;

-- Update offering seat count
UPDATE COURSE_OFFERING SET current_enrolled = current_enrolled + 1 WHERE offering_id = 404;
SELECT offering_id, course_id, current_enrolled, max_capacity 
FROM COURSE_OFFERING 
WHERE offering_id = 404;


-- Transaction 3: Record exam result
-- Insert exam score for enrollment 526
INSERT INTO EXAM_RESULT (result_id, enrollment_id, marks_obtained, grade, exam_date, remarks)
VALUES (626, 526, 92.50, 'S', CURRENT_DATE, 'Good performance');

-- Verify result
SELECT er.result_id, s.reg_no, s.first_name || ' ' || s.last_name AS student, c.course_code, er.marks_obtained, er.grade, er.remarks
FROM EXAM_RESULT er
JOIN ENROLLMENT e ON er.enrollment_id = e.enrollment_id
JOIN STUDENT s ON e.student_id = s.student_id
JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
JOIN COURSE c ON co.course_id = c.course_id
WHERE er.result_id = 626;


-- Transaction 4: Process fee payment
-- Insert fee payment for student 221
INSERT INTO FEE_PAYMENT (payment_id, student_id, amount_paid, payment_date, payment_method, transaction_ref, payment_status)
VALUES (726, 221, 95000.00, CURRENT_DATE, 'UPI', 'TXN_26', 'Success');

-- Verify payment
SELECT fp.payment_id, s.reg_no, s.first_name || ' ' || s.last_name AS student, fp.amount_paid, fp.payment_method, fp.transaction_ref, fp.payment_status
FROM FEE_PAYMENT fp
JOIN STUDENT s ON fp.student_id = s.student_id
WHERE fp.payment_id = 726;

-- Check remaining balance
SELECT 
    s.student_id, 
    s.reg_no, 
    s.first_name || ' ' || last_name AS student_name,
    COALESCE(SUM(fp.amount_paid), 0) AS total_fees_paid,
    (190000.00 - COALESCE(SUM(fp.amount_paid), 0)) AS remaining_balance
FROM STUDENT s
LEFT JOIN FEE_PAYMENT fp ON s.student_id = fp.student_id
WHERE s.student_id = 221
GROUP BY s.student_id, s.reg_no, s.first_name, s.last_name;


-- Transaction 5: Academic report query
SELECT 
    s.reg_no,
    s.first_name || ' ' || s.last_name AS student_name,
    d.dept_code,
    COUNT(er.result_id) AS total_subjects,
    ROUND(AVG(er.marks_obtained), 2) AS average_score,
    CASE 
        WHEN AVG(er.marks_obtained) >= 90 THEN 'Distinction'
        WHEN AVG(er.marks_obtained) >= 75 THEN 'First Class'
        WHEN AVG(er.marks_obtained) >= 50 THEN 'Pass'
        ELSE 'Needs Improvement'
    END AS academic_status
FROM STUDENT s
JOIN DEPARTMENT d ON s.dept_id = d.dept_id
JOIN ENROLLMENT e ON s.student_id = e.student_id
JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id
GROUP BY s.student_id, s.reg_no, s.first_name, s.last_name, d.dept_code
ORDER BY average_score DESC;
