import pytest
from course_registration import can_register, waitlist_position, late_fee

#Example test cases:
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0

#Write the rest of the test cases so that the code is 90- 100% covered.
