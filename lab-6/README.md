# Lab 6 — Code and Branch Coverage Analysis

**Name:** Kuradi Sumukh Kalkura  **SRN:** PES1UG24CS244
**Project:** Course Registration
**Source:** [SETAPESU26/L6_L7_56_course_registration](https://github.com/SETAPESU26/L6_L7_56_course_registration), folder `LAB6`

## Objective

The goal is to measure how much of `course_registration.py` the starter tests run, then write tests that reach at least 90% (target 100%) of both kinds of coverage:

- **Statement (code/line) coverage** is the share of executable statements that ran at least once.
- **Branch coverage** is the share of decision outcomes that were taken. Each `if` has a true outcome and a false outcome, and both have to happen.

`course_registration.py` and `test_course_registration.py` are copied unchanged from the assigned repository. Their SHA-256 hashes were checked after every run. Coverage was raised only by adding tests. No lines were excluded and no application code was changed. The upstream README is kept as `ORIGINAL_README.md`.

## Functions under test

| Function | Rules |
|---|---|
| `can_register(status, current, course, prereqs)` | The status must be regular (max 24 credits), probation (max 16) or honors (max 28), otherwise `ValueError`. Course credits must be greater than 0, otherwise `ValueError`. Returns `"prerequisites missing"`, `"credit limit exceeded"` or `"registered"`. |
| `waitlist_position(enrolled, capacity, waitlist_len)` | Capacity must be greater than 0, otherwise `ValueError`. Returns `0` if a seat is free, `-1` if the waitlist has 10 or more people, otherwise `waitlist_len + 1`. |
| `late_fee(days_late, credits, has_waiver)` | Returns 0 if the student is not late or has a waiver. The fee is 500 up to day 7, plus 100 for each day after day 7. Adds 250 if credits are over 20. The fee is capped at 2000. |

## Test suites

| File | Purpose | Tests |
|---|---|---|
| `test_course_registration.py` | Starter tests (unchanged) | 2 |
| `CodeCoverageTest_course_registration_application.py` | Runs every statement: each status, unknown status, zero or negative credits, missing prerequisites, over the limit, exactly at the limit, free seat, invalid capacity, full course, full waitlist, on-time or early registration, waiver, late by 7 days or less, late by more than 7 days, more than 20 credits, fee cap | 21 |
| `BranchCoverageTest_course_registration_application.py` | Takes the true and false outcome of all 12 decisions, using values on both sides of each boundary | 43 |

Boundary values used in the branch suite:

| Decision | False side | True side |
|---|---|---|
| status invalid | regular, probation, honors | `""`, `"Regular"`, `"alumni"` |
| course credits ≤ 0 | 1 | 0, −1 |
| prerequisites missing | `True` | `False` |
| total > limit | exactly at the limit (24, 16, 28) | limit + 1 |
| capacity ≤ 0 | 1 | 0, −10 |
| enrolled < capacity | 40/40, 42/40 | 39/40 |
| waitlist ≥ 10 | 9 | 10, 15 |
| days late ≤ 0 | 1 | 0, −5 |
| waiver | `False` | `True` |
| days late ≤ 7 | 8 (fee 600) | 7 (fee 500) |
| credits > 20 | 20 | 21 |
| fee > 2000 | 1900, exactly 2000 | 2100, 2050 (because of the surcharge) |

The branch suite also checks the order of the checks: an unknown status is reported before invalid credits, and missing prerequisites are reported before the credit limit.

## Setup and running

```bash
cd lab-6
python3 -m venv .venv
source .venv/bin/activate
pip install pytest coverage

# Code coverage
python -m coverage erase
python -m coverage run --source=course_registration -m pytest -q CodeCoverageTest_course_registration_application.py
python -m coverage report -m

# Branch coverage
python -m coverage erase
python -m coverage run --branch --source=course_registration -m pytest -q BranchCoverageTest_course_registration_application.py
python -m coverage report -m
```

`--source=course_registration` limits measurement to the module under test, so the test files and Labs 1–5 are not counted. `pytest.ini` sets up discovery so that a plain `python -m pytest` also collects the `*Test_*.py` files.

## Results

Measured with Python 3.13.7, pytest 9.2.0 and coverage 7.17.3.

| Run | Tests | Stmts | Miss | Branch | BrPart | Cover |
|---|---|---|---|---|---|---|
| Baseline: starter tests, statement | 2 passed | 32 | 20 | – | – | **38%** |
| Baseline: starter tests, branch | 2 passed | 32 | 20 | 24 | 6 | **32%** |
| Final: CodeCoverageTest, statement | 21 passed | 32 | 0 | – | – | **100%** |
| Final: BranchCoverageTest, branch | 43 passed | 32 | 0 | 24 | 0 | **100%** |

The baseline missed lines 6, 8, 10, 12, 18, 21–23 and 27–39. The starter tests never ran `late_fee`, and they never reached any error path or rejection path.

## Line coverage vs. branch coverage

Full line coverage does not prove full branch coverage. An `if` that has no `else` can have every line run while its false outcome never happens. For example:

```python
fee = 500
if credits > 20:
    fee += 250
```

The single test `late_fee(3, 25, False)` runs every line above, so line coverage is 100%. The case where the surcharge is skipped is never tested, so branch coverage is incomplete. This module has several decisions of this kind (lines 35 and 37, and every early-return guard).

In this project, the code-coverage suite also reaches 100% branch coverage. That happens because it has one test per rule, and those tests already cover both outcomes of each decision. It is a property of these particular tests, not something line coverage guarantees. The branch suite goes further by testing the exact boundary values (7/8, 20/21, 9/10, limit/limit+1, 1900/2000/2100). Off-by-one mistakes such as writing `<` instead of `<=` show up at these values. Branch coverage measures whether each outcome happened, not whether the boundaries were tested.

## Deliverables

```
lab-6/
├── course_registration.py                                (original, unchanged)
├── test_course_registration.py                           (original starter tests)
├── ORIGINAL_README.md                                    (upstream LAB6 README)
├── CodeCoverageTest_course_registration_application.py
├── BranchCoverageTest_course_registration_application.py
├── pytest.ini
├── .gitignore                                            (.venv, caches, .coverage, htmlcov)
├── README.md
├── reports/
│   ├── code_coverage.txt          (terminal log of the final code coverage run)
│   ├── branch_coverage.txt        (terminal log of the final branch coverage run)
│   ├── html_code_coverage/        (coverage HTML report)
│   └── html_branch_coverage/      (coverage HTML report)
└── screenshots/
    ├── code_coverage.png          (VS Code terminal capture)
    └── branch_coverage.png        (VS Code terminal capture)
```

## Commits

The work is submitted in two separate commits:

1. **Code coverage:** the source files, the starter tests, the code-coverage suite, the code-coverage report and screenshot, and the shared setup files.
2. **Branch coverage:** the branch-coverage suite, the branch-coverage report and screenshot, and this README.
