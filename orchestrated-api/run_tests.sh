#!/bin/bash

# Navigate to the script's directory
cd "$(dirname "$0")"

echo "Starting test stack with Docker Compose..."
docker compose -f docker-compose.test.yml up --build \
    --abort-on-container-exit --exit-code-from tests
EXIT_CODE=$?

echo "Tearing down containers..."
docker compose -f docker-compose.test.yml down -v

exit $EXIT_CODE
