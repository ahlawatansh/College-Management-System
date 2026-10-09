# BCSE302L – Database Systems: Review II Implementation Report
# COLLEGE MANAGEMENT SYSTEM

**Institution:** School of Computer Science and Engineering, Vellore Institute of Technology  
**Course Code & Title:** BCSE302L – Database Systems  
**Faculty In-Charge:** Course Instructor  

### Project Team Details:
| Student Name | Registration Number | Specialization | Role & Review II Focus |
| :--- | :--- | :--- | :--- |
| **Ansh** | **REG_01** | B.Tech Data Engineering | DDL Table Creation, Constraints & Referential Cascades |
| **Student 2** | **REG_02** | B.Tech Computer Science | Stored Procedures, Functions, Cursor & Reactive Triggers |
| **Student 3** | **REG_03** | B.Tech Data Engineering | DML Population (80+ records), Complex Analytical SQL Queries |

---

## 1. Review II Implementation Overview

In accordance with BCSE302L guidelines, Review II demonstrates the complete implementation of:
1. **DDL Architecture:** 8 normalized tables with comprehensive Primary Keys, Foreign Keys, NOT NULL, UNIQUE, CHECK, and DEFAULT constraints.
2. **DML Population:** Over 80 realistic institutional records (>= 10 records per table) without dummy placeholders.
3. **Complex SQL Querying:** 16 tested analytical queries covering Joins, Group By, Having, Aggregations, Correlated Subqueries, and Nested Sets.
4. **PL/SQL Stored Procedures:** Core application business procedures with parameter validation and exception handling.
5. **PL/SQL Functions:** Pure computational functions for GPA calculation and pending fee balances.
6. **PL/SQL Cursor:** Multi-row iterative processing generating institutional academic audit reports.
7. **PL/SQL Reactive Triggers:** Automatic seat capacity updates and automated grade classification.
8. **DML Demonstrations:** Live execution of INSERT, UPDATE, and DELETE operations.

---

## 2. Table Creation (DDL) and Integrity Constraints

The complete DDL script (`01_create_tables.sql`) enforces relational integrity across all 8 tables:

### Constraint Matrix

| Table Name | PK | FK Dependencies | NOT NULL | UNIQUE | CHECK Constraints | DEFAULT Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DEPARTMENT** | `dept_id` | *None* | 4 cols | `dept_name`, `dept_code` | `budget > 0`, `year 1950..2026` | - |
| **FACULTY** | `faculty_id` | `dept_id` → DEPARTMENT | 8 cols | `email`, `phone` | `salary >= 25000`, `designation` | - |
| **STUDENT** | `student_id` | `dept_id` → DEPARTMENT | 10 cols | `reg_no`, `email`, `phone` | `gender`, `sem 1..8`, `status` | `sem=1`, `status='Active'` |
| **COURSE** | `course_id` | `dept_id` → DEPARTMENT | 5 cols | `course_code` | `credits 1..6`, `course_level` | - |
| **COURSE_OFFERING** | `offering_id` | `course_id` → COURSE<br>`faculty_id` → FACULTY | 7 cols | `(course, faculty, year, sem)` | `capacity >= 10`, `enrolled <= capacity` | `current_enrolled = 0` |
| **ENROLLMENT** | `enrollment_id` | `student_id` → STUDENT<br>`offering_id` → OFFERING | 4 cols | `(student_id, offering_id)` | `status IN ('Enrolled','Completed','Dropped')` | `status='Enrolled'`, `date=CURRENT_DATE` |
| **EXAM_RESULT** | `result_id` | `enrollment_id` → ENROLLMENT | 4 cols | `enrollment_id` | `marks BETWEEN 0 AND 100`, `grade IN ('S'..'F')` | `date=CURRENT_DATE`, `remarks='Regular'` |
| **FEE_PAYMENT** | `payment_id` | `student_id` → STUDENT | 6 cols | `transaction_ref` | `amount_paid > 0`, `method`, `status` | `date=CURRENT_DATE`, `status='Success'` |

---

## 3. Data Population Verification (DML)

All 8 tables were populated with authentic college data (`02_insert_data.sql`):
- `DEPARTMENT`: 10 records (CSE, DSAI, IT, ECE, MECH, EEE, CIVIL, BIO, MGMT, MATH)
- `FACULTY`: 10 records (Course Instructor, Dr. Sangeetha Kumar, Dr. Arun Sundaram, etc.)
- `STUDENT`: 12 records (including team members: Ansh REG_01, Student 2 REG_02, Student 3 REG_03)
- `COURSE`: 10 records (BCSE302L, BCSE201L, BDSE301L, BDSE202L, etc.)
- `COURSE_OFFERING`: 10 scheduled term sections
- `ENROLLMENT`: 15 registered student-section records
- `EXAM_RESULT`: 12 evaluated course grades
- `FEE_PAYMENT`: 12 verified tuition payment transactions

---

## 4. Complex SQL Queries and Executed Outputs

Below are 6 highlighted queries from the 16 executed queries in `03_queries.sql`:

### Query 6: Course-Wise Grade Statistics (Aggregations & GROUP BY)
```sql
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
```
**Output:**
```
course_code | course_title                   | total_graded | avg_marks | lowest_marks | highest_marks
------------+--------------------------------+--------------+-----------+--------------+--------------
BCSE302L    | Database Systems               | 5            | 90.50     | 78.00        | 96.00
BDSE301L    | Machine Learning Foundations   | 3            | 87.83     | 86.00        | 89.50
BCSE201L    | Data Structures and Algorithms | 2            | 84.00     | 82.50        | 85.50
BIT3002     | Web Technologies & App         | 1            | 80.00     | 80.00        | 80.00
BECE203L    | Digital Signal Processing      | 1            | 75.00     | 75.00        | 75.00
```

### Query 9: Highest-Scoring Student (Nested Subquery with MAX)
```sql
SELECT s.reg_no, s.first_name || ' ' || s.last_name AS student_name,
       c.course_code, er.marks_obtained, er.grade, er.remarks
FROM EXAM_RESULT er
INNER JOIN ENROLLMENT e ON er.enrollment_id = e.enrollment_id
INNER JOIN STUDENT s ON e.student_id = s.student_id
INNER JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
INNER JOIN COURSE c ON co.course_id = c.course_id
WHERE er.marks_obtained = (SELECT MAX(marks_obtained) FROM EXAM_RESULT);
```
**Output:**
```
reg_no    | student_name   | course_code | marks_obtained | grade | remarks
----------+----------------+-------------+----------------+-------+----------------------------------------
REG_03 | Student 3 | BCSE302L    | 96.00          | S     | Highest score in Database Systems class
```

### Query 10: Correlated Subquery (Above Course Average)
```sql
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
```
**Output:**
```
reg_no    | student_name     | course_code | marks_obtained
----------+------------------+-------------+---------------
REG_03 | Student 3   | BCSE302L    | 96.00
REG_01 | Student 1     | BCSE302L    | 94.50
24BCE0215 | Sneha Iyer       | BCSE302L    | 93.00
REG_02 | Student 2 | BCSE302L    | 91.00
REG_03 | Student 3   | BDSE301L    | 89.50
REG_01 | Student 1     | BDSE301L    | 88.00
REG_02 | Student 2 | BCSE201L    | 85.50
```

---

## 5. PL/SQL Components Summary

### 5.1 Stored Procedures
1. **`Enroll_Student_Proc(student_id, offering_id)`:** Performs 4 validation checkpoints (active student check, offering existence, duplicate enrollment, and seat availability) before inserting the enrollment record and automatically incrementing `current_enrolled`.
2. **`Process_Fee_Payment_Proc(student_id, amount, method, txn_ref)`:** Validates student ID and positive amount, checks for duplicate transaction references, inserts the payment record, and returns a verified payment receipt.
3. **`Record_Exam_Result_Proc(enrollment_id, marks, remarks)`:** Validates score (0–100), computes the appropriate letter grade ('S' through 'F'), and updates the `EXAM_RESULT` table.

### 5.2 Stored Functions
1. **`Calculate_Student_GPA_Func(student_id)`:** Traverses student's completed courses, maps letter grades to numerical points (S=10, A=9, B=8, C=7, D=6, E=5, F=0), and computes the credit-weighted Cumulative GPA.
2. **`Calculate_Pending_Fee_Func(student_id)`:** Queries `FEE_PAYMENT`, sums successful remittances, and deducts from the annual institutional fee (INR 190,000) to return pending dues.

### 5.3 Explicit Cursor
- **`Generate_Academic_Report_Cursor`:** Declares explicit cursor `cur_student_summary`, loops through student records using `FETCH ... INTO`, evaluates honors standings (Dean's List / First Class / Academic Warning), and prints a comprehensive academic audit.

### 5.4 Reactive Triggers
- **`trg_enrollment_seat_increment` (AFTER INSERT ON ENROLLMENT):** Increments `COURSE_OFFERING.current_enrolled`.
- **`trg_auto_compute_grade` (BEFORE INSERT OR UPDATE ON EXAM_RESULT):** Automatically validates marks and assigns letter grades.
- **`trg_prevent_over_enrollment` (BEFORE INSERT ON ENROLLMENT):** Aborts enrollment if section capacity is exceeded.
