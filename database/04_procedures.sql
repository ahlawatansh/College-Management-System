-- Stored Procedures for College Management System

-- Procedure 1: Enroll Student
-- Enrolls a student in a course offering after checking capacity and duplicate registration
CREATE OR REPLACE PROCEDURE Enroll_Student_Proc (
    p_student_id    IN  INTEGER,
    p_offering_id   IN  INTEGER,
    p_status_msg    OUT VARCHAR2
)
IS
    v_student_count    INTEGER;
    v_offering_count   INTEGER;
    v_already_enrolled INTEGER;
    v_max_capacity     INTEGER;
    v_current_enrolled INTEGER;
    v_new_enrollment_id INTEGER;
    v_student_name     VARCHAR2(100);
    v_course_code      VARCHAR2(20);

    e_student_not_found  EXCEPTION;
    e_offering_not_found EXCEPTION;
    e_already_registered EXCEPTION;
    e_class_full         EXCEPTION;
BEGIN
    -- Check if student exists
    SELECT COUNT(*), MAX(first_name || ' ' || last_name)
    INTO v_student_count, v_student_name
    FROM STUDENT
    WHERE student_id = p_student_id AND status = 'Active';

    IF v_student_count = 0 THEN
        RAISE e_student_not_found;
    END IF;

    -- Check course offering and seats
    SELECT COUNT(*), MAX(co.max_capacity), MAX(co.current_enrolled), MAX(c.course_code)
    INTO v_offering_count, v_max_capacity, v_current_enrolled, v_course_code
    FROM COURSE_OFFERING co
    JOIN COURSE c ON co.course_id = c.course_id
    WHERE co.offering_id = p_offering_id;

    IF v_offering_count = 0 THEN
        RAISE e_offering_not_found;
    END IF;

    -- Check if already enrolled
    SELECT COUNT(*)
    INTO v_already_enrolled
    FROM ENROLLMENT
    WHERE student_id = p_student_id AND offering_id = p_offering_id;

    IF v_already_enrolled > 0 THEN
        RAISE e_already_registered;
    END IF;

    -- Check capacity
    IF v_current_enrolled >= v_max_capacity THEN
        RAISE e_class_full;
    END IF;

    -- Insert new enrollment
    SELECT NVL(MAX(enrollment_id), 500) + 1 INTO v_new_enrollment_id FROM ENROLLMENT;

    INSERT INTO ENROLLMENT (enrollment_id, student_id, offering_id, enrollment_date, status)
    VALUES (v_new_enrollment_id, p_student_id, p_offering_id, SYSDATE, 'Enrolled');

    -- Increment seat count
    UPDATE COURSE_OFFERING
    SET current_enrolled = current_enrolled + 1
    WHERE offering_id = p_offering_id;

    COMMIT;

    p_status_msg := 'SUCCESS: Student ' || v_student_name || ' registered for ' || v_course_code;
    DBMS_OUTPUT.PUT_LINE(p_status_msg);

EXCEPTION
    WHEN e_student_not_found THEN
        p_status_msg := 'ERROR: Student ID ' || p_student_id || ' not found.';
        DBMS_OUTPUT.PUT_LINE(p_status_msg);
    WHEN e_offering_not_found THEN
        p_status_msg := 'ERROR: Course Offering ID ' || p_offering_id || ' not found.';
        DBMS_OUTPUT.PUT_LINE(p_status_msg);
    WHEN e_already_registered THEN
        p_status_msg := 'ERROR: Student already enrolled.';
        DBMS_OUTPUT.PUT_LINE(p_status_msg);
    WHEN e_class_full THEN
        p_status_msg := 'ERROR: Course Offering is full.';
        DBMS_OUTPUT.PUT_LINE(p_status_msg);
    WHEN OTHERS THEN
        ROLLBACK;
        p_status_msg := 'ERROR: ' || SQLERRM;
        DBMS_OUTPUT.PUT_LINE(p_status_msg);
END Enroll_Student_Proc;
/

-- Procedure 2: Process Fee Payment
-- Records fee payment and outputs confirmation
CREATE OR REPLACE PROCEDURE Process_Fee_Payment_Proc (
    p_student_id       IN  INTEGER,
    p_amount           IN  NUMBER,
    p_payment_method   IN  VARCHAR2,
    p_transaction_ref  IN  VARCHAR2,
    p_receipt_msg      OUT VARCHAR2
)
IS
    v_student_count    INTEGER;
    v_student_name     VARCHAR2(100);
    v_reg_no           VARCHAR2(20);
    v_dup_txn_count    INTEGER;
    v_new_payment_id   INTEGER;

    e_invalid_student  EXCEPTION;
    e_invalid_amount   EXCEPTION;
    e_duplicate_txn    EXCEPTION;
BEGIN
    -- Check student
    SELECT COUNT(*), MAX(first_name || ' ' || last_name), MAX(reg_no)
    INTO v_student_count, v_student_name, v_reg_no
    FROM STUDENT
    WHERE student_id = p_student_id;

    IF v_student_count = 0 THEN
        RAISE e_invalid_student;
    END IF;

    -- Validate amount
    IF p_amount <= 0 THEN
        RAISE e_invalid_amount;
    END IF;

    -- Check duplicate transaction
    SELECT COUNT(*)
    INTO v_dup_txn_count
    FROM FEE_PAYMENT
    WHERE transaction_ref = p_transaction_ref;

    IF v_dup_txn_count > 0 THEN
        RAISE e_duplicate_txn;
    END IF;

    -- Insert payment
    SELECT NVL(MAX(payment_id), 700) + 1 INTO v_new_payment_id FROM FEE_PAYMENT;

    INSERT INTO FEE_PAYMENT (payment_id, student_id, amount_paid, payment_date, payment_method, transaction_ref, payment_status)
    VALUES (v_new_payment_id, p_student_id, p_amount, SYSDATE, p_payment_method, p_transaction_ref, 'Success');

    COMMIT;

    p_receipt_msg := 'SUCCESS: Payment recorded for ' || v_student_name || ' (' || v_reg_no || ') Amount: ' || p_amount;
    DBMS_OUTPUT.PUT_LINE(p_receipt_msg);

EXCEPTION
    WHEN e_invalid_student THEN
        p_receipt_msg := 'ERROR: Invalid Student ID ' || p_student_id;
        DBMS_OUTPUT.PUT_LINE(p_receipt_msg);
    WHEN e_invalid_amount THEN
        p_receipt_msg := 'ERROR: Amount must be greater than zero.';
        DBMS_OUTPUT.PUT_LINE(p_receipt_msg);
    WHEN e_duplicate_txn THEN
        p_receipt_msg := 'ERROR: Transaction reference already exists.';
        DBMS_OUTPUT.PUT_LINE(p_receipt_msg);
    WHEN OTHERS THEN
        ROLLBACK;
        p_receipt_msg := 'ERROR: ' || SQLERRM;
        DBMS_OUTPUT.PUT_LINE(p_receipt_msg);
END Process_Fee_Payment_Proc;
/

-- Procedure 3: Record Exam Result
-- Inserts or updates marks and assigns grade automatically
CREATE OR REPLACE PROCEDURE Record_Exam_Result_Proc (
    p_enrollment_id    IN  INTEGER,
    p_marks            IN  NUMBER,
    p_remarks          IN  VARCHAR2,
    p_result_msg       OUT VARCHAR2
)
IS
    v_enroll_count     INTEGER;
    v_grade            VARCHAR2(2);
    v_result_count     INTEGER;
    v_new_result_id    INTEGER;
    v_student_reg      VARCHAR2(20);
    v_course_title     VARCHAR2(100);

    e_invalid_enrollment EXCEPTION;
    e_invalid_marks      EXCEPTION;
BEGIN
    -- Check enrollment
    SELECT COUNT(*), MAX(s.reg_no), MAX(c.course_title)
    INTO v_enroll_count, v_student_reg, v_course_title
    FROM ENROLLMENT e
    JOIN STUDENT s ON e.student_id = s.student_id
    JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
    JOIN COURSE c ON co.course_id = c.course_id
    WHERE e.enrollment_id = p_enrollment_id;

    IF v_enroll_count = 0 THEN
        RAISE e_invalid_enrollment;
    END IF;

    -- Validate marks
    IF p_marks < 0 OR p_marks > 100 THEN
        RAISE e_invalid_marks;
    END IF;

    -- Determine grade
    IF p_marks >= 90 THEN
        v_grade := 'S';
    ELSIF p_marks >= 80 THEN
        v_grade := 'A';
    ELSIF p_marks >= 70 THEN
        v_grade := 'B';
    ELSIF p_marks >= 60 THEN
        v_grade := 'C';
    ELSIF p_marks >= 50 THEN
        v_grade := 'D';
    ELSIF p_marks >= 40 THEN
        v_grade := 'E';
    ELSE
        v_grade := 'F';
    END IF;

    -- Insert or update
    SELECT COUNT(*) INTO v_result_count FROM EXAM_RESULT WHERE enrollment_id = p_enrollment_id;

    IF v_result_count > 0 THEN
        UPDATE EXAM_RESULT
        SET marks_obtained = p_marks,
            grade = v_grade,
            exam_date = SYSDATE,
            remarks = p_remarks
        WHERE enrollment_id = p_enrollment_id;
    ELSE
        SELECT NVL(MAX(result_id), 600) + 1 INTO v_new_result_id FROM EXAM_RESULT;
        INSERT INTO EXAM_RESULT (result_id, enrollment_id, marks_obtained, grade, exam_date, remarks)
        VALUES (v_new_result_id, p_enrollment_id, p_marks, v_grade, SYSDATE, p_remarks);
    END IF;

    COMMIT;

    p_result_msg := 'SUCCESS: Result updated for ' || v_student_reg || ' in ' || v_course_title || ' Marks: ' || p_marks || ' Grade: ' || v_grade;
    DBMS_OUTPUT.PUT_LINE(p_result_msg);

EXCEPTION
    WHEN e_invalid_enrollment THEN
        p_result_msg := 'ERROR: Enrollment ID ' || p_enrollment_id || ' does not exist.';
        DBMS_OUTPUT.PUT_LINE(p_result_msg);
    WHEN e_invalid_marks THEN
        p_result_msg := 'ERROR: Marks must be between 0 and 100.';
        DBMS_OUTPUT.PUT_LINE(p_result_msg);
    WHEN OTHERS THEN
        ROLLBACK;
        p_result_msg := 'ERROR: ' || SQLERRM;
        DBMS_OUTPUT.PUT_LINE(p_result_msg);
END Record_Exam_Result_Proc;
/
