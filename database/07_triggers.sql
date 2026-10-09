-- Triggers for College Management System

-- Trigger 1: Increment seat count when a student enrolls
CREATE OR REPLACE TRIGGER trg_enrollment_seat_increment
AFTER INSERT ON ENROLLMENT
FOR EACH ROW
BEGIN
    UPDATE COURSE_OFFERING
    SET current_enrolled = current_enrolled + 1
    WHERE offering_id = :NEW.offering_id;
END;
/

-- Trigger 2: Decrement seat count when a student drops/unenrolls
CREATE OR REPLACE TRIGGER trg_enrollment_seat_decrement
AFTER DELETE ON ENROLLMENT
FOR EACH ROW
BEGIN
    UPDATE COURSE_OFFERING
    SET current_enrolled = CASE 
        WHEN current_enrolled > 0 THEN current_enrolled - 1 
        ELSE 0 
    END
    WHERE offering_id = :OLD.offering_id;
END;
/

-- Trigger 3: Automatically compute grade based on marks obtained
CREATE OR REPLACE TRIGGER trg_auto_compute_grade
BEFORE INSERT OR UPDATE ON EXAM_RESULT
FOR EACH ROW
BEGIN
    IF :NEW.marks_obtained < 0 OR :NEW.marks_obtained > 100 THEN
        RAISE_APPLICATION_ERROR(-20001, 'Marks must be between 0 and 100.');
    END IF;

    IF :NEW.marks_obtained >= 90.00 THEN
        :NEW.grade := 'S';
    ELSIF :NEW.marks_obtained >= 80.00 THEN
        :NEW.grade := 'A';
    ELSIF :NEW.marks_obtained >= 70.00 THEN
        :NEW.grade := 'B';
    ELSIF :NEW.marks_obtained >= 60.00 THEN
        :NEW.grade := 'C';
    ELSIF :NEW.marks_obtained >= 50.00 THEN
        :NEW.grade := 'D';
    ELSIF :NEW.marks_obtained >= 40.00 THEN
        :NEW.grade := 'E';
    ELSE
        :NEW.grade := 'F';
    END IF;
END;
/

-- Trigger 4: Prevent enrollment if course offering is full
CREATE OR REPLACE TRIGGER trg_prevent_over_enrollment
BEFORE INSERT ON ENROLLMENT
FOR EACH ROW
DECLARE
    v_cap INTEGER;
    v_curr INTEGER;
BEGIN
    SELECT max_capacity, current_enrolled
    INTO v_cap, v_curr
    FROM COURSE_OFFERING
    WHERE offering_id = :NEW.offering_id;

    IF v_curr >= v_cap THEN
        RAISE_APPLICATION_ERROR(-20002, 'Course Offering is already full.');
    END IF;
END;
/
