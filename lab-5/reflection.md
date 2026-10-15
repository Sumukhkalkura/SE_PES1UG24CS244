# Lab 5 - Reflection

1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were the Flake8 formatting issues and small Pylint warnings like the unused json import, missing blank lines and long lines. These only needed simple changes. The hardest was removing exec() from applyPromo. Just deleting it would break the promo feature, so I wrote a regex that only accepts rules like "amount = amount * 0.9". The hardcoded admin password was also not straightforward since the password now has to come from an environment variable. The logic bugs (renting the same car twice, negative cost) were also hard because none of the tools reported them, I only found them by reading the program output.

2. Did the static analysis tools report any false positives? If so, describe one example.

Bandit B311 (using random) is close to a false positive here, since a booking code is not really a secret. I still changed it to secrets because it was an easy change. The SQL injection warning on findCustomer had low confidence but it was a real problem, the test input x' OR '1'='1 returned every customer. Some issues were reported by more than one tool, for example the bare except was flagged by Bandit, Pylint and Flake8.

3. How would you integrate static analysis tools into your actual software development workflow?

I would add Flake8 and Bandit to a pre-commit hook so problems are caught before committing. In CI (for example GitHub Actions) I would run all three tools on every push and pull request, and fail the build if Bandit finds any high or medium issue, Flake8 reports errors, or the Pylint score goes below 9.5. Using linter plugins in the editor also helps catch issues while writing code.

4. What tangible improvements did you observe in code quality, readability, or potential robustness after applying the fixes?

The security problems (SQL injection, exec, file permissions, temp file, hardcoded password) are fixed and Bandit now reports 0 issues. The program now gives proper errors for invalid input instead of failing silently or giving wrong values like a negative cost. The code is easier to read with snake_case names, docstrings, f-strings and named constants. The Pylint score went from 4.94 to 10.00 and Flake8 went from 25 issues to 0. The main() call is now under if __name__ == "__main__" so the file can be imported without running the demo.
