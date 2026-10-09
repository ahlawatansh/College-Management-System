# Relational Schema - College Management System

**Course:** BCSE302L – Database Systems  
**Faculty In-Charge:** Course Instructor  
**Team Details:**  
- Ansh (REG_01)  
- Student 2 (REG_02)  
- Student 3 (REG_03)  

---

## 1. Formal Relational Schema Specification

### 1. DEPARTMENT
```text
DEPARTMENT(
    dept_id: INTEGER [PK],
    dept_name: VARCHAR(100) [NOT NULL, UNIQUE],
    dept_code: VARCHAR(10) [NOT NULL, UNIQUE],
    building: VARCHAR(100) [NOT NULL],
    budget: DECIMAL(12, 2) [NOT NULL, CHECK (budget > 0)],
    established_year: INTEGER [NOT NULL, CHECK (established_year >= 1950 AND established_year <= 2026)]
)
```

### 2. FACULTY
```text
FACULTY(
    faculty_id: INTEGER [PK],
    first_name: VARCHAR(50) [NOT NULL],
    last_name: VARCHAR(50) [NOT NULL],
    email: VARCHAR(100) [NOT NULL, UNIQUE],
    phone: VARCHAR(15) [NOT NULL, UNIQUE],
    hire_date: DATE [NOT NULL],
    designation: VARCHAR(50) [NOT NULL, CHECK (designation IN ('Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer', 'Dean', 'HOD'))],
    salary: DECIMAL(10, 2) [NOT NULL, CHECK (salary >= 25000)],
    dept_id: INTEGER [FK -> DEPARTMENT(dept_id), NOT NULL]
)
```

### 3. STUDENT
```text
STUDENT(
    student_id: INTEGER [PK],
    reg_no: VARCHAR(20) [NOT NULL, UNIQUE],
    first_name: VARCHAR(50) [NOT NULL],
    last_name: VARCHAR(50) [NOT NULL],
    email: VARCHAR(100) [NOT NULL, UNIQUE],
    phone: VARCHAR(15) [NOT NULL, UNIQUE],
    date_of_birth: DATE [NOT NULL],
    gender: VARCHAR(10) [NOT NULL, CHECK (gender IN ('Male', 'Female', 'Other'))],
    admission_date: DATE [NOT NULL],
    dept_id: INTEGER [FK -> DEPARTMENT(dept_id), NOT NULL],
    current_semester: INTEGER [NOT NULL, DEFAULT 1, CHECK (current_semester BETWEEN 1 AND 8)],
    status: VARCHAR(15) [NOT NULL, DEFAULT 'Active', CHECK (status IN ('Active', 'Graduated', 'Suspended', 'Withdrawn'))]
)
```

### 4. COURSE
```text
COURSE(
    course_id: INTEGER [PK],
    course_code: VARCHAR(15) [NOT NULL, UNIQUE],
    course_title: VARCHAR(100) [NOT NULL],
    credits: INTEGER [NOT NULL, CHECK (credits BETWEEN 1 AND 6)],
    dept_id: INTEGER [FK -> DEPARTMENT(dept_id), NOT NULL],
    course_level: VARCHAR(20) [NOT NULL, CHECK (course_level IN ('Introductory', 'Intermediate', 'Advanced', 'Elective'))]
)
```

### 5. COURSE_OFFERING
```text
COURSE_OFFERING(
    offering_id: INTEGER [PK],
    course_id: INTEGER [FK -> COURSE(course_id), NOT NULL],
    faculty_id: INTEGER [FK -> FACULTY(faculty_id), NOT NULL],
    academic_year: VARCHAR(10) [NOT NULL],
    semester: INTEGER [NOT NULL, CHECK (semester BETWEEN 1 AND 8)],
    classroom: VARCHAR(50) [NOT NULL],
    max_capacity: INTEGER [NOT NULL, CHECK (max_capacity >= 10)],
    current_enrolled: INTEGER [NOT NULL, DEFAULT 0, CHECK (current_enrolled >= 0 AND current_enrolled <= max_capacity)],
    UNIQUE (course_id, faculty_id, academic_year, semester)
)
```

### 6. ENROLLMENT
```text
ENROLLMENT(
    enrollment_id: INTEGER [PK],
    student_id: INTEGER [FK -> STUDENT(student_id), NOT NULL],
    offering_id: INTEGER [FK -> COURSE_OFFERING(offering_id), NOT NULL],
    enrollment_date: DATE [NOT NULL, DEFAULT CURRENT_DATE],
    status: VARCHAR(15) [NOT NULL, DEFAULT 'Enrolled', CHECK (status IN ('Enrolled', 'Completed', 'Dropped'))],
    UNIQUE (student_id, offering_id)
)
```

### 7. EXAM_RESULT
```text
EXAM_RESULT(
    result_id: INTEGER [PK],
    enrollment_id: INTEGER [FK -> ENROLLMENT(enrollment_id), NOT NULL, UNIQUE],
    marks_obtained: DECIMAL(5, 2) [NOT NULL, CHECK (marks_obtained BETWEEN 0 AND 100)],
    grade: VARCHAR(2) [NOT NULL, CHECK (grade IN ('S', 'A', 'B', 'C', 'D', 'E', 'F'))],
    exam_date: DATE [NOT NULL, DEFAULT CURRENT_DATE],
    remarks: VARCHAR(100) [DEFAULT 'Regular Evaluation']
)
```

### 8. FEE_PAYMENT
```text
FEE_PAYMENT(
    payment_id: INTEGER [PK],
    student_id: INTEGER [FK -> STUDENT(student_id), NOT NULL],
    amount_paid: DECIMAL(10, 2) [NOT NULL, CHECK (amount_paid > 0)],
    payment_date: DATE [NOT NULL, DEFAULT CURRENT_DATE],
    payment_method: VARCHAR(20) [NOT NULL, CHECK (payment_method IN ('Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash'))],
    transaction_ref: VARCHAR(50) [NOT NULL, UNIQUE],
    payment_status: VARCHAR(15) [NOT NULL, DEFAULT 'Success', CHECK (payment_status IN ('Success', 'Pending', 'Failed'))]
)
```

---

## 2. Integrity Constraints Summary Table

| Table Name | Primary Key | Foreign Key(s) | Key Constraints |
| :--- | :--- | :--- | :--- |
| **DEPARTMENT** | `dept_id` | *None* | UNIQUE(`dept_name`, `dept_code`), CHECK(`budget` > 0) |
| **FACULTY** | `faculty_id` | `dept_id` → DEPARTMENT | UNIQUE(`email`, `phone`), CHECK(`salary` >= 25000, `designation`) |
| **STUDENT** | `student_id` | `dept_id` → DEPARTMENT | UNIQUE(`reg_no`, `email`, `phone`), CHECK(`gender`, `semester`, `status`) |
| **COURSE** | `course_id` | `dept_id` → DEPARTMENT | UNIQUE(`course_code`), CHECK(`credits` 1..6, `course_level`) |
| **COURSE_OFFERING** | `offering_id` | `course_id` → COURSE, `faculty_id` → FACULTY | UNIQUE(`course_id`, `faculty_id`, `year`, `semester`), CHECK(`capacity`) |
| **ENROLLMENT** | `enrollment_id` | `student_id` → STUDENT, `offering_id` → COURSE_OFFERING | UNIQUE(`student_id`, `offering_id`), CHECK(`status`) |
| **EXAM_RESULT** | `result_id` | `enrollment_id` → ENROLLMENT | UNIQUE(`enrollment_id`), CHECK(`marks` 0..100, `grade` S..F) |
| **FEE_PAYMENT** | `payment_id` | `student_id` → STUDENT | UNIQUE(`transaction_ref`), CHECK(`amount_paid` > 0, `method`, `status`) |

---

## 3. Normalization Analysis (BCNF / 3NF)
- **1NF Compliance:** All attributes are atomic (no repeating groups, no multi-valued attributes like multiple phone numbers in one field).
- **2NF Compliance:** All non-key attributes are fully functionally dependent on the entire primary key (no partial dependencies).
- **3NF & BCNF Compliance:** No transitive dependencies ($X \rightarrow Y$ where $Y \rightarrow Z$). Every determinant is a candidate key. Foreign keys cleanly reference independent entities without redundant denormalization.
