# Lab 5 - Static Code Analysis: Issues Table

File: car_rental.py
Line numbers refer to the original file.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Weak hash (Bandit B324, High) | Security | 48 | SHA-1 used to hash licence numbers | Changed to hashlib.sha256 |
| Bad file permissions (Bandit B103, High) | Security | 67 | Receipt file set to 0o777, anyone can read/write it | Changed to 0o600 |
| SQL injection (Bandit B608, Medium) | Security | 23, 26 | Queries built with string formatting. findCustomer("x' OR '1'='1") returned all customers | Used parameterised queries with ? placeholders |
| Use of exec (Bandit B102, Medium) | Security | 53 | applyPromo runs whatever rule string is typed in | Parse the rule with a regex, only allow "amount = amount * factor" with factor between 0 and 1 |
| Insecure temp file (Bandit B306, Medium) | Security | 63 | tempfile.mktemp is deprecated and unsafe | Used tempfile.mkstemp |
| Hardcoded password (Bandit B105, B107, Low) | Security | 70-71 | Admin password written in the code and used as default argument | Read password from RENTAL_ADMIN_PASSWORD environment variable, compare with hmac.compare_digest |
| Assert used (Bandit B101, Low) | Security | 30 | assert is removed when run with python -O | Replaced with raise ValueError |
| Bare except with pass (Bandit B110, Pylint W0702, Flake8 E722) | Bug | 41-42 | Errors silently ignored, unknown car returns None | Check if plate exists, raise KeyError otherwise |
| Insecure random (Bandit B311, Low) | Security | 45 | random module used for booking codes | Used secrets.randbelow |
| Mutable default argument (Pylint W0102) | Bug | 16 | features=[] shared across calls | Default None, new list created inside function |
| Inconsistent return (Pylint R1710) | Bug | 16, 36 | Some paths return a value, others return None | Raise errors for bad input, return 0 when no extra charge |
| Open without with/encoding (Pylint R1732, W1514) | Quality | 64 | File opened without with block and encoding | Used with os.fdopen(..., encoding="utf-8") |
| Unused import (Pylint W0611, Flake8 F401) | Quality | 2 | json imported but not used | Removed import |
| Naming and docstrings (Pylint C0103, C0114, C0116) | Style | All functions | camelCase function names, no docstrings | Renamed to snake_case, added docstrings |
| Other Pylint warnings (C0209, R1703, R1705, C0206, C0121) | Style | 23, 57, 65, 77-78 | % formatting, if/else returning True/False, == True, looping over keys | f-strings, return bool(...), list comprehension with .items() |
| PEP 8 formatting (Flake8 E302, E305, E501, E712) | Style | Throughout | Missing blank lines, lines longer than 79 characters | Added 2 blank lines between functions, split long lines |
| Car rented twice (found from output, not by tools) | Logic | 29-34 | Car never marked unavailable, same car could be booked again | rent_car checks availability and sets it to False |
| Negative cost (found from output, not by tools) | Logic | 31 | End date before start date gave cost -9000 | Raise ValueError if number of days is 0 or less |
| Negative daily rate (found from output, not by tools) | Logic | 16 | Car added with rate -500 | Raise ValueError for negative rate |

## Summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.94/10 | 10.00/10 |
| Bandit | 11 issues (2 High, 4 Medium, 5 Low) | 0 issues |
| Flake8 | 25 issues | 0 issues |
