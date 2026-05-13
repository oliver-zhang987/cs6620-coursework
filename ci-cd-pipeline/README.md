# HW 1 – CI/CD Pipeline

This assignment sets up a **CI/CD foundation** for the CS 6620 coursework repository. It contains a small Python utility library, comprehensive unit tests, and a GitHub Actions workflow that runs linting and tests automatically.

## Project Layout

```
ci-cd-pipeline/
├── src/
│   ├── __init__.py
│   ├── mathutil.py      # factorial, fibonacci, is_prime, gcd
│   └── strutil.py       # reverse_words, is_palindrome, char_frequency, caesar_cipher
├── tests/
│   ├── __init__.py
│   ├── test_mathutil.py  # 20 test cases for mathutil
│   └── test_strutil.py   # 22 test cases for strutil
└── requirements.txt      # pytest, flake8
```

## Prerequisites

- **Python 3.10+** (tested on 3.10, 3.11, 3.12)
- `pip` (comes with Python)

## Setup

```bash
# 1. Clone the repository (if you haven't already)
git clone git@github.khoury.northeastern.edu:fuhengzhang/cs6620-coursework.git
cd cs6620-coursework/ci-cd-pipeline

# 2. (Recommended) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

## Running the Code

The utility modules can be imported in a Python interpreter:

```python
from src.mathutil import factorial, is_prime
from src.strutil import caesar_cipher, is_palindrome

print(factorial(6))                         # 720
print(is_prime(97))                         # True
print(caesar_cipher("Hello, World!", 13))   # Uryyb, Jbeyq!
print(is_palindrome("A man, a plan, a canal: Panama"))  # True
```

## Running the Tests

From the `ci-cd-pipeline/` directory:

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run only math tests
pytest tests/test_mathutil.py -v

# Run only string tests
pytest tests/test_strutil.py -v
```

## Linting

```bash
# Critical errors only (syntax errors, undefined names)
flake8 src/ tests/ --select=E9,F63,F7,F82 --show-source

# Full lint report
flake8 src/ tests/ --max-line-length=120 --statistics
```

## CI / CD Workflow

The GitHub Actions workflow (`.github/workflows/ci.yml`) triggers on:

| Trigger | Condition |
|---|---|
| `push` | Any change inside `ci-cd-pipeline/` |
| `pull_request` | Any change inside `ci-cd-pipeline/` |
| `workflow_dispatch` | Manual run from the Actions tab |

**Steps executed by the workflow:**

1. Checkout the repository
2. Set up Python (matrix: 3.10 / 3.11 / 3.12)
3. Install dependencies from `requirements.txt`
4. Lint with `flake8`
5. Run tests with `pytest`
