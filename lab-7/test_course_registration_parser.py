"""Hypothesis fuzz tests for course_registration_parser.py (Lab 7).

Expected behaviour, decided before the module was fixed:

* All three functions accept any input (any text, None or another type)
  and never raise an exception.
* Valid input gives the same result the original module gave:
      format_course_code("cs 301")                               -> "CS301"
      total_credits("4,3,4")                                     -> 11
      parse_student_record("pes1ug24cs244|Sumukh Kalkura|regular")
          -> {"srn": "PES1UG24CS244", "name": "Sumukh Kalkura", "status": "regular"}
* Malformed input returns None. It never returns a partial or made-up result.

What counts as valid:

* Course code: exactly two words, a department made of ASCII letters and a
  number made of ASCII digits. Extra whitespace around the words is allowed.
* Credit list: one or more comma-separated whole numbers (ASCII digits, so no
  sign, no decimals, no empty items). Spaces around each number are allowed.
* Student record: exactly three '|'-separated fields, all non-empty after
  stripping. The SRN is ASCII letters/digits, the status is ASCII letters and
  the name can be any non-empty text (Unicode is allowed).

derandomize=True and database=None make every run try the same inputs, so the
failures are reproducible.
"""
import string

from hypothesis import example, given, settings, strategies as st

from course_registration_parser import format_course_code, total_credits, parse_student_record

FUZZ = settings(max_examples=500, derandomize=True, database=None, deadline=None)

# Inputs that look roughly like the real format, so the fuzzer also hits
# words, delimiters and numbers instead of only random text.
course_code_like = st.lists(st.text(max_size=5), max_size=4).map(" ".join)
credit_list_like = st.lists(
    st.integers(min_value=-10**6, max_value=10**30).map(str) | st.text(max_size=4),
    max_size=6,
).map(",".join)
student_record_like = st.lists(st.text(max_size=12), max_size=5).map("|".join)

padding = st.sampled_from(["", " ", "  ", "\t"])


# ---------------------------------------------------------------- format_course_code

@FUZZ
@given(st.text() | st.none() | course_code_like)
def test_format_course_code_no_crash(s):
    try:
        result = format_course_code(s)
    except Exception as e:
        assert False, f"format_course_code crashed with {type(e).__name__}: {e}"

    if result is not None:
        # Only a real "DEPT NUMBER" input may give a formatted code.
        parts = s.split()
        assert len(parts) == 2, f"accepted {s!r}, which is not two words"
        dept, number = parts
        assert dept.isascii() and dept.isalpha(), f"accepted department {dept!r}"
        assert number.isascii() and number.isdigit(), f"accepted course number {number!r}"
        assert result == dept.upper() + number


@FUZZ
@given(dept=st.text(alphabet=string.ascii_letters, min_size=1, max_size=6),
       number=st.text(alphabet=string.digits, min_size=1, max_size=5),
       lead=padding, gap=st.sampled_from([" ", "  ", "\t"]), trail=padding)
@example(dept="cs", number="301", lead="", gap=" ", trail="")
def test_format_course_code_valid_inputs(dept, number, lead, gap, trail):
    assert format_course_code(f"{lead}{dept}{gap}{number}{trail}") == dept.upper() + number


def test_format_course_code_rejects_malformed_inputs():
    malformed = [None, "", "   ", "cs", "301", "cs301", "cs 301 extra", "301 cs",
                 "cs 3O1", "cs-301", "c$ 301", "çs 301", "cs ٣٠١", 301, b"cs 301"]
    bad = {}
    for value in malformed:
        try:
            result = format_course_code(value)
        except Exception as e:
            result = f"crashed: {type(e).__name__}"
        if result is not None:
            bad[repr(value)] = result
    assert not bad, f"malformed course codes not rejected: {bad}"


# ---------------------------------------------------------------- total_credits

@FUZZ
@given(st.text() | st.none() | credit_list_like)
def test_total_credits_no_crash(s):
    try:
        result = total_credits(s)
    except Exception as e:
        assert False, f"total_credits crashed with {type(e).__name__}: {e}"

    if result is not None:
        # Only a list of non-negative whole numbers may give a total.
        credits = [part.strip() for part in s.split(",")]
        for credit in credits:
            assert credit.isascii() and credit.isdigit(), f"accepted credit {credit!r} in {s!r}"
        assert type(result) is int and result >= 0
        assert result == sum(int(credit) for credit in credits)


@FUZZ
@given(credits=st.lists(st.integers(min_value=0, max_value=10**30), min_size=1, max_size=10),
       pad=padding)
@example(credits=[4, 3, 4], pad="")
def test_total_credits_valid_inputs(credits, pad):
    text = ",".join(f"{pad}{credit}{pad}" for credit in credits)
    assert total_credits(text) == sum(credits)


def test_total_credits_rejects_malformed_inputs():
    malformed = [None, "", "   ", ",", "4,,3", "4,3,", ",4", "four", "4,three", "-3",
                 "4,-3", "3.5", "+4", "4_000", "١,٢", "9" * 5000, 4, [4, 3]]
    bad = {}
    for value in malformed:
        try:
            result = total_credits(value)
        except Exception as e:
            result = f"crashed: {type(e).__name__}"
        if result is not None:
            bad[repr(value)[:40]] = result
    assert not bad, f"malformed credit lists not rejected: {bad}"


# ---------------------------------------------------------------- parse_student_record

@FUZZ
@given(st.text() | st.none() | student_record_like)
def test_parse_student_record_no_crash(s):
    try:
        result = parse_student_record(s)
    except Exception as e:
        assert False, f"parse_student_record crashed with {type(e).__name__}: {e}"

    if result is not None:
        # Only a full SRN|name|status record may give a dictionary.
        fields = [field.strip() for field in s.split("|")]
        assert len(fields) == 3, f"accepted {s!r}, which does not have exactly 3 fields"
        srn, name, status = fields
        assert srn.isascii() and srn.isalnum(), f"accepted SRN {srn!r}"
        assert name, "accepted an empty name"
        assert status.isascii() and status.isalpha(), f"accepted status {status!r}"
        assert result == {"srn": srn.upper(), "name": name, "status": status.lower()}


@FUZZ
@given(srn=st.text(alphabet=string.ascii_letters + string.digits, min_size=1, max_size=15),
       name=st.text(min_size=1, max_size=30).filter(lambda n: "|" not in n and n.strip()),
       status=st.text(alphabet=string.ascii_letters, min_size=1, max_size=10),
       pad=padding)
@example(srn="pes1ug24cs244", name="Sumukh Kalkura", status="regular", pad="")
@example(srn="pes1ug24cs001", name="Ārya Rāo", status="Regular", pad=" ")
def test_parse_student_record_valid_inputs(srn, name, status, pad):
    line = f"{pad}{srn}{pad}|{pad}{name}{pad}|{pad}{status}{pad}"
    assert parse_student_record(line) == {"srn": srn.upper(), "name": name.strip(),
                                          "status": status.lower()}


def test_parse_student_record_rejects_malformed_inputs():
    malformed = [None, "", "   ", "pes1ug24cs244", "pes1ug24cs244|Sumukh Kalkura",
                 "pes1ug24cs244|Sumukh Kalkura|regular|extra", "pes1ug24cs244||regular",
                 "|Sumukh Kalkura|regular", "pes1ug24cs244|Sumukh Kalkura| ", "||", "|||",
                 "pes 1ug24|Sumukh Kalkura|regular", "pes1ug24cs244|Sumukh Kalkura|régular",
                 "pes1ug24cs244|Sumukh Kalkura|regular-2", 42]
    bad = {}
    for value in malformed:
        try:
            result = parse_student_record(value)
        except Exception as e:
            result = f"crashed: {type(e).__name__}"
        if result is not None:
            bad[repr(value)] = result
    assert not bad, f"malformed student records not rejected: {bad}"
