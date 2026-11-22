def format_course_code(code):
    """
    Formats 'cs 301' as 'CS301'.
    Assumes code has exactly two words: department and number.
    """
    dept, number = code.split()
    return dept.upper() + number

def total_credits(text):
    """
    Adds up comma-separated course credits.
    Assumes every value is a whole number.
    """
    return sum(int(credit) for credit in text.split(','))

def parse_student_record(line):
    """
    Parses 'SRN|name|status' into a dictionary.
    Assumes all three fields are present.
    """
    parts = line.split('|')
    return {"srn": parts[0].strip().upper(),
            "name": parts[1].strip(),
            "status": parts[2].strip().lower()}

def main():
    print("==== Running format_course_code ====")
    value = input("Enter a course code as DEPT NUMBER (e.g. cs 301): ")
    print("Formatted course code:", format_course_code(value))

    print("\n==== Running total_credits ====")
    value = input("Enter course credits separated by commas (e.g. 4,3,4): ")
    print("Total credits:", total_credits(value))

    print("\n==== Running parse_student_record ====")
    value = input("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ")
    print("Student record:", parse_student_record(value))

if __name__ == "__main__":
    main()
