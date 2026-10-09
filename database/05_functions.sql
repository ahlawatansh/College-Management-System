-- Functions for College Management System

-- Function 1: Calculate Student GPA
-- Returns weighted CGPA on a 10.0 scale based on course credits
CREATE OR REPLACE FUNCTION Calculate_Student_GPA_Func (
    p_student_id IN INTEGER
) RETURN NUMBER
IS
    v_total_weighted_points NUMBER := 0;
    v_total_credits         NUMBER := 0;
    v_cgpa                  NUMBER := 0.0;
    v_grade_point           NUMBER;

    CURSOR c_grades IS
        SELECT c.credits, er.grade
        FROM ENROLLMENT e
        JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
        JOIN COURSE c ON co.course_id = c.course_id
        JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id
        WHERE e.student_id = p_student_id;
BEGIN
    FOR r IN c_grades LOOP
        CASE r.grade
            WHEN 'S' THEN v_grade_point := 10.0;
            WHEN 'A' THEN v_grade_point := 9.0;
            WHEN 'B' THEN v_grade_point := 8.0;
            WHEN 'C' THEN v_grade_point := 7.0;
            WHEN 'D' THEN v_grade_point := 6.0;
            WHEN 'E' THEN v_grade_point := 5.0;
            ELSE          v_grade_point := 0.0;
        END CASE;

        v_total_weighted_points := v_total_weighted_points + (r.credits * v_grade_point);
        v_total_credits := v_total_credits + r.credits;
    END LOOP;

    IF v_total_credits > 0 THEN
        v_cgpa := ROUND(v_total_weighted_points / v_total_credits, 2);
    ELSE
        v_cgpa := 0.0;
    END IF;

    RETURN v_cgpa;
EXCEPTION
    WHEN OTHERS THEN
        RETURN 0.0;
END Calculate_Student_GPA_Func;
/

-- Function 2: Calculate Pending Fee
-- Computes remaining tuition balance owed by a student
CREATE OR REPLACE FUNCTION Calculate_Pending_Fee_Func (
    p_student_id       IN INTEGER,
    p_standard_fee     IN NUMBER DEFAULT 190000.00
) RETURN NUMBER
IS
    v_total_paid   NUMBER := 0;
    v_pending_fee  NUMBER := 0;
BEGIN
    SELECT COALESCE(SUM(amount_paid), 0)
    INTO v_total_paid
    FROM FEE_PAYMENT
    WHERE student_id = p_student_id AND payment_status = 'Success';

    v_pending_fee := p_standard_fee - v_total_paid;

    IF v_pending_fee < 0 THEN
        v_pending_fee := 0;
    END IF;

    RETURN v_pending_fee;
EXCEPTION
    WHEN OTHERS THEN
        RETURN p_standard_fee;
END Calculate_Pending_Fee_Func;
/

-- Function 3: Get Available Seats
-- Returns remaining seats for a course offering
CREATE OR REPLACE FUNCTION Get_Offering_Available_Seats_Func (
    p_offering_id IN INTEGER
) RETURN INTEGER
IS
    v_available_seats INTEGER := 0;
BEGIN
    SELECT (max_capacity - current_enrolled)
    INTO v_available_seats
    FROM COURSE_OFFERING
    WHERE offering_id = p_offering_id;

    RETURN v_available_seats;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN -1;
    WHEN OTHERS THEN
        RETURN 0;
END Get_Offering_Available_Seats_Func;
/
