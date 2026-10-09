# Entity-Relationship (ER) Diagram - College Management System

**Course:** BCSE302L – Database Systems  
**Faculty In-Charge:** Course Instructor  
**Team Details:**  
- Ansh (REG_01)  
- Student 2 (REG_02)  
- Student 3 (REG_03)  

---

## 1. Visual Entity-Relationship Architecture

![College Management System ER Diagram](file:///Users/ansh/Desktop/College/DBMS%20project/college-management-system/diagrams/er_diagram.jpg)

---

## 2. Mermaid Relational ER Model

```mermaid
erDiagram
    DEPARTMENT ||--o{ FACULTY : "employs"
    DEPARTMENT ||--o{ STUDENT : "enrolls"
    DEPARTMENT ||--o{ COURSE : "curates"
    
    FACULTY ||--o{ COURSE_OFFERING : "instructs"
    COURSE ||--o{ COURSE_OFFERING : "instantiated_as"
    
    STUDENT ||--o{ ENROLLMENT : "registers_for"
    COURSE_OFFERING ||--o{ ENROLLMENT : "receives"
    
    ENROLLMENT ||--o| EXAM_RESULT : "evaluated_with"
    STUDENT ||--o{ FEE_PAYMENT : "remits"

    DEPARTMENT {
        int dept_id PK
        string dept_name "UNIQUE"
        string dept_code "UNIQUE"
        string building
        decimal budget "CHECK > 0"
        int established_year
    }

    FACULTY {
        int faculty_id PK
        string first_name
        string last_name
        string email "UNIQUE"
        string phone "UNIQUE"
        date hire_date
        string designation
        decimal salary "CHECK >= 25000"
        int dept_id FK
    }

    STUDENT {
        int student_id PK
        string reg_no "UNIQUE"
        string first_name
        string last_name
        string email "UNIQUE"
        string phone "UNIQUE"
        date date_of_birth
        string gender
        date admission_date
        int dept_id FK
        int current_semester "CHECK 1..8"
        string status
    }

    COURSE {
        int course_id PK
        string course_code "UNIQUE"
        string course_title
        int credits "CHECK 1..6"
        int dept_id FK
        string course_level
    }

    COURSE_OFFERING {
        int offering_id PK
        int course_id FK
        int faculty_id FK
        string academic_year
        int semester "CHECK 1..8"
        string classroom
        int max_capacity "CHECK >= 10"
        int current_enrolled
    }

    ENROLLMENT {
        int enrollment_id PK
        int student_id FK
        int offering_id FK
        date enrollment_date
        string status
    }

    EXAM_RESULT {
        int result_id PK
        int enrollment_id FK "UNIQUE"
        decimal marks_obtained "CHECK 0..100"
        string grade
        date exam_date
        string remarks
    }

    FEE_PAYMENT {
        int payment_id PK
        int student_id FK
        decimal amount_paid "CHECK > 0"
        date payment_date
        string payment_method
        string transaction_ref "UNIQUE"
        string payment_status
    }
```

---

## 3. Detailed Entity and Cardinality Justifications

1. **DEPARTMENT to STUDENT (1 : N)**:
   - *Rationale:* Every student is formally enrolled in exactly one parent degree department (`dept_id`). One department admits hundreds of students.
2. **DEPARTMENT to FACULTY (1 : N)**:
   - *Rationale:* Every faculty member is appointed to a primary academic department. A department employs multiple faculty members.
3. **DEPARTMENT to COURSE (1 : N)**:
   - *Rationale:* Courses belong to a curriculum board maintained by a department. A department creates many distinct courses.
4. **COURSE & FACULTY to COURSE_OFFERING (M : N resolved via Ternary/Associative Section)**:
   - *Rationale:* A course can be taught multiple times across semesters by different faculty. A faculty member teaches multiple courses. `COURSE_OFFERING` acts as the associative entity capturing venue, term, and capacity.
5. **STUDENT & COURSE_OFFERING to ENROLLMENT (M : N resolved)**:
   - *Rationale:* A student registers for multiple course offerings per term; a course offering section enrolls multiple students. Resolved via `ENROLLMENT` with a candidate key on `(student_id, offering_id)`.
6. **ENROLLMENT to EXAM_RESULT (1 : 1)**:
   - *Rationale:* Each student enrollment produces exactly one official semester final exam evaluation and letter grade.
7. **STUDENT to FEE_PAYMENT (1 : N)**:
   - *Rationale:* A student makes multiple periodic fee remittances (semester tuition, lab fees, installments) over their academic degree tenure.
