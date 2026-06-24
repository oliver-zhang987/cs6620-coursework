from flask import Flask, jsonify, request
import threading

app = Flask(__name__)

# Threading lock for thread-safe in-memory operations
db_lock = threading.Lock()

# In-memory store
items = {
    1: {"id": 1, "name": "Item One", "description": "This is item one"},
    2: {"id": 2, "name": "Item Two", "description": "This is item two"}
}
next_id = 3

@app.route("/items", methods=["GET"])
def get_items():
    with db_lock:
        return jsonify(list(items.values())), 200

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    with db_lock:
        item = items.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route("/items", methods=["POST"])
def create_item():
    global next_id
    if not request.json or "name" not in request.json:
        return jsonify({"error": "Bad request, name is required"}), 400

    with db_lock:
        new_item = {
            "id": next_id,
            "name": request.json["name"],
            "description": request.json.get("description", "")
        }
        items[next_id] = new_item
        next_id += 1
    return jsonify(new_item), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    if not request.json:
        return jsonify({"error": "Bad request, json body is required"}), 400

    with db_lock:
        if item_id not in items:
            return jsonify({"error": "Item not found"}), 404
        item = items[item_id]
        item["name"] = request.json.get("name", item["name"])
        item["description"] = request.json.get("description", item["description"])
        return jsonify(item), 200

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    with db_lock:
        if item_id not in items:
            return jsonify({"error": "Item not found"}), 404
        del items[item_id]
        return jsonify({"message": f"Item {item_id} deleted successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
