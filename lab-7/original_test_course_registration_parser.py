from hypothesis import given, strategies as st
from course_registration_parser import format_course_code, total_credits, parse_student_record

@given(st.text() | st.none())
def test_format_course_code_no_crash(s):
    # To-Do: Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_total_credits_no_crash(s):
    # To-Do: Using try and except complete this function.
    pass

@given(st.text() | st.none())
def test_parse_student_record_no_crash(s):
    # To-Do: Using try and except complete this function.
    pass
