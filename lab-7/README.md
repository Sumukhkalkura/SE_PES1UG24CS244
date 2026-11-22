# Lab 7 — Fuzzing for Input Validation Bugs

**Name:** Kuradi Sumukh Kalkura  **SRN:** PES1UG24CS244
**Project:** Course Registration
**Source:** [SETAPESU26/L6_L7_56_course_registration](https://github.com/SETAPESU26/L6_L7_56_course_registration), folder `LAB7`

## Objective

Use property-based fuzz testing with [Hypothesis](https://hypothesis.readthedocs.io/) to find input-validation bugs in `course_registration_parser.py`, then harden its three functions so they handle any input without crashing and still return the same results for valid input.

## Files

| File | Description |
|---|---|
| `course_registration_parser.py` | Fixed module (each change is marked with a `# FIX:` comment) |
| `original_course_registration_parser.py` | Unchanged copy of the buggy module from the assigned repository |
| `test_course_registration_parser.py` | Completed Hypothesis tests (9 tests, 3 for each function) |
| `original_test_course_registration_parser.py` | Unchanged starter test template |
| `ORIGINAL_README.md` | Upstream `LAB7/README.md` |
| `reports/failing_tests.txt` | Full pytest output of the tests against the original module (6 failed, 3 passed) |
| `reports/passing_tests.txt` | Full pytest output of the tests against the fixed module (9 passed) |
| `screenshots/` | SS1–SS4 Terminal screenshots (plus `SS2b`, the first page of the SS2 output) |
| `PES1UG24CS244_Kuradi_Sumukh_Kalkura_LAB7.pdf` | Submission document |

## Expected behaviour (decided before fixing)

* All three functions accept any input (any text, `None` or another type) and never raise.
* Valid input gives the same result as the original module.
* Malformed input returns `None`, never a partial or made-up result. The command-line program prints an error message instead.

| Function | Valid input | Result |
|---|---|---|
| `format_course_code` | Exactly two words: ASCII-letter department, ASCII-digit number (`cs 301`) | `"CS301"` |
| `total_credits` | Comma-separated whole numbers, digits only, spaces allowed (`4,3,4`) | `11` |
| `parse_student_record` | Exactly three non-empty `\|` fields: alphanumeric SRN, any name, alphabetic status | `{"srn": "PES1UG24CS244", "name": "Sumukh Kalkura", "status": "regular"}` |

## Tests

Each function has three tests:

1. **`*_no_crash`** completes the starter template. It uses `@given(st.text() | st.none() | <format-like strategy>)` and the template's `try/except`, so any exception fails the test. If a result comes back, the input must really be valid and the result must be correct.
2. **`*_valid_inputs`** generates valid inputs (with extra whitespace) and checks the exact expected result, so the fix cannot break valid input.
3. **`*_rejects_malformed_inputs`** checks fixed edge cases that must return `None`: empty, `None`, missing/extra fields, Unicode digits, negatives, very large values and so on.

The fuzz tests use `settings(max_examples=500, derandomize=True, database=None)`, so every run tries the same inputs and the results are reproducible.

## Bugs found and fixes

| Function | Input found | Original behaviour | Fix |
|---|---|---|---|
| all three | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` | Return `None` if the input is not a `str` |
| `format_course_code` | `''`, `'cs'`, `'cs 301 extra'` | `ValueError` while unpacking `split()` | Require exactly two words |
| `format_course_code` | `'0 0'`, `'A :'`, `'cs 3O1'` | Returned `'00'`, `'A:'`, `'CS3O1'` | Department must be ASCII letters, number ASCII digits |
| `total_credits` | `''`, `'4,,3'`, `'four'`, `'3.5'` | `ValueError: invalid literal for int()` | Check each stripped item is ASCII digits |
| `total_credits` | `'-0'`, `'4,-3'`, `'+4'`, `'4_000'`, `'١,٢'` | Accepted. `'4,-3'` gave a total of 1 | Digits only: no sign, underscore or non-ASCII digits |
| `total_credits` | `'9' * 5000` | `ValueError: Exceeds the limit (4300 digits)` | Catch the `ValueError` and return `None` |
| `parse_student_record` | `''`, `'\|'`, `'pes1ug24cs244\|Sumukh Kalkura'` | `IndexError: list index out of range` | Require exactly three fields |
| `parse_student_record` | `'\|\|\|'`, `'...\|regular\|extra'` | Extra fields silently dropped | Require exactly three fields |
| `parse_student_record` | `'\|\|'`, `'0\|\|'` | Returned records with empty SRN, name or status | Non-empty fields, alphanumeric SRN, alphabetic status |
| `main()` | Any malformed input, Ctrl+D | Crashed with a traceback | Prints an error message and ends cleanly on EOF/Ctrl+C |

## Results

| Run | Result |
|---|---|
| Tests against the original module | **6 failed, 3 passed.** Only the valid-input tests passed |
| Tests against the fixed module | **9 passed** |
| Extra check (not submitted): 20,000 random inputs per function plus arbitrary Python types | No failures |

## Setup and running

```bash
cd lab-7
python3 -m venv .venv
source .venv/bin/activate
pip install pytest hypothesis

python course_registration_parser.py
python -m pytest -v test_course_registration_parser.py
```

To reproduce the failing run, temporarily copy `original_course_registration_parser.py` over `course_registration_parser.py` and run the tests again.
