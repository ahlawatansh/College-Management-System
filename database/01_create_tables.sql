DROP TABLE IF EXISTS FEE_PAYMENT;
DROP TABLE IF EXISTS EXAM_RESULT;
DROP TABLE IF EXISTS ENROLLMENT;
DROP TABLE IF EXISTS COURSE_OFFERING;
DROP TABLE IF EXISTS COURSE;
DROP TABLE IF EXISTS STUDENT;
DROP TABLE IF EXISTS FACULTY;
DROP TABLE IF EXISTS DEPARTMENT;

CREATE TABLE DEPARTMENT (
    dept_id             INTEGER PRIMARY KEY,
    dept_name           VARCHAR(100) NOT NULL UNIQUE,
    dept_code           VARCHAR(10)  NOT NULL UNIQUE,
    building            VARCHAR(100) NOT NULL,
    budget              DECIMAL(12, 2) NOT NULL CHECK (budget > 0),
    established_year    INTEGER NOT NULL CHECK (established_year >= 1950 AND established_year <= 2026)
);

CREATE TABLE FACULTY (
    faculty_id          INTEGER PRIMARY KEY,
    first_name          VARCHAR(50)  NOT NULL,
    last_name           VARCHAR(50)  NOT NULL,
    email               VARCHAR(100) NOT NULL UNIQUE,
    phone               VARCHAR(15)  NOT NULL UNIQUE,
    hire_date           DATE         NOT NULL,
    designation         VARCHAR(50)  NOT NULL CHECK (designation IN ('Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer', 'Dean', 'HOD')),
    salary              DECIMAL(10, 2) NOT NULL CHECK (salary >= 25000),
    dept_id             INTEGER NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES DEPARTMENT(dept_id) ON DELETE RESTRICT
);

CREATE TABLE STUDENT (
    student_id          INTEGER PRIMARY KEY,
    reg_no              VARCHAR(20)  NOT NULL UNIQUE,
    first_name          VARCHAR(50)  NOT NULL,
    last_name           VARCHAR(50)  NOT NULL,
    email               VARCHAR(100) NOT NULL UNIQUE,
    phone               VARCHAR(15)  NOT NULL UNIQUE,
    date_of_birth       DATE         NOT NULL,
    gender              VARCHAR(10)  NOT NULL CHECK (gender IN ('Male', 'Female', 'Other')),
    admission_date      DATE         NOT NULL,
    dept_id             INTEGER NOT NULL,
    current_semester    INTEGER NOT NULL DEFAULT 1 CHECK (current_semester BETWEEN 1 AND 8),
    status              VARCHAR(15)  NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Graduated', 'Suspended', 'Withdrawn')),
    FOREIGN KEY (dept_id) REFERENCES DEPARTMENT(dept_id) ON DELETE RESTRICT
);

CREATE TABLE COURSE (
    course_id           INTEGER PRIMARY KEY,
    course_code         VARCHAR(15)  NOT NULL UNIQUE,
    course_title        VARCHAR(100) NOT NULL,
    credits             INTEGER      NOT NULL CHECK (credits BETWEEN 1 AND 6),
    dept_id             INTEGER      NOT NULL,
    course_level        VARCHAR(20)  NOT NULL CHECK (course_level IN ('Introductory', 'Intermediate', 'Advanced', 'Elective')),
    FOREIGN KEY (dept_id) REFERENCES DEPARTMENT(dept_id) ON DELETE RESTRICT
);

CREATE TABLE COURSE_OFFERING (
    offering_id         INTEGER PRIMARY KEY,
    course_id           INTEGER      NOT NULL,
    faculty_id          INTEGER      NOT NULL,
    academic_year       VARCHAR(10)  NOT NULL,
    semester            INTEGER      NOT NULL CHECK (semester BETWEEN 1 AND 8),
    classroom           VARCHAR(50)  NOT NULL,
    max_capacity        INTEGER      NOT NULL CHECK (max_capacity >= 10),
    current_enrolled    INTEGER      NOT NULL DEFAULT 0 CHECK (current_enrolled >= 0 AND current_enrolled <= max_capacity),
    FOREIGN KEY (course_id) REFERENCES COURSE(course_id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES FACULTY(faculty_id) ON DELETE RESTRICT,
    CONSTRAINT unique_course_faculty_term UNIQUE (course_id, faculty_id, academic_year, semester)
);

CREATE TABLE ENROLLMENT (
    enrollment_id       INTEGER PRIMARY KEY,
    student_id          INTEGER      NOT NULL,
    offering_id         INTEGER      NOT NULL,
    enrollment_date     DATE         NOT NULL DEFAULT CURRENT_DATE,
    status              VARCHAR(15)  NOT NULL DEFAULT 'Enrolled' CHECK (status IN ('Enrolled', 'Completed', 'Dropped')),
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE,
    FOREIGN KEY (offering_id) REFERENCES COURSE_OFFERING(offering_id) ON DELETE CASCADE,
    CONSTRAINT unique_student_offering UNIQUE (student_id, offering_id)
);

CREATE TABLE EXAM_RESULT (
    result_id           INTEGER PRIMARY KEY,
    enrollment_id       INTEGER      NOT NULL UNIQUE,
    marks_obtained      DECIMAL(5, 2) NOT NULL CHECK (marks_obtained BETWEEN 0 AND 100),
    grade               VARCHAR(2)   NOT NULL CHECK (grade IN ('S', 'A', 'B', 'C', 'D', 'E', 'F')),
    exam_date           DATE         NOT NULL DEFAULT CURRENT_DATE,
    remarks             VARCHAR(100) DEFAULT 'Regular Evaluation',
    FOREIGN KEY (enrollment_id) REFERENCES ENROLLMENT(enrollment_id) ON DELETE CASCADE
);

CREATE TABLE FEE_PAYMENT (
    payment_id          INTEGER PRIMARY KEY,
    student_id          INTEGER      NOT NULL,
    amount_paid         DECIMAL(10, 2) NOT NULL CHECK (amount_paid > 0),
    payment_date        DATE         NOT NULL DEFAULT CURRENT_DATE,
    payment_method      VARCHAR(20)  NOT NULL CHECK (payment_method IN ('Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Cash')),
    transaction_ref     VARCHAR(50)  NOT NULL UNIQUE,
    payment_status      VARCHAR(15)  NOT NULL DEFAULT 'Success' CHECK (payment_status IN ('Success', 'Pending', 'Failed')),
    FOREIGN KEY (student_id) REFERENCES STUDENT(student_id) ON DELETE CASCADE
);
