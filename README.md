# CS 6620 – Coursework Repository

This repository contains all assignments and projects for **CS 6620 – Software Engineering Processes** at Northeastern University.

## Repository Structure

```
cs6620-coursework/
├── .github/workflows/   # CI/CD workflow definitions
├── ci-cd-pipeline/      # CI/CD Pipeline (HW 1)
│   ├── src/             # Source code
│   ├── tests/           # Unit tests
│   └── requirements.txt
├── .gitignore
└── README.md            # ← you are here
```

Each assignment lives in its own directory at the repo root. Refer to the README inside each folder for setup and usage instructions.

## CI / CD

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs automatically on every push or pull request that touches assignment code. It can also be triggered manually via the **Actions** tab ("Run workflow").

## Author

Fuheng Zhang – Northeastern University
