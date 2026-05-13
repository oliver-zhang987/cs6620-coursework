# CS 6620 – Coursework Repository

This repository contains all assignments and projects for **CS 6620 – Software Engineering Processes** at Northeastern University.

## Repository Structure

```
cs6620-coursework/
├── .github/workflows/   # CI/CD workflow definitions
├── assignments/
│   └── hw1-cicd/        # HW 1 – CI/CD Pipeline
│       ├── src/         # Source code
│       ├── tests/       # Unit tests
│       └── requirements.txt
├── .gitignore
└── README.md            # ← you are here
```

Each assignment lives in its own directory under `assignments/`. Refer to the README inside each assignment folder for setup and usage instructions specific to that assignment.

## CI / CD

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs automatically on every push or pull request that touches assignment code. It can also be triggered manually via the **Actions** tab ("Run workflow").

## Author

Fuheng Zhang – Northeastern University
