-- Cursor for College Management System

-- Cursor Procedure: Generate Academic Report
-- Iterates over student records to display academic summary
CREATE OR REPLACE PROCEDURE Generate_Academic_Report_Cursor
IS
    CURSOR cur_student_summary IS
        SELECT 
            s.student_id,
            s.reg_no,
            s.first_name || ' ' || s.last_name AS full_name,
            d.dept_code,
            COUNT(er.result_id) AS total_courses_evaluated,
            COALESCE(SUM(c.credits), 0) AS total_credits_earned,
            COALESCE(ROUND(AVG(er.marks_obtained), 2), 0.0) AS avg_marks
        FROM STUDENT s
        JOIN DEPARTMENT d ON s.dept_id = d.dept_id
        LEFT JOIN ENROLLMENT e ON s.student_id = e.student_id
        LEFT JOIN COURSE_OFFERING co ON e.offering_id = co.offering_id
        LEFT JOIN COURSE c ON co.course_id = c.course_id
        LEFT JOIN EXAM_RESULT er ON e.enrollment_id = er.enrollment_id
        WHERE s.status = 'Active'
        GROUP BY s.student_id, s.reg_no, s.first_name, s.last_name, d.dept_code
        ORDER BY avg_marks DESC, total_credits_earned DESC;

    v_student_id       STUDENT.student_id%TYPE;
    v_reg_no           STUDENT.reg_no%TYPE;
    v_full_name        VARCHAR2(100);
    v_dept_code        DEPARTMENT.dept_code%TYPE;
    v_courses_count    INTEGER;
    v_credits_earned   INTEGER;
    v_avg_marks        NUMBER(5, 2);

    v_standing         VARCHAR2(30);
    v_total_processed  INTEGER := 0;
    v_honors_count     INTEGER := 0;
    v_first_class_cnt  INTEGER := 0;
BEGIN
    DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('                       ACADEMIC AUDIT REPORT                                            ');
    DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE(RPAD('REG NO', 12) || RPAD('STUDENT NAME', 22) || RPAD('DEPT', 8) || 
                         RPAD('COURSES', 10) || RPAD('CREDITS', 10) || RPAD('AVG MARKS', 12) || 'STANDING');
    DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------------------------------');

    -- Open cursor
    OPEN cur_student_summary;

    -- Fetch loop
    LOOP
        FETCH cur_student_summary INTO 
            v_student_id, 
            v_reg_no, 
            v_full_name, 
            v_dept_code, 
            v_courses_count, 
            v_credits_earned, 
            v_avg_marks;

        EXIT WHEN cur_student_summary%NOTFOUND;

        v_total_processed := v_total_processed + 1;

        IF v_avg_marks >= 90.0 THEN
            v_standing := 'Distinction';
            v_honors_count := v_honors_count + 1;
        ELSIF v_avg_marks >= 75.0 THEN
            v_standing := 'First Class';
            v_first_class_cnt := v_first_class_cnt + 1;
        ELSIF v_avg_marks >= 50.0 THEN
            v_standing := 'Pass';
        ELSIF v_courses_count = 0 THEN
            v_standing := 'Awaiting Evaluation';
        ELSE
            v_standing := 'Warning';
        END IF;

        DBMS_OUTPUT.PUT_LINE(
            RPAD(v_reg_no, 12) || 
            RPAD(v_full_name, 22) || 
            RPAD(v_dept_code, 8) || 
            RPAD(TO_CHAR(v_courses_count), 10) || 
            RPAD(TO_CHAR(v_credits_earned), 10) || 
            RPAD(TO_CHAR(v_avg_marks, '990.00'), 12) || 
            v_standing
        );
    END LOOP;

    -- Close cursor
    CLOSE cur_student_summary;

    DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('Total Students: ' || v_total_processed || ' | Distinction: ' || v_honors_count || ' | First Class: ' || v_first_class_cnt);
    DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------------------------------');

EXCEPTION
    WHEN OTHERS THEN
        IF cur_student_summary%ISOPEN THEN
            CLOSE cur_student_summary;
        END IF;
        DBMS_OUTPUT.PUT_LINE('Error in cursor: ' || SQLERRM);
END Generate_Academic_Report_Cursor;
/
