"""
Simple Flask API with two endpoints:
  GET  /health  – returns service health status
  GET  /items   – returns a list of items (supports ?category= filter)
  POST /items   – creates a new item
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory store (reset on each run)
_items: list[dict] = [
    {"id": 1, "name": "Widget A", "category": "hardware"},
    {"id": 2, "name": "Widget B", "category": "software"},
]
_next_id = 3


# ──────────────────────────────────────────
# Endpoint 1 – Health check
# ──────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    """Return a simple health-check payload."""
    return jsonify({"status": "ok", "service": "secure-api"}), 200


# ──────────────────────────────────────────
# Endpoint 2 – Items resource
# ──────────────────────────────────────────
@app.route("/items", methods=["GET"])
def get_items():
    """
    Return all items.
    Optional query param: ?category=<value>
    """
    category = request.args.get("category")
    if category:
        result = [i for i in _items if i["category"] == category]
    else:
        result = _items
    return jsonify({"items": result, "count": len(result)}), 200


@app.route("/items", methods=["POST"])
def create_item():
    """
    Create a new item.
    Expected JSON body: { "name": "...", "category": "..." }
    """
    global _next_id
    data = request.get_json(silent=True)
    if not data or "name" not in data or "category" not in data:
        return jsonify({"error": "Both 'name' and 'category' are required."}), 400

    item = {"id": _next_id, "name": data["name"], "category": data["category"]}
    _items.append(item)
    _next_id += 1
    return jsonify(item), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
