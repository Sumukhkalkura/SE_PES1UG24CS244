# Lab 5 – Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the Flake8 style issues and simple Pylint warnings: missing blank lines, long lines, the unused `json` import, and `== True`. Each has a single obvious mechanical fix. The hardest was removing `exec()` from `applyPromo`. Simply deleting it would break the promo feature, so I had to design a safe replacement: a strict regex that accepts only `amount = amount * <factor>` and checks the factor is between 0 and 1. The hardcoded admin password was also tricky, because removing it changes how the program is configured (it now reads `RENTAL_ADMIN_PASSWORD` from the environment). The logic bugs were hard in a different way. No tool reported them; I found them only by reading the program output (renting the same car twice, a cost of -9000).

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Partly. Bandit's B311 (`random` is not cryptographically secure) is borderline for a booking code that is not a secret. Switching to `secrets` was still cheap and harmless. Bandit's B608 on `findCustomer` was rated Low confidence, but it was a real vulnerability: the demo's `"x' OR '1'='1"` lookup returned every customer. Several issues were also reported by more than one tool (the bare `except` by Bandit, Pylint and Flake8; the unused import by Pylint and Flake8), which is duplication rather than a false positive.

**3. How would you integrate static analysis tools into your actual software development workflow?**

Locally, I would run Flake8 and Bandit in a `pre-commit` hook so style and security problems are caught before a commit. In CI (e.g. GitHub Actions), I would run Pylint, Flake8 and Bandit on every push and pull request. The build would fail on any High/Medium Bandit finding, any Flake8 error, or a Pylint score below a threshold such as 9.5. Editor plugins give instant feedback while typing. Reports would be saved as build artifacts so reviewers can see them.

**4. What tangible improvements did you observe in code quality, readability, or robustness after applying the fixes?**

- **Security:** SQL injection, arbitrary code execution, the world-writable receipt file, the insecure temp file and the hardcoded password are all gone (Bandit: 11 issues → 0).
- **Robustness:** invalid input now raises clear errors instead of failing silently or producing wrong numbers. Double-renting, negative costs and negative rates are rejected, and unknown plates raise `KeyError` instead of returning `None`.
- **Readability:** snake_case names, docstrings, f-strings, named constants (`FREE_KM`, `EXTRA_KM_RATE`) and PEP 8 formatting make the code easier to read (Pylint 4.94 → 10.00, Flake8 25 → 0).
- **Maintainability:** the `if __name__ == "__main__"` guard means the module can be imported (e.g. for tests) without running the demo.
