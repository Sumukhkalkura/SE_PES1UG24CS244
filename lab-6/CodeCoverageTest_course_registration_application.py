"""Code (statement) coverage tests for course_registration.py.

Goal: execute every statement of the module at least once.
Expected values are derived directly from the rules in course_registration.py.
"""

import pytest

from course_registration import can_register, late_fee, waitlist_position


# ---------------------------------------------------------------------------
# can_register(student_status, current_credits, course_credits, prerequisites_met)
# Limits: regular 24, probation 16, honors 28
# ---------------------------------------------------------------------------

def test_regular_student_registers_below_limit():
    assert can_register("regular", 10, 4, True) == "registered"


def test_probation_student_registers_below_limit():
    assert can_register("probation", 10, 3, True) == "registered"


def test_honors_student_registers_below_limit():
    assert can_register("honors", 20, 4, True) == "registered"


def test_registration_exactly_at_credit_limit_is_allowed():
    # 20 + 4 == 24 == regular limit
    assert can_register("regular", 20, 4, True) == "registered"


def test_unknown_student_status_raises():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("graduate", 10, 4, True)


def test_zero_course_credits_raises():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)


def test_negative_course_credits_raises():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, -3, True)


def test_missing_prerequisites_blocks_registration():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"


def test_exceeding_maximum_credits_is_rejected():
    # 22 + 3 == 25 > 24
    assert can_register("regular", 22, 3, True) == "credit limit exceeded"


# ---------------------------------------------------------------------------
# waitlist_position(enrolled, capacity, waitlist_length)
# ---------------------------------------------------------------------------

def test_seat_available_returns_zero():
    assert waitlist_position(30, 40, 0) == 0


def test_zero_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, 0, 0)


def test_negative_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(5, -5, 0)


def test_full_course_returns_next_waitlist_position():
    # 3 people already waiting -> new student is 4th
    assert waitlist_position(40, 40, 3) == 4


def test_full_waitlist_of_ten_returns_minus_one():
    assert waitlist_position(40, 40, 10) == -1


# ---------------------------------------------------------------------------
# late_fee(days_late, credits, has_waiver)
# ---------------------------------------------------------------------------

def test_on_time_registration_has_no_fee():
    assert late_fee(0, 12, False) == 0


def test_early_registration_has_no_fee():
    assert late_fee(-2, 12, False) == 0


def test_waiver_removes_late_fee():
    assert late_fee(5, 12, True) == 0


def test_late_within_seven_days_flat_fee():
    assert late_fee(3, 12, False) == 500


def test_late_after_seven_days_adds_daily_charge():
    # 500 + (10 - 7) * 100 = 800
    assert late_fee(10, 12, False) == 800


def test_more_than_twenty_credits_adds_surcharge():
    # 500 + 250 = 750
    assert late_fee(5, 21, False) == 750


def test_fee_is_capped_at_two_thousand():
    # 500 + (30 - 7) * 100 = 2800 -> capped to 2000
    assert late_fee(30, 12, False) == 2000
