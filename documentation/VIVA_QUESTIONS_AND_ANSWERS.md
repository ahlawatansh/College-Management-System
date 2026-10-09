# BCSE302L DBMS Project - Viva Questions and Answers
# COLLEGE MANAGEMENT SYSTEM

**Faculty In-Charge:** Course Instructor  
**Team Members:** Project Team  

---

## Part 1: Review I – ER Modeling, Normalization & Relational Schema

### Q1: What is the primary difference between Conceptual Schema (ER Model) and Relational Schema?
**Answer:**  
The **ER Model** is a high-level conceptual data model that uses entities, attributes, and relationships (represented diagrammatically via rectangles, ellipses, and diamonds) to represent real-world objects without considering physical storage details.  
The **Relational Schema** is a logical data model derived from the ER diagram that maps entities and relationships into two-dimensional tables (relations) with column names, primary keys, foreign keys, and domain constraints.

### Q2: Why are there exactly 8 tables in your design? Can any table be merged?
**Answer:**  
No table should be merged without violating normalization:
- Merging `COURSE` and `COURSE_OFFERING` would repeat course credits and titles for every semester section (violating 2NF/3NF).
- Merging `STUDENT` and `ENROLLMENT` would create multi-valued attributes since a student takes multiple courses (violating 1NF).
- Merging `ENROLLMENT` and `EXAM_RESULT` would cause insertion anomalies if grades are entered later in the semester.
Thus, 8 tables is the optimal normalized design for this domain.

### Q3: What normal form does your database achieve? Prove it.
**Answer:**  
Our database achieves **Boyce-Codd Normal Form (BCNF)** and **Third Normal Form (3NF)**:
1. **1NF:** Every column contains atomic values. No repeating groups.
2. **2NF:** All non-key attributes are fully functionally dependent on the entire primary key (we use single-attribute surrogate keys like `student_id`, eliminating partial dependency).
3. **3NF & BCNF:** In every non-trivial functional dependency $X \to Y$, the determinant $X$ is a superkey. There are no transitive dependencies ($X \to Y \to Z$). Candidate keys (such as `reg_no`, `course_code`, and `(student_id, offering_id)`) are guarded by `UNIQUE` constraints.

### Q4: Explain the cardinality between STUDENT and COURSE_OFFERING.
**Answer:**  
It is a **Many-to-Many ($M:N$)** relationship. A student registers for multiple course offerings (typically 4–6 per term), and a course offering section accommodates multiple students (e.g., 60 students). It is resolved in the relational model using the associative table `ENROLLMENT`, where the combination `(student_id, offering_id)` is defined as `UNIQUE`.

### Q5: What is the purpose of the ON DELETE CASCADE and ON DELETE RESTRICT clauses in your foreign keys?
**Answer:**  
- **ON DELETE RESTRICT** (e.g., in `FACULTY.dept_id -> DEPARTMENT.dept_id` and `STUDENT.dept_id -> DEPARTMENT.dept_id`): Prevents accidental deletion of a department if students or faculty members are still assigned to it.
- **ON DELETE CASCADE** (e.g., in `ENROLLMENT.student_id -> STUDENT.student_id`): Ensures that if a student record is legally expunged, their corresponding enrollments, exam results, and fee payment entries are automatically removed, preventing orphaned records.

---

## Part 2: Review II – SQL Queries, DDL, DML & Constraints

### Q6: What is the difference between a Correlated Subquery and a Regular Nested Subquery?
**Answer:**  
- In a **regular nested subquery** (e.g., Query 9 finding `MAX(marks_obtained)`), the inner query executes once independently and passes its result to the outer query.
- In a **correlated subquery** (e.g., Query 10 finding students scoring above their course average), the inner query references columns from the outer query (`inner_co.course_id = c.course_id`). The inner query executes repeatedly—once for each row processed by the outer query.

### Q7: Explain the difference between WHERE and HAVING in SQL.
**Answer:**  
- The `WHERE` clause filters individual rows *before* grouping occurs and cannot be used with aggregate functions directly.
- The `HAVING` clause filters groups *after* the `GROUP BY` operation has aggregated rows (e.g., `GROUP BY dept_id HAVING COUNT(student_id) >= 2`).

### Q8: What is the difference between an INNER JOIN and a LEFT OUTER JOIN? Where did you use LEFT JOIN?
**Answer:**  
- **INNER JOIN** returns rows only when there is a match in both tables.
- **LEFT OUTER JOIN** returns all rows from the left table, and the matched rows from the right table. If there is no match, the right side returns `NULL`.
- *Application:* We used `LEFT JOIN` in **Query 13** (`STUDENT LEFT JOIN FEE_PAYMENT`) so that students who have made zero payments are still included with `NULL` (handled via `COALESCE(SUM(amount_paid), 0)`) rather than being excluded from the dues report.

### Q9: What CHECK constraints did you implement?
**Answer:**  
1. `DEPARTMENT`: `budget > 0`, `established_year BETWEEN 1950 AND 2026`.
2. `FACULTY`: `salary >= 25000`, `designation IN ('Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer', 'Dean', 'HOD')`.
3. `STUDENT`: `gender IN ('Male', 'Female', 'Other')`, `current_semester BETWEEN 1 AND 8`, `status IN ('Active', 'Graduated', 'Suspended', 'Withdrawn')`.
4. `COURSE`: `credits BETWEEN 1 AND 6`, `course_level IN ('Introductory', 'Intermediate', 'Advanced', 'Elective')`.
5. `COURSE_OFFERING`: `max_capacity >= 10`, `current_enrolled >= 0 AND current_enrolled <= max_capacity`.
6. `ENROLLMENT`: `status IN ('Enrolled', 'Completed', 'Dropped')`.
7. `EXAM_RESULT`: `marks_obtained BETWEEN 0 AND 100`, `grade IN ('S', 'A', 'B', 'C', 'D', 'E', 'F')`.
8. `FEE_PAYMENT`: `amount_paid > 0`, `payment_method IN ('Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash')`, `payment_status IN ('Success', 'Pending', 'Failed')`.

---

## Part 3: Review III – Procedures, Functions, Cursor, Triggers & Transactions

### Q10: What is the fundamental difference between a Stored Procedure and a Stored Function?
**Answer:**  
- A **Stored Procedure** is intended to execute a business transaction (DML operations like INSERT, UPDATE, DELETE). It does not need to return a value, but can return multiple values via `OUT` parameters. It cannot be directly called inside a SQL `SELECT` expression.
- A **Stored Function** must return a single deterministic value via the `RETURN` statement. It is typically side-effect free and can be called directly within a SQL `SELECT` or `WHERE` clause (e.g., `SELECT Calculate_Student_GPA_Func(student_id) FROM STUDENT`).

### Q11: Explain your course enrollment procedure (`Enroll_Student_Proc`).
**Answer:**  
The procedure takes `student_id` and `offering_id` as input:
1. Validates that the student exists and is `Active`.
2. Validates that the course offering exists.
3. Checks if the student is already registered to prevent duplicates.
4. Checks if `current_enrolled < max_capacity` to prevent class overflow.
5. Generates the new `enrollment_id` and inserts into `ENROLLMENT`.
6. Increments `COURSE_OFFERING.current_enrolled` by 1.
7. Commits the transaction and outputs confirmation.

### Q12: How does your explicit cursor work? Why is a cursor necessary here?
**Answer:**  
A cursor is a private work area in memory used to handle queries that return multiple rows. Our procedure `Generate_Academic_Report_Cursor`:
1. `DECLARE cur_student_summary CURSOR FOR SELECT ...`
2. `OPEN cur_student_summary;`
3. `LOOP` $\to$ `FETCH cur_student_summary INTO ...;` $\to$ `EXIT WHEN %NOTFOUND;`
4. Processes each row conditionally (classifies honors standing: Dean's List for $\ge 90\%$, First Class for $\ge 75\%$, Warning for $< 50\%$).
5. `CLOSE cur_student_summary;`
A cursor is necessary because individual SQL `SELECT` statements cannot execute row-by-row procedural branch logic across multi-record datasets.

### Q13: What triggers did you implement and why?
**Answer:**  
1. **`trg_enrollment_seat_increment` (AFTER INSERT ON ENROLLMENT):**  
   Automatically increments `current_enrolled` in `COURSE_OFFERING` whenever an enrollment row is inserted, keeping the seat count synchronized.
2. **`trg_auto_compute_grade` (BEFORE INSERT OR UPDATE ON EXAM_RESULT):**  
   Validates that marks are between 0 and 100, and automatically computes the letter grade ('S' for $\ge 90$, 'A' for $\ge 80$, etc.), preventing human grading discrepancies.
3. **`trg_prevent_over_enrollment` (BEFORE INSERT ON ENROLLMENT):**  
   Acts as a database-level firewall to abort any insert if `current_enrolled >= max_capacity`.

### Q14: Explain the 5 major real-world transactions in your application.
**Answer:**  
1. **Student Registration:** Form input $\to$ `INSERT INTO STUDENT` $\to$ Unique ID and Reg No assigned $\to$ Confirmation.
2. **Course Enrollment:** Student ID + Section ID $\to$ `Enroll_Student_Proc` $\to$ Capacity validated $\to$ `ENROLLMENT` inserted $\to$ Offering seats updated $\to$ Status displayed.
3. **Examination Grading:** Enrollment ID + Score $\to$ `Record_Exam_Result_Proc` $\to$ Grade auto-assigned $\to$ Enrollment marked 'Completed' $\to$ Transcript updated.
4. **Fee Payment Processing:** Student ID + Amount + Method $\to$ `Process_Fee_Payment_Proc` $\to$ Bank reference checked $\to$ `FEE_PAYMENT` inserted $\to$ Outstanding dues reduced.
5. **Academic Audit Generation:** Audit request $\to$ Explicit Cursor executes across all departments $\to$ CGPA and honors computed $\to$ Multi-student institutional report printed.
