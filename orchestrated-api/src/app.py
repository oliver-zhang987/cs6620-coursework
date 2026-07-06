from flask import Flask, jsonify, request
import boto3
import os
import json
import uuid

app = Flask(__name__)

# AWS / LocalStack config from environment
endpoint_url = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url, region_name=region)
s3 = boto3.client("s3", endpoint_url=endpoint_url, region_name=region)

TABLE_NAME = "items"
BUCKET_NAME = "items-bucket"

table = dynamodb.Table(TABLE_NAME)


@app.route("/health")
def health():
    """Simple health check — also makes sure the DynamoDB table is reachable."""
    try:
        table.load()
        return jsonify({"status": "ok"}), 200
    except Exception:
        return jsonify({"status": "unhealthy"}), 503


@app.route("/items", methods=["GET"])
def get_items():
    result = table.scan()
    return jsonify(result.get("Items", [])), 200


@app.route("/items/<item_id>", methods=["GET"])
def get_item(item_id):
    result = table.get_item(Key={"id": item_id})
    item = result.get("Item")
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route("/items", methods=["POST"])
def create_item():
    if not request.json or "name" not in request.json:
        return jsonify({"error": "Bad request, name is required"}), 400

    # Duplicate check — scan for existing item with same name
    scan = table.scan(
        FilterExpression="#n = :name",
        ExpressionAttributeNames={"#n": "name"},
        ExpressionAttributeValues={":name": request.json["name"]}
    )
    if scan.get("Items"):
        return jsonify({"error": "Item with this name already exists"}), 409

    item_id = str(uuid.uuid4())
    new_item = {
        "id": item_id,
        "name": request.json["name"],
        "description": request.json.get("description", "")
    }

    # Store in DynamoDB
    table.put_item(Item=new_item)

    # Store in S3 as a JSON object
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=item_id,
        Body=json.dumps(new_item),
        ContentType="application/json"
    )

    return jsonify(new_item), 201


@app.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    if not request.json:
        return jsonify({"error": "Bad request, JSON body is required"}), 400

    result = table.get_item(Key={"id": item_id})
    if "Item" not in result:
        return jsonify({"error": "Item not found"}), 404

    item = result["Item"]
    item["name"] = request.json.get("name", item["name"])
    item["description"] = request.json.get("description", item["description"])

    # Update DynamoDB
    table.put_item(Item=item)

    # Overwrite S3 object
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=item_id,
        Body=json.dumps(item),
        ContentType="application/json"
    )

    return jsonify(item), 200


@app.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    result = table.get_item(Key={"id": item_id})
    if "Item" not in result:
        return jsonify({"error": "Item not found"}), 404

    table.delete_item(Key={"id": item_id})
    s3.delete_object(Bucket=BUCKET_NAME, Key=item_id)

    return jsonify({"message": f"Item {item_id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
