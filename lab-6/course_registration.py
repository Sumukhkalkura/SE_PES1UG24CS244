MAX_CREDITS = {"regular": 24, "probation": 16, "honors": 28}


def can_register(student_status, current_credits, course_credits, prerequisites_met):
    if student_status not in MAX_CREDITS:
        raise ValueError("unknown status")
    if course_credits <= 0:
        raise ValueError("invalid course credits")
    if not prerequisites_met:
        return "prerequisites missing"
    if current_credits + course_credits > MAX_CREDITS[student_status]:
        return "credit limit exceeded"
    return "registered"


def waitlist_position(enrolled, capacity, waitlist_length):
    if capacity <= 0:
        raise ValueError("invalid capacity")
    if enrolled < capacity:
        return 0
    if waitlist_length >= 10:
        return -1
    return waitlist_length + 1


def late_fee(days_late, credits, has_waiver):
    if days_late <= 0:
        return 0
    if has_waiver:
        return 0
    if days_late <= 7:
        fee = 500
    else:
        fee = 500 + (days_late - 7) * 100
    if credits > 20:
        fee += 250
    if fee > 2000:
        fee = 2000
    return fee
