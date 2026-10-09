-- Sample data for College Management System

-- 1. Departments (5 Departments)
INSERT INTO DEPARTMENT (dept_id, dept_name, dept_code, building, budget, established_year) VALUES
(1, 'Department 1', 'DEP_01', 'Block A', 1500000.00, 1995),
(2, 'Department 2', 'DEP_02', 'Block B', 1250000.00, 2005),
(3, 'Department 3', 'DEP_03', 'Block A', 1100000.00, 2000),
(4, 'Department 4', 'DEP_04', 'Block C', 1400000.00, 1998),
(5, 'Department 5', 'DEP_05', 'Block D', 950000.00,  1996);

-- 2. Faculty (10 Faculty Members)
INSERT INTO FACULTY (faculty_id, first_name, last_name, email, phone, hire_date, designation, salary, dept_id) VALUES
(101, 'Faculty', '1',  'faculty1@college.edu',  '9800000101', '2010-06-15', 'Professor',           145000.00, 1),
(102, 'Faculty', '2',  'faculty2@college.edu',  '9800000102', '2012-08-20', 'Associate Professor', 115000.00, 2),
(103, 'Faculty', '3',  'faculty3@college.edu',  '9800000103', '2015-01-10', 'Assistant Professor', 88000.00,  1),
(104, 'Faculty', '4',  'faculty4@college.edu',  '9800000104', '2008-11-01', 'HOD',                 160000.00, 3),
(105, 'Faculty', '5',  'faculty5@college.edu',  '9800000105', '2014-04-18', 'Associate Professor', 110000.00, 4),
(106, 'Faculty', '6',  'faculty6@college.edu',  '9800000106', '2016-09-05', 'Assistant Professor', 82000.00,  5),
(107, 'Faculty', '7',  'faculty7@college.edu',  '9800000107', '2018-07-22', 'Assistant Professor', 78000.00,  2),
(108, 'Faculty', '8',  'faculty8@college.edu',  '9800000108', '2011-03-30', 'Associate Professor', 112000.00, 3),
(109, 'Faculty', '9',  'faculty9@college.edu',  '9800000109', '2019-12-01', 'Lecturer',            65000.00,  4),
(110, 'Faculty', '10', 'faculty10@college.edu', '9800000110', '2006-02-14', 'Dean',                175000.00, 5);

-- 3. Students (20 Students)
INSERT INTO STUDENT (student_id, reg_no, first_name, last_name, email, phone, date_of_birth, gender, admission_date, dept_id, current_semester, status) VALUES
(201, 'REG_01', 'Student', '1',  'student1@college.edu',  '9811000101', '2004-03-14', 'Male',   '2024-07-15', 1, 4, 'Active'),
(202, 'REG_02', 'Student', '2',  'student2@college.edu',  '9811000102', '2004-06-25', 'Male',   '2024-07-15', 1, 4, 'Active'),
(203, 'REG_03', 'Student', '3',  'student3@college.edu',  '9811000103', '2004-11-08', 'Male',   '2024-07-15', 2, 4, 'Active'),
(204, 'REG_04', 'Student', '4',  'student4@college.edu',  '9811000104', '2004-01-20', 'Male',   '2024-07-15', 2, 4, 'Active'),
(205, 'REG_05', 'Student', '5',  'student5@college.edu',  '9811000105', '2004-08-12', 'Female', '2024-07-15', 1, 4, 'Active'),
(206, 'REG_06', 'Student', '6',  'student6@college.edu',  '9811000106', '2003-12-05', 'Male',   '2023-07-20', 3, 6, 'Active'),
(207, 'REG_07', 'Student', '7',  'student7@college.edu',  '9811000107', '2004-04-17', 'Female', '2024-07-15', 4, 4, 'Active'),
(208, 'REG_08', 'Student', '8',  'student8@college.edu',  '9811000108', '2003-09-30', 'Male',   '2023-07-20', 5, 6, 'Active'),
(209, 'REG_09', 'Student', '9',  'student9@college.edu',  '9811000109', '2005-02-18', 'Female', '2025-07-10', 3, 2, 'Active'),
(210, 'REG_10', 'Student', '10', 'student10@college.edu', '9811000110', '2004-07-09', 'Male',   '2024-07-15', 4, 4, 'Active'),
(211, 'REG_11', 'Student', '11', 'student11@college.edu', '9811000111', '2003-05-14', 'Female', '2023-07-20', 5, 6, 'Active'),
(212, 'REG_12', 'Student', '12', 'student12@college.edu', '9811000112', '2004-10-22', 'Male',   '2024-07-15', 2, 4, 'Active'),
(213, 'REG_13', 'Student', '13', 'student13@college.edu', '9811000113', '2004-02-11', 'Female', '2024-07-15', 1, 4, 'Active'),
(214, 'REG_14', 'Student', '14', 'student14@college.edu', '9811000114', '2003-08-19', 'Male',   '2023-07-20', 2, 6, 'Active'),
(215, 'REG_15', 'Student', '15', 'student15@college.edu', '9811000115', '2005-01-30', 'Female', '2025-07-10', 3, 2, 'Active'),
(216, 'REG_16', 'Student', '16', 'student16@college.edu', '9811000116', '2004-05-14', 'Male',   '2024-07-15', 4, 4, 'Active'),
(217, 'REG_17', 'Student', '17', 'student17@college.edu', '9811000117', '2004-12-03', 'Female', '2024-07-15', 5, 4, 'Active'),
(218, 'REG_18', 'Student', '18', 'student18@college.edu', '9811000118', '2003-04-27', 'Male',   '2023-07-20', 1, 6, 'Active'),
(219, 'REG_19', 'Student', '19', 'student19@college.edu', '9811000119', '2005-09-16', 'Female', '2025-07-10', 2, 2, 'Active'),
(220, 'REG_20', 'Student', '20', 'student20@college.edu', '9811000120', '2004-11-25', 'Male',   '2024-07-15', 3, 4, 'Active');

-- 4. Courses (7 Courses)
INSERT INTO COURSE (course_id, course_code, course_title, credits, dept_id, course_level) VALUES
(301, 'CRS_01', 'Course 1', 4, 1, 'Intermediate'),
(302, 'CRS_02', 'Course 2', 4, 1, 'Introductory'),
(303, 'CRS_03', 'Course 3', 4, 2, 'Advanced'),
(304, 'CRS_04', 'Course 4', 3, 2, 'Intermediate'),
(305, 'CRS_05', 'Course 5', 3, 3, 'Intermediate'),
(306, 'CRS_06', 'Course 6', 4, 4, 'Intermediate'),
(307, 'CRS_07', 'Course 7', 3, 5, 'Intermediate');

-- 5. Course Offerings (7 Offerings)
INSERT INTO COURSE_OFFERING (offering_id, course_id, faculty_id, academic_year, semester, classroom, max_capacity, current_enrolled) VALUES
(401, 301, 101, '2025-2026', 4, 'Room 101', 60, 8),
(402, 302, 103, '2025-2026', 4, 'Room 102', 60, 5),
(403, 303, 102, '2025-2026', 4, 'Room 103', 50, 6),
(404, 304, 107, '2025-2026', 4, 'Room 104', 50, 0),
(405, 305, 104, '2025-2026', 6, 'Room 105', 55, 2),
(406, 306, 105, '2025-2026', 4, 'Room 106', 45, 2),
(407, 307, 106, '2025-2026', 6, 'Room 107', 40, 2);

-- 6. Enrollments (25 Enrollments)
INSERT INTO ENROLLMENT (enrollment_id, student_id, offering_id, enrollment_date, status) VALUES
(501, 201, 401, '2025-01-05', 'Completed'),
(502, 201, 403, '2025-01-06', 'Completed'),
(503, 202, 401, '2025-01-05', 'Completed'),
(504, 202, 402, '2025-01-05', 'Completed'),
(505, 203, 401, '2025-01-05', 'Completed'),
(506, 203, 403, '2025-01-06', 'Completed'),
(507, 204, 401, '2025-01-07', 'Completed'),
(508, 204, 402, '2025-01-07', 'Completed'),
(509, 205, 401, '2025-01-08', 'Completed'),
(510, 205, 403, '2025-01-08', 'Completed'),
(511, 206, 405, '2025-01-05', 'Completed'),
(512, 207, 406, '2025-01-06', 'Completed'),
(513, 208, 407, '2025-01-06', 'Completed'),
(514, 209, 402, '2025-01-07', 'Completed'),
(515, 210, 403, '2025-01-08', 'Completed'),
(516, 211, 407, '2025-01-08', 'Completed'),
(517, 212, 401, '2025-01-09', 'Completed'),
(518, 213, 401, '2025-01-09', 'Completed'),
(519, 214, 402, '2025-01-10', 'Completed'),
(520, 215, 403, '2025-01-10', 'Completed'),
(521, 216, 405, '2025-01-11', 'Completed'),
(522, 217, 406, '2025-01-11', 'Completed'),
(523, 218, 401, '2025-01-12', 'Completed'),
(524, 219, 402, '2025-01-12', 'Completed'),
(525, 220, 403, '2025-01-12', 'Completed');

-- 7. Exam Results (25 Records)
INSERT INTO EXAM_RESULT (result_id, enrollment_id, marks_obtained, grade, exam_date, remarks) VALUES
(601, 501, 94.50, 'S', '2025-05-10', 'Excellent performance'),
(602, 502, 88.00, 'A', '2025-05-12', 'Very good evaluation'),
(603, 503, 91.00, 'S', '2025-05-10', 'High score recorded'),
(604, 504, 82.50, 'A', '2025-05-14', 'Consistent coursework'),
(605, 505, 86.00, 'A', '2025-05-10', 'Solid understanding'),
(606, 506, 77.00, 'B', '2025-05-12', 'Good performance'),
(607, 507, 74.50, 'B', '2025-05-10', 'Satisfactory result'),
(608, 508, 66.00, 'C', '2025-05-14', 'Passing grade achieved'),
(609, 509, 96.00, 'S', '2025-05-10', 'Top performance in section'),
(610, 510, 92.50, 'S', '2025-05-12', 'Distinction achieved'),
(611, 511, 83.50, 'A', '2025-05-15', 'Very good practicals'),
(612, 512, 71.00, 'B', '2025-05-16', 'Good evaluation'),
(613, 513, 64.00, 'C', '2025-05-16', 'Satisfactory assessment'),
(614, 514, 88.50, 'A', '2025-05-17', 'Strong subject proficiency'),
(615, 515, 78.00, 'B', '2025-05-17', 'Good performance'),
(616, 516, 91.50, 'S', '2025-05-18', 'Exceptional standing'),
(617, 517, 79.00, 'B', '2025-05-18', 'Competent evaluation'),
(618, 518, 85.00, 'A', '2025-05-18', 'Consistent score'),
(619, 519, 72.00, 'B', '2025-05-19', 'Above average'),
(620, 520, 89.00, 'A', '2025-05-19', 'Very good answers'),
(621, 521, 68.00, 'C', '2025-05-20', 'Pass grade'),
(622, 522, 81.00, 'A', '2025-05-20', 'Good understanding'),
(623, 523, 93.00, 'S', '2025-05-21', 'High distinction'),
(624, 524, 76.50, 'B', '2025-05-21', 'Satisfactory performance'),
(625, 525, 87.00, 'A', '2025-05-21', 'Strong concepts');

-- 8. Fee Payments (25 Records)
INSERT INTO FEE_PAYMENT (payment_id, student_id, amount_paid, payment_date, payment_method, transaction_ref, payment_status) VALUES
(701, 201, 95000.00, '2024-07-20', 'Net Banking', 'TXN_01', 'Success'),
(702, 201, 95000.00, '2025-01-10', 'UPI',         'TXN_02', 'Success'),
(703, 202, 95000.00, '2024-07-22', 'Credit Card',  'TXN_03', 'Success'),
(704, 202, 95000.00, '2025-01-12', 'Net Banking', 'TXN_04', 'Success'),
(705, 203, 95000.00, '2024-07-21', 'UPI',         'TXN_05', 'Success'),
(706, 203, 95000.00, '2025-01-11', 'Debit Card',   'TXN_06', 'Success'),
(707, 204, 95000.00, '2024-07-25', 'Net Banking', 'TXN_07', 'Success'),
(708, 205, 95000.00, '2024-07-26', 'UPI',         'TXN_08', 'Success'),
(709, 206, 90000.00, '2024-08-01', 'Debit Card',   'TXN_09', 'Success'),
(710, 207, 95000.00, '2024-07-28', 'Credit Card',  'TXN_10', 'Success'),
(711, 208, 90000.00, '2024-08-05', 'UPI',         'TXN_11', 'Success'),
(712, 209, 98000.00, '2025-07-15', 'Net Banking', 'TXN_12', 'Success'),
(713, 210, 85000.00, '2024-07-29', 'UPI',         'TXN_13', 'Success'),
(714, 211, 95000.00, '2024-07-30', 'Net Banking', 'TXN_14', 'Success'),
(715, 212, 92000.00, '2024-08-02', 'Cash',        'TXN_15', 'Success'),
(716, 213, 95000.00, '2024-08-03', 'UPI',         'TXN_16', 'Success'),
(717, 214, 95000.00, '2024-08-04', 'Net Banking', 'TXN_17', 'Success'),
(718, 215, 95000.00, '2024-08-05', 'Debit Card',   'TXN_18', 'Success'),
(719, 216, 90000.00, '2024-08-06', 'Credit Card',  'TXN_19', 'Success'),
(720, 217, 95000.00, '2024-08-07', 'UPI',         'TXN_20', 'Success'),
(721, 218, 95000.00, '2024-08-08', 'Cash',        'TXN_21', 'Success'),
(722, 219, 95000.00, '2024-08-09', 'Net Banking', 'TXN_22', 'Success'),
(723, 220, 95000.00, '2024-08-10', 'UPI',         'TXN_23', 'Success'),
(724, 218, 95000.00, '2025-01-15', 'Net Banking', 'TXN_24', 'Success'),
(725, 220, 95000.00, '2025-01-16', 'UPI',         'TXN_25', 'Success');
