# Dockerized REST API

A simple Python-based REST API built with Flask, containerized using Docker, and configured with a CI/CD pipeline that reports test status to Slack.

## API Endpoints

The API manages a simple in-memory list of items.

| Verb | Endpoint | Description | Status Code |
|------|----------|-------------|-------------|
| GET | `/items` | Get list of all items | `200 OK` |
| GET | `/items/<id>` | Get a specific item | `200 OK` / `404 Not Found` |
| POST | `/items` | Create a new item (requires JSON: `{"name": "..."}`) | `201 Created` / `400 Bad Request` |
| PUT | `/items/<id>` | Update an existing item (requires JSON) | `200 OK` / `404 Not Found` / `400 Bad Request` |
| DELETE| `/items/<id>` | Delete an item | `200 OK` / `404 Not Found` |

## Local Development (Without Docker)

To run or test the API directly on your host machine:

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the API
```bash
python src/app.py
```

### Run tests
```bash
python3 -m pytest tests/ -v
```

## Running with Docker

We provide two Dockerfiles and shell scripts to automate container building and execution.

### 1. Run the REST API
To build and run the API container until manually stopped:
```bash
./run_api.sh
```
This builds the `dockerized-api` image and maps port `5000` of the container to port `5000` on your local host. You can access the API at `http://localhost:5000`.

To stop the container, press `Ctrl+C` in the terminal.

### 2. Run the Tests
To build and run the test suite container:
```bash
./run_tests.sh
```
This builds the `dockerized-api-test` image and runs `pytest tests/ -v`. It exits with status code `0` if all tests pass, and a non-zero code if any test fails.

## CI/CD Pipeline

The GitHub Actions workflow is located at `.github/workflows/docker-api.yml`.

### Triggers
- Automatic: Any push or pull request that touches files inside `dockerized-api/`.
- Manual: Can be triggered via the Actions tab in GitHub (using `workflow_dispatch`).

### Slack Notifications
The workflow reports the outcome (Success, Failure, etc.) to a Slack channel using a Slack webhook.
To configure this:
1. Generate an Incoming Webhook in your Slack workspace.
2. In your GitHub repository settings, add a Repository Secret:
   - Name: `SLACK_WEBHOOK_URL`
   - Value: `<Your Slack Webhook URL>`

