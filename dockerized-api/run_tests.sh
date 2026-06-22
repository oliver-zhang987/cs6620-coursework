#!/bin/bash
set -e

# Navigate to the script's directory
cd "$(dirname "$0")"

echo "Building test Docker image..."
docker build -t dockerized-api-test -f Dockerfile.test .

echo "Running tests in Docker container..."
docker run --rm dockerized-api-test
