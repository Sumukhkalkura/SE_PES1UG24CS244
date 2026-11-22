def format_course_code(code):
    """
    Formats 'cs 301' as 'CS301'.
    Expects exactly two words: a department (letters) and a number (digits).
    Returns None for any other input instead of raising an exception.
    """
    # FIX: None or a non-string has no .split()
    if not isinstance(code, str):
        return None
    parts = code.split()
    # FIX: anything other than exactly two words used to crash the unpacking
    if len(parts) != 2:
        return None
    dept, number = parts
    # FIX: reject codes like '0 0' or 'cs 3O1' instead of formatting them
    if not (dept.isascii() and dept.isalpha() and number.isascii() and number.isdigit()):
        return None
    return dept.upper() + number

def total_credits(text):
    """
    Adds up comma-separated course credits.
    Every value must be a whole number (digits only, spaces around it allowed).
    Returns None for any other input instead of raising an exception.
    """
    # FIX: None or a non-string has no .split()
    if not isinstance(text, str):
        return None
    total = 0
    for credit in text.split(','):
        credit = credit.strip()
        # FIX: empty items ('', '4,,3'), words, decimals and negative numbers are rejected
        if not (credit.isascii() and credit.isdigit()):
            return None
        try:
            total += int(credit)
        except ValueError:
            # FIX: a number too long for int() (over Python's 4300-digit limit)
            return None
    return total

def parse_student_record(line):
    """
    Parses 'SRN|name|status' into a dictionary.
    Expects exactly three non-empty fields: SRN (letters/digits), name, status (letters).
    Returns None for any other input instead of raising an exception.
    """
    # FIX: None or a non-string has no .split()
    if not isinstance(line, str):
        return None
    parts = [part.strip() for part in line.split('|')]
    # FIX: missing fields used to raise IndexError, extra fields were silently dropped
    if len(parts) != 3:
        return None
    srn, name, status = parts
    # FIX: empty or malformed fields are rejected instead of returned as a record
    if not (srn.isascii() and srn.isalnum() and name and status.isascii() and status.isalpha()):
        return None
    return {"srn": srn.upper(),
            "name": name,
            "status": status.lower()}

def main():
    print("==== Running format_course_code ====")
    value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    result = format_course_code(value)
    # FIX: report invalid input instead of crashing
    if result is None:
        print("Invalid course code: expected DEPT NUMBER, e.g. cs 301")
    else:
        print("Formatted course code:", result)

    print("\n==== Running total_credits ====")
    value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    result = total_credits(value)
    if result is None:
        print("Invalid credits: expected whole numbers separated by commas, e.g. 4,3,4")
    else:
        print("Total credits:", result)

    print("\n==== Running parse_student_record ====")
    value = input("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ")
    result = parse_student_record(value)
    if result is None:
        print("Invalid student record: expected SRN|name|status, e.g. pes1ug23cs001|Asha|regular")
    else:
        print("Student record:", result)

if __name__ == "__main__":
    # FIX: end cleanly on Ctrl+D / Ctrl+C instead of printing a traceback
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended. Exiting.")
