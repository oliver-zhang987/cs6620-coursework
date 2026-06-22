import os
import sys
import pytest

# Add src folder to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app, items

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Save a backup of in-memory data
        original_items = items.copy()
        yield client
        # Restore state after each test run
        items.clear()
        items.update(original_items)

def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["name"] == "Item One"

def test_get_item_success(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Item One"

def test_get_item_not_found(client):
    response = client.get("/items/99")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_create_item_success(client):
    new_data = {"name": "Test Item", "description": "This is a test"}
    response = client.post("/items", json=new_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data["id"] == 3
    assert data["name"] == "Test Item"
    
    # Check that it's added
    get_res = client.get("/items/3")
    assert get_res.status_code == 200

def test_create_item_invalid(client):
    # Missing name
    invalid_data = {"description": "no name"}
    response = client.post("/items", json=invalid_data)
    assert response.status_code == 400

def test_update_item_success(client):
    update_data = {"name": "Updated Name", "description": "Updated description"}
    response = client.put("/items/1", json=update_data)
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["name"] == "Updated Name"
    assert data["description"] == "Updated description"

def test_update_item_not_found(client):
    response = client.put("/items/99", json={"name": "Ghost"})
    assert response.status_code == 404

def test_delete_item_success(client):
    response = client.delete("/items/1")
    assert response.status_code == 200
    data = response.get_json()
    assert "deleted" in data["message"]
    
    # Verify it is deleted
    get_res = client.get("/items/1")
    assert get_res.status_code == 404

def test_delete_item_not_found(client):
    response = client.delete("/items/99")
    assert response.status_code == 404
