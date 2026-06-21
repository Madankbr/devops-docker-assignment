from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # allow requests from the Express frontend (different origin/port)

# ---- MongoDB connection ----
# MONGO_URI is supplied via environment variable (set in docker-compose.yml).
# Falls back to local MongoDB Atlas-style connection string if not set.
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/assignmentDB")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.get_database()
    collection = db["submissions"]
    client.server_info()  # force connection check
    print("✅ Connected to MongoDB successfully.")
except Exception as e:
    print(f"⚠️  MongoDB connection failed: {e}")
    collection = None


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Flask Backend",
        "status": "running",
        "message": "Flask backend is up. POST form data to /submit"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/submit", methods=["POST"])
def submit_form():
    """
    Handles form submission coming from the Express/Node.js frontend.
    Accepts both JSON and standard form-encoded data.
    """
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email:
            return jsonify({"error": "Name and email are required fields."}), 400

        record = {
            "name": name,
            "email": email,
            "message": message or "",
            "submitted_at": datetime.utcnow().isoformat()
        }

        if collection is not None:
            result = collection.insert_one(record)
            record["_id"] = str(result.inserted_id)
            return jsonify({
                "success": True,
                "message": "Form submitted and saved to MongoDB successfully!",
                "data": record
            }), 201
        else:
            return jsonify({
                "success": False,
                "message": "Form received but MongoDB is not connected.",
                "data": record
            }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api", methods=["GET"])
def get_submissions():
    """Returns all stored submissions (useful for verifying DB writes)."""
    try:
        if collection is None:
            return jsonify({"error": "MongoDB not connected"}), 503
        docs = list(collection.find())
        for d in docs:
            d["_id"] = str(d["_id"])
        return jsonify(docs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
