# Lab 5 – Issues Found and Fixed (`car_rental.py`)

Line numbers refer to the **original** file. Ordered by severity (High → Low).

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Weak hash | Bandit B324 | Security | High | 48 | `hashlib.sha1` used for licence hashing; SHA-1 is broken for security use | Switched to `hashlib.sha256` |
| 2 | World-writable file | Bandit B103 | Security | High | 67 | `os.chmod(path, 0o777)` lets any user read/modify receipts | Changed to `0o600` (owner read/write only) |
| 3 | SQL injection | Bandit B608 | Security | Medium | 23, 26 | Queries built with `%` / string concatenation; `findCustomer("x' OR '1'='1")` returned every customer | Parameterised queries with `?` placeholders |
| 4 | Arbitrary code execution | Bandit B102, Pylint W0122 | Security | Medium | 53 | `exec(rule)` runs any Python typed by counter staff | Strict regex parser that only accepts `amount = amount * <factor>` with 0 < factor ≤ 1 |
| 5 | Insecure temp file | Bandit B306 | Security | Medium | 63 | `tempfile.mktemp` has a race condition (file can be hijacked) | `tempfile.mkstemp` + `os.fdopen` |
| 6 | Hardcoded password | Bandit B105, B107 | Security | Low | 70–71 | Admin password `admin@rent` in source and as a default argument, so `adminLogin("admin")` succeeded | Read from `RENTAL_ADMIN_PASSWORD` env var, no default, `hmac.compare_digest` |
| 7 | Assert for validation | Bandit B101 | Security | Low | 30 | `assert` is stripped with `python -O`, removing the customer check | Explicit `raise ValueError` |
| 8 | Swallowed errors | Bandit B110, Pylint W0702, Flake8 E722 | Bug | Low | 41–42 | Bare `except: pass` hid unknown-plate errors (returned `None`) | Explicit plate check raising `KeyError` |
| 9 | Weak RNG | Bandit B311 | Security | Low | 45 | `random` is predictable for booking codes | `secrets.randbelow` |
| 10 | Mutable default arg | Pylint W0102 | Bug | Medium | 16 | `features=[]` shared across calls | Default `None`, create a new list inside |
| 11 | Inconsistent returns | Pylint R1710 | Bug | Medium | 16, 36 | Functions return a value on some paths and `None` on others | Raise on invalid input; return `0` when no extra charge |
| 12 | File not closed safely | Pylint R1732, W1514 | Quality | Medium | 64 | `open()` without `with` or encoding | `with os.fdopen(fd, "w", encoding="utf-8")` |
| 13 | Unused import | Pylint W0611, Flake8 F401 | Quality | Low | 2 | `json` imported but never used | Removed |
| 14 | Naming / docstrings | Pylint C0103, C0114, C0116 | Style | Low | all functions | camelCase names, no docstrings | snake_case names, module + function docstrings |
| 15 | Misc. Pylint refactors | Pylint C0209, R1703, R1705, C0206, C0121 | Style | Low | 23, 57, 65, 77–78 | `%` formatting, `if…return True else False`, `== True`, iterating keys | f-strings, `return bool(...)`, list comprehension over `.items()` |
| 16 | PEP 8 formatting | Flake8 E302, E305, E501, E712 | Style | Low | throughout | Missing blank lines, lines > 79 chars, `== True` | Two blank lines between functions, wrapped long lines |
| 17 | Car can be rented twice | *Not flagged by tools* (found from output) | Logic bug | High | 29–34 | Renting never marked the car unavailable; "Rent Swift again" succeeded | Check and set `available` in `rent_car` |
| 18 | Negative rental cost | *Not flagged by tools* | Logic bug | High | 31 | End date before start date gave cost `-9000` | Raise `ValueError` if days ≤ 0 |
| 19 | Negative daily rate | *Not flagged by tools* | Logic bug | Medium | 16 | `addCar(..., -500)` accepted | Reject negative `daily_rate` |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.94 / 10 | **10.00 / 10** |
| Bandit | 11 issues (2 High, 4 Medium, 5 Low) | **0** |
| Flake8 | 25 issues | **0** |
