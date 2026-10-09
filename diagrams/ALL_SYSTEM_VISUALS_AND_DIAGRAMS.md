# College Management System - Complete System Visuals & Diagrams
### Course: BCSE302L – Database Systems | Faculty: Course Instructor
### Team: Project Team

---

## Visual 1: Full Relational Entity-Relationship (ER) Diagram (Crow's Foot)

```mermaid
erDiagram
    DEPARTMENT ||--o{ FACULTY : "employs (1:N)"
    DEPARTMENT ||--o{ STUDENT : "enrolls (1:N)"
    DEPARTMENT ||--o{ COURSE : "curates (1:N)"
    
    FACULTY ||--o{ COURSE_OFFERING : "instructs (1:N)"
    COURSE ||--o{ COURSE_OFFERING : "instantiated_as (1:N)"
    
    STUDENT ||--o{ ENROLLMENT : "registers_for (1:N)"
    COURSE_OFFERING ||--o{ ENROLLMENT : "receives (1:N)"
    
    ENROLLMENT ||--o| EXAM_RESULT : "evaluated_with (1:1)"
    STUDENT ||--o{ FEE_PAYMENT : "remits (1:N)"

    DEPARTMENT {
        int dept_id PK
        string dept_name "UNIQUE, NOT NULL"
        string dept_code "UNIQUE, NOT NULL"
        string building "NOT NULL"
        decimal budget "CHECK > 0"
        int established_year "CHECK 1950..2026"
    }

    FACULTY {
        int faculty_id PK
        string first_name "NOT NULL"
        string last_name "NOT NULL"
        string email "UNIQUE, NOT NULL"
        string phone "UNIQUE, NOT NULL"
        date hire_date "NOT NULL"
        string designation "CHECK ('Professor'..)"
        decimal salary "CHECK >= 25000"
        int dept_id FK "REFERENCES DEPARTMENT"
    }

    STUDENT {
        int student_id PK
        string reg_no "UNIQUE, NOT NULL"
        string first_name "NOT NULL"
        string last_name "NOT NULL"
        string email "UNIQUE, NOT NULL"
        string phone "UNIQUE, NOT NULL"
        date date_of_birth "NOT NULL"
        string gender "CHECK ('Male','Female','Other')"
        date admission_date "NOT NULL"
        int dept_id FK "REFERENCES DEPARTMENT"
        int current_semester "CHECK 1..8, DEFAULT 1"
        string status "CHECK ('Active'..), DEFAULT 'Active'"
    }

    COURSE {
        int course_id PK
        string course_code "UNIQUE, NOT NULL"
        string course_title "NOT NULL"
        int credits "CHECK 1..6"
        int dept_id FK "REFERENCES DEPARTMENT"
        string course_level "CHECK ('Introductory'..)"
    }

    COURSE_OFFERING {
        int offering_id PK
        int course_id FK "REFERENCES COURSE"
        int faculty_id FK "REFERENCES FACULTY"
        string academic_year "NOT NULL"
        int semester "CHECK 1..8"
        string classroom "NOT NULL"
        int max_capacity "CHECK >= 10"
        int current_enrolled "DEFAULT 0, CHECK <= capacity"
    }

    ENROLLMENT {
        int enrollment_id PK
        int student_id FK "REFERENCES STUDENT"
        int offering_id FK "REFERENCES COURSE_OFFERING"
        date enrollment_date "DEFAULT CURRENT_DATE"
        string status "CHECK ('Enrolled','Completed','Dropped')"
    }

    EXAM_RESULT {
        int result_id PK
        int enrollment_id FK "UNIQUE, REFERENCES ENROLLMENT"
        decimal marks_obtained "CHECK 0..100"
        string grade "CHECK ('S','A','B','C','D','E','F')"
        date exam_date "DEFAULT CURRENT_DATE"
        string remarks "DEFAULT 'Regular Evaluation'"
    }

    FEE_PAYMENT {
        int payment_id PK
        int student_id FK "REFERENCES STUDENT"
        decimal amount_paid "CHECK > 0"
        date payment_date "DEFAULT CURRENT_DATE"
        string payment_method "CHECK ('UPI','Net Banking'..)"
        string transaction_ref "UNIQUE, NOT NULL"
        string payment_status "CHECK ('Success','Pending','Failed')"
    }
```

---

## Visual 2: Relational Schema Dependency & Foreign Key Linkage Map

```
┌────────────────────────────────────────────────────────────────────────┐
│                          DEPARTMENT (Root)                             │
│                  PK: dept_id | UQ: dept_code, dept_name                │
└──────────────┬─────────────────────────┬───────────────────────────────┘
               │ (1:N RESTRICT)          │ (1:N RESTRICT)                │ (1:N RESTRICT)
               ▼                         ▼                               ▼
       ┌───────────────┐         ┌───────────────┐               ┌───────────────┐
       │    FACULTY    │         │    STUDENT    │               │    COURSE     │
       │ PK: faculty_id│         │ PK: student_id│               │ PK: course_id │
       │ FK: dept_id   │         │ FK: dept_id   │               │ FK: dept_id   │
       └───────┬───────┘         └───────┬───────┘               └───────┬───────┘
               │ (1:N RESTRICT)          │                               │ (1:N CASCADE)
               │                         │                               │
               └───────────┐             │             ┌─────────────────┘
                           ▼             │             ▼
                 ┌───────────────────────────────────────┐
                 │            COURSE_OFFERING            │
                 │ PK: offering_id                       │
                 │ FK: course_id, faculty_id             │
                 │ UQ: (course, faculty, year, sem)      │
                 └───────────────────┬───────────────────┘
                                     │ (1:N CASCADE)
                                     ▼
                           ┌───────────────────┐
                           │    ENROLLMENT     │ <── (1:N CASCADE from STUDENT)
                           │ PK: enrollment_id │
                           │ FK: student_id    │
                           │ FK: offering_id   │
                           │ UQ: (student, off)│
                           └─────────┬─────────┘
                                     │ (1:1 CASCADE)
                                     ▼
                           ┌───────────────────┐                 ┌───────────────────┐
                           │    EXAM_RESULT    │                 │    FEE_PAYMENT    │
                           │ PK: result_id     │                 │ PK: payment_id    │
                           │ FK: enrollment_id │                 │ FK: student_id    │ <── (1:N CASCADE)
                           └───────────────────┘                 └───────────────────┘
```

---

## Visual 3: 5-Tier Closed-Loop System Architecture

```mermaid
flowchart TD
    subgraph T1["Tier 1: Presentation Layer"]
        UI1["Web Dashboard (Localhost:5001)"]
        UI2["CLI Interactive Console (app.py)"]
        UI3["1-Click Demo Runner (demo_runner.py)"]
    end

    subgraph T2["Tier 2: Application API Bridge"]
        SVR["Flask Server (server.py)"]
        MGR["Database Manager (db_manager.py)"]
        QR["Query Runner (query_runner.py)"]
    end

    subgraph T3["Tier 3: Procedural Database Logic"]
        P1["Enroll_Student_Proc"]
        P2["Process_Fee_Payment_Proc"]
        P3["Record_Exam_Result_Proc"]
        F1["Calculate_Student_GPA_Func"]
        F2["Calculate_Pending_Fee_Func"]
        C1["Generate_Academic_Report_Cursor"]
        TR1["trg_enrollment_seat_increment"]
        TR2["trg_auto_compute_grade"]
    end

    subgraph T4["Tier 4: Relational Engine & Integrity Firewall"]
        FK["Referential Actions (CASCADE / RESTRICT)"]
        CHK["Domain Check Constraints"]
        UQ["Unique Candidate Keys"]
        ACID["ACID Transaction Journal"]
    end

    subgraph T5["Tier 5: Physical Storage"]
        DB["college_cms.db (Tables, Indexes, WAL)"]
    end

    T1 -->|HTTP JSON / Stdin| T2
    T2 -->|Execute Procedure / SQL| T3
    T3 -->|Atomic DDL/DML| T4
    T4 -->|B-Tree Writes / Read| T5
```

---

## Visual 4: Data Flow Diagram (DFD Level 0 Context & Level 1)

### DFD Level 0 (Context Diagram)
```mermaid
flowchart LR
    S[Student Actor] <-->|Registration Requests / Transcripts & Receipts| CMS((0.0 College Management System))
    F[Faculty Actor] <-->|Class Rosters / Evaluation Marks| CMS
    D[Dean / HOD] <-->|Curriculum Approvals / Academic Audit Reports| CMS
    A[Finance Office] <-->|Fee Remittances / Revenue Breakdown| CMS
```

### DFD Level 1 (Operational Decomposition)
```mermaid
flowchart TD
    S[Student] -->|Admissions Application| P1((1.0 Student Admissions))
    P1 -->|Store Record| D1[(D1: STUDENT)]
    P1 -->|Fetch Dept Info| D2[(D2: DEPARTMENT)]

    HOD[Dean / HOD] -->|Define Curriculum| P2((2.0 Course & Section Scheduling))
    P2 -->|Catalog Items| D4[(D4: COURSE)]
    P2 -->|Section Quota| D5[(D5: COURSE_OFFERING)]
    P2 -->|Instructor Assignment| D3[(D3: FACULTY)]

    S -->|Enrollment Request| P3((3.0 Registration & Capacity Control))
    P3 -->|Validate Seat Ceiling| D5
    P3 -->|Log Registration| D6[(D6: ENROLLMENT)]

    FAC[Faculty] -->|Enter Evaluation Score| P4((4.0 Continuous Grading))
    P4 -->|Trigger Auto-Grade| D7[(D7: EXAM_RESULT)]
    D7 -->|Mark Complete| D6

    S -->|Pay Tuition| P5((5.0 Fee Reconciliation))
    P5 -->|Log Transaction Voucher| D8[(D8: FEE_PAYMENT)]
```

---

## Visual 5: Normalization Functional Dependency Graph (BCNF Proof)

```
1. DEPARTMENT:
   dept_id [Superkey] ──> {dept_name, dept_code, building, budget, established_year}
   dept_name [Candidate Key] ──> {dept_id, dept_code, ...}
   dept_code [Candidate Key] ──> {dept_id, dept_name, ...}

2. FACULTY:
   faculty_id [Superkey] ──> {first_name, last_name, email, phone, hire_date, designation, salary, dept_id}
   email, phone [Candidate Keys] ──> {faculty_id, ...}

3. STUDENT:
   student_id [Superkey] ──> {reg_no, first_name, last_name, email, phone, dob, gender, admission_date, dept_id, sem, status}
   reg_no, email, phone [Candidate Keys] ──> {student_id, ...}

4. COURSE:
   course_id [Superkey] ──> {course_code, course_title, credits, dept_id, course_level}
   course_code [Candidate Key] ──> {course_id, ...}

5. COURSE_OFFERING:
   offering_id [Superkey] ──> {course_id, faculty_id, academic_year, semester, classroom, max_capacity, current_enrolled}
   (course_id, faculty_id, academic_year, semester) [Candidate Key] ──> {offering_id, ...}

6. ENROLLMENT:
   enrollment_id [Superkey] ──> {student_id, offering_id, enrollment_date, status}
   (student_id, offering_id) [Candidate Key] ──> {enrollment_id, ...}

7. EXAM_RESULT:
   result_id [Superkey] ──> {enrollment_id, marks_obtained, grade, exam_date, remarks}
   enrollment_id [Candidate Key (1:1)] ──> {result_id, ...}

8. FEE_PAYMENT:
   payment_id [Superkey] ──> {student_id, amount_paid, payment_date, payment_method, transaction_ref, payment_status}
   transaction_ref [Candidate Key] ──> {payment_id, ...}

Conclusion:
In every functional dependency X -> Y across all 8 tables, X is a SUPERKEY.
Therefore, the database is strictly in BOYCE-CODD NORMAL FORM (BCNF) and 3NF.
```

---

## Visual 6: State Transition Lifecycle Statecharts

### 1. Enrollment Lifecycle
```mermaid
stateDiagram-v2
    [*] --> Submitted : Student selects offering_id
    Submitted --> Validating : Check active status & capacity
    Validating --> Rejected : Capacity full OR duplicate
    Rejected --> [*]
    Validating --> Enrolled : Available seats exist
    Enrolled --> Completed : Final exam marks recorded
    Enrolled --> Dropped : Voluntary course drop
    Completed --> [*]
    Dropped --> [*]
```

### 2. Examination Evaluation Lifecycle
```mermaid
stateDiagram-v2
    [*] --> Unassigned : Section active
    Unassigned --> MarksEntered : Faculty submits raw score
    MarksEntered --> ValidateRange : Check 0.00 <= marks <= 100.00
    ValidateRange --> ScoreError : Score < 0 or > 100
    ScoreError --> [*]
    ValidateRange --> AutoGrade : trg_auto_compute_grade fired
    AutoGrade --> Grade_S : marks >= 90
    AutoGrade --> Grade_A : 80 <= marks < 90
    AutoGrade --> Grade_B : 70 <= marks < 80
    AutoGrade --> Grade_C : 60 <= marks < 70
    AutoGrade --> Grade_D : 50 <= marks < 60
    AutoGrade --> Grade_E : 40 <= marks < 50
    AutoGrade --> Grade_F : marks < 40
    Grade_S --> Published
    Grade_A --> Published
    Grade_B --> Published
    Grade_C --> Published
    Grade_D --> Published
    Grade_E --> Published
    Grade_F --> Published
    Published --> [*]
```

### 3. Tuition Fee Remittance Lifecycle
```mermaid
stateDiagram-v2
    [*] --> RemittanceInitiated : Amount & Payment Method chosen
    RemittanceInitiated --> VerifyingReference : Check amount > 0 & unique txn_ref
    VerifyingReference --> TransactionAborted : Duplicate reference found
    TransactionAborted --> [*]
    VerifyingReference --> SuccessLogged : Inserted into FEE_PAYMENT
    SuccessLogged --> DuesRecalculated : Call Calculate_Pending_Fee_Func
    DuesRecalculated --> ReceiptGenerated : Voucher issued with student reg_no
    ReceiptGenerated --> [*]
```
