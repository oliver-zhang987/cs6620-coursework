import os
import json
import pytest
import requests
import boto3
from botocore.exceptions import ClientError

# Config from env (set by docker-compose.test.yml)
API_URL = os.environ.get("API_URL", "http://localhost:5000")
AWS_ENDPOINT = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

TABLE_NAME = "items"
BUCKET_NAME = "items-bucket"

# Direct boto3 clients for verifying DynamoDB / S3 state
dynamodb = boto3.resource("dynamodb", endpoint_url=AWS_ENDPOINT, region_name=REGION)
table = dynamodb.Table(TABLE_NAME)
s3 = boto3.client("s3", endpoint_url=AWS_ENDPOINT, region_name=REGION)


# ── helpers ──────────────────────────────────────────────────────────

def _get_db_item(item_id):
    """Fetch an item directly from DynamoDB."""
    result = table.get_item(Key={"id": item_id})
    return result.get("Item")


def _get_s3_object(item_id):
    """Fetch and parse a JSON object from S3."""
    try:
        resp = s3.get_object(Bucket=BUCKET_NAME, Key=item_id)
        return json.loads(resp["Body"].read().decode())
    except ClientError:
        return None


def _s3_object_exists(item_id):
    """Check whether an object exists in S3."""
    try:
        s3.head_object(Bucket=BUCKET_NAME, Key=item_id)
        return True
    except ClientError:
        return False


# ── POST tests ───────────────────────────────────────────────────────

def test_post_creates_item_in_db_and_s3():
    """POST stores item in DynamoDB AND S3, and both should match."""
    payload = {"name": "Test Widget", "description": "A test widget"}
    resp = requests.post(f"{API_URL}/items", json=payload)
    assert resp.status_code == 201

    item = resp.json()
    item_id = item["id"]
    assert item["name"] == "Test Widget"

    # Verify DynamoDB
    db_item = _get_db_item(item_id)
    assert db_item is not None
    assert db_item["name"] == "Test Widget"

    # Verify S3
    s3_item = _get_s3_object(item_id)
    assert s3_item is not None
    assert s3_item["name"] == "Test Widget"

    # DB and S3 should match
    assert db_item == s3_item

    # cleanup
    requests.delete(f"{API_URL}/items/{item_id}")


def test_post_duplicate_returns_conflict():
    """Posting an item with the same name twice returns 409."""
    payload = {"name": "Duplicate Thing", "description": "first one"}
    resp1 = requests.post(f"{API_URL}/items", json=payload)
    assert resp1.status_code == 201
    item_id = resp1.json()["id"]

    # same name again
    resp2 = requests.post(f"{API_URL}/items", json=payload)
    assert resp2.status_code == 409

    # cleanup
    requests.delete(f"{API_URL}/items/{item_id}")


# ── GET tests ────────────────────────────────────────────────────────

def test_get_item_returns_expected_json():
    """GET with a valid id returns the correct item from the database."""
    payload = {"name": "Fetch Me", "description": "fetch test"}
    create_resp = requests.post(f"{API_URL}/items", json=payload)
    item_id = create_resp.json()["id"]

    resp = requests.get(f"{API_URL}/items/{item_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == item_id
    assert data["name"] == "Fetch Me"

    # DB and S3 should match
    db_item = _get_db_item(item_id)
    s3_item = _get_s3_object(item_id)
    assert db_item == s3_item

    requests.delete(f"{API_URL}/items/{item_id}")


def test_get_item_not_found():
    """GET for an id that doesn't exist returns 404."""
    resp = requests.get(f"{API_URL}/items/nonexistent-id-12345")
    assert resp.status_code == 404
    assert "error" in resp.json()


def test_get_all_items():
    """GET /items with no parameters returns all items."""
    r1 = requests.post(f"{API_URL}/items", json={"name": "ListItem-A"})
    r2 = requests.post(f"{API_URL}/items", json={"name": "ListItem-B"})
    id1 = r1.json()["id"]
    id2 = r2.json()["id"]

    resp = requests.get(f"{API_URL}/items")
    assert resp.status_code == 200
    data = resp.json()
    names = [item["name"] for item in data]
    assert "ListItem-A" in names
    assert "ListItem-B" in names

    requests.delete(f"{API_URL}/items/{id1}")
    requests.delete(f"{API_URL}/items/{id2}")


def test_get_item_bad_id():
    """GET with a garbage / incorrect id returns 404."""
    resp = requests.get(f"{API_URL}/items/!!!invalid!!!")
    assert resp.status_code == 404
    assert "error" in resp.json()


# ── PUT tests ────────────────────────────────────────────────────────

def test_put_updates_db_and_s3():
    """PUT updates the item in both DynamoDB and S3."""
    create_resp = requests.post(
        f"{API_URL}/items",
        json={"name": "Old Name", "description": "old desc"}
    )
    item_id = create_resp.json()["id"]

    resp = requests.put(
        f"{API_URL}/items/{item_id}",
        json={"name": "New Name", "description": "new desc"}
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "New Name"

    # Verify both stores were updated
    db_item = _get_db_item(item_id)
    s3_item = _get_s3_object(item_id)
    assert db_item["name"] == "New Name"
    assert db_item["description"] == "new desc"
    assert db_item == s3_item

    requests.delete(f"{API_URL}/items/{item_id}")


def test_put_nonexistent_returns_404():
    """PUT targeting a non-existing item returns 404."""
    resp = requests.put(
        f"{API_URL}/items/ghost-id-999",
        json={"name": "Ghost"}
    )
    assert resp.status_code == 404


# ── DELETE tests ─────────────────────────────────────────────────────

def test_delete_removes_from_db_and_s3():
    """DELETE removes the item from both DynamoDB and S3."""
    create_resp = requests.post(
        f"{API_URL}/items",
        json={"name": "Delete Me", "description": "bye"}
    )
    item_id = create_resp.json()["id"]

    resp = requests.delete(f"{API_URL}/items/{item_id}")
    assert resp.status_code == 200
    assert "deleted" in resp.json()["message"]

    # Verify gone from both stores
    assert _get_db_item(item_id) is None
    assert not _s3_object_exists(item_id)


def test_delete_nonexistent_returns_404():
    """DELETE on a non-existing item returns 404."""
    resp = requests.delete(f"{API_URL}/items/no-such-id-000")
    assert resp.status_code == 404
