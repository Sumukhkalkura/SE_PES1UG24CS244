"""Branch coverage tests for course_registration.py.

Goal: drive every decision in the module to BOTH its true and false outcome,
with boundary values on each side of every threshold.
Expected values are derived directly from the rules in course_registration.py.
"""

import pytest

from course_registration import MAX_CREDITS, can_register, late_fee, waitlist_position


# ===========================================================================
# can_register
# ===========================================================================

# Decision 1: student_status not in MAX_CREDITS
@pytest.mark.parametrize("status", ["regular", "probation", "honors"])
def test_status_valid_branch_false(status):
    assert can_register(status, 0, 1, True) == "registered"


@pytest.mark.parametrize("status", ["", "Regular", "alumni"])
def test_status_invalid_branch_true(status):
    with pytest.raises(ValueError, match="unknown status"):
        can_register(status, 0, 1, True)


def test_status_checked_before_course_credits():
    # Both inputs are invalid; status validation must win.
    with pytest.raises(ValueError, match="unknown status"):
        can_register("visitor", 0, 0, True)


# Decision 2: course_credits <= 0
def test_course_credits_one_is_valid_boundary():
    assert can_register("regular", 0, 1, True) == "registered"


@pytest.mark.parametrize("credits", [0, -1])
def test_course_credits_zero_or_negative_raises(credits):
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, credits, True)


# Decision 3: not prerequisites_met
def test_prerequisites_met_branch_false():
    assert can_register("honors", 10, 3, True) == "registered"


def test_prerequisites_missing_branch_true():
    assert can_register("honors", 10, 3, False) == "prerequisites missing"


def test_prerequisites_checked_before_credit_limit():
    # Would exceed the limit too, but missing prerequisites is reported first.
    assert can_register("probation", 16, 4, False) == "prerequisites missing"


# Decision 4: current_credits + course_credits > MAX_CREDITS[status]
@pytest.mark.parametrize("status", ["regular", "probation", "honors"])
def test_credit_total_equal_to_limit_registers(status):
    limit = MAX_CREDITS[status]
    assert can_register(status, limit - 3, 3, True) == "registered"


@pytest.mark.parametrize("status", ["regular", "probation", "honors"])
def test_credit_total_one_over_limit_rejected(status):
    limit = MAX_CREDITS[status]
    assert can_register(status, limit - 2, 3, True) == "credit limit exceeded"


def test_limit_depends_on_status():
    # 17 credits: over the probation limit (16) but fine for regular (24).
    assert can_register("probation", 14, 3, True) == "credit limit exceeded"
    assert can_register("regular", 14, 3, True) == "registered"


# ===========================================================================
# waitlist_position
# ===========================================================================

# Decision 5: capacity <= 0
def test_capacity_one_is_valid_boundary():
    assert waitlist_position(0, 1, 0) == 0


@pytest.mark.parametrize("capacity", [0, -10])
def test_capacity_zero_or_negative_raises(capacity):
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(0, capacity, 0)


# Decision 6: enrolled < capacity
def test_enrolled_one_below_capacity_gets_seat():
    assert waitlist_position(39, 40, 5) == 0


def test_enrolled_equal_to_capacity_goes_to_waitlist():
    assert waitlist_position(40, 40, 0) == 1


def test_enrolled_above_capacity_goes_to_waitlist():
    assert waitlist_position(42, 40, 2) == 3


# Decision 7: waitlist_length >= 10
def test_waitlist_length_nine_gives_last_slot():
    assert waitlist_position(40, 40, 9) == 10


def test_waitlist_length_ten_is_full():
    assert waitlist_position(40, 40, 10) == -1


def test_waitlist_length_above_ten_is_full():
    assert waitlist_position(40, 40, 15) == -1


# ===========================================================================
# late_fee
# ===========================================================================

# Decision 8: days_late <= 0
@pytest.mark.parametrize("days", [0, -5])
def test_not_late_has_no_fee_even_without_waiver(days):
    assert late_fee(days, 25, False) == 0


def test_one_day_late_is_charged():
    assert late_fee(1, 10, False) == 500


# Decision 9: has_waiver
def test_waiver_true_removes_fee_even_with_surcharges():
    assert late_fee(30, 25, True) == 0


def test_waiver_false_charges_fee():
    assert late_fee(2, 10, False) == 500


# Decision 10: days_late <= 7 (if / else)
def test_day_seven_is_flat_fee_boundary():
    assert late_fee(7, 10, False) == 500


def test_day_eight_adds_first_daily_charge():
    # 500 + (8 - 7) * 100 = 600
    assert late_fee(8, 10, False) == 600


# Decision 11: credits > 20
def test_twenty_credits_no_surcharge():
    assert late_fee(3, 20, False) == 500


def test_twenty_one_credits_adds_surcharge():
    assert late_fee(3, 21, False) == 750


def test_surcharge_combines_with_daily_charge():
    # 500 + (12 - 7) * 100 + 250 = 1250
    assert late_fee(12, 22, False) == 1250


# Decision 12: fee > 2000
def test_fee_below_cap_unchanged():
    # 500 + (21 - 7) * 100 = 1900
    assert late_fee(21, 10, False) == 1900


def test_fee_exactly_at_cap_unchanged():
    # 500 + (22 - 7) * 100 = 2000 -> not > 2000
    assert late_fee(22, 10, False) == 2000


def test_fee_just_above_cap_is_capped():
    # 500 + (23 - 7) * 100 = 2100 -> 2000
    assert late_fee(23, 10, False) == 2000


def test_surcharge_pushing_fee_over_cap_is_capped():
    # 500 + (20 - 7) * 100 + 250 = 2050 -> 2000
    assert late_fee(20, 21, False) == 2000
