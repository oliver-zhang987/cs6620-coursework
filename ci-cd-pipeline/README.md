# CI/CD Pipeline (HW1)

Simple Python project with unit tests and a GitHub Actions CI workflow.

## What's in here

- `src/mathutil.py` - math functions (factorial, fibonacci, is_prime, gcd)
- `src/strutil.py` - string functions (reverse_words, is_palindrome, char_frequency, caesar_cipher)
- `tests/` - pytest unit tests for the above

## How to run

```bash
# from this directory (ci-cd-pipeline/)

# install deps
pip install -r requirements.txt

# run tests
pytest tests/ -v

# lint
flake8 src/ tests/ --max-line-length=120
```

## CI Workflow

The workflow at `.github/workflows/ci.yml` runs on:
- push/PR that changes files in this folder
- manual trigger (workflow_dispatch)

It tests against Python 3.10, 3.11, and 3.12.
