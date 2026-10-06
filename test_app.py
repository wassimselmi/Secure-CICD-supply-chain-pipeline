"""
Unit tests for the Flask API (app.py).

Three tests:
  1. test_health_check         – GET /health returns 200 + correct payload
  2. test_get_items            – GET /items returns all items
  3. test_create_item_success  – POST /items creates a new item (201)
  4. test_create_item_missing_fields – POST /items without required fields (400)
"""

import json
import unittest

from app import app, _items


class APITestCase(unittest.TestCase):

    def setUp(self):
        """Configure Flask test client and reset in-memory state before each test."""
        app.config["TESTING"] = True
        self.client = app.test_client()

        # Reset the items list to a known state
        import app as api_module
        api_module._items.clear()
        api_module._items.extend([
            {"id": 1, "name": "Widget A", "category": "hardware"},
            {"id": 2, "name": "Widget B", "category": "software"},
        ])
        api_module._next_id = 3

    # ── Test 1 ──────────────────────────────
    def test_health_check(self):
        """GET /health should return 200 with status=ok."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["service"], "secure-api")

    # ── Test 2 ──────────────────────────────
    def test_get_items(self):
        """GET /items should return all seeded items."""
        response = self.client.get("/items")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["count"], 2)
        self.assertEqual(len(data["items"]), 2)

    # ── Test 3 ──────────────────────────────
    def test_create_item_success(self):
        """POST /items with valid payload should return 201 and the new item."""
        payload = {"name": "Gadget X", "category": "electronics"}
        response = self.client.post(
            "/items",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["name"], "Gadget X")
        self.assertEqual(data["category"], "electronics")
        self.assertIn("id", data)

    def test_create_item_missing_fields(self):
        """POST /items without required fields should return 400."""
        response = self.client.post(
            "/items",
            data=json.dumps({"name": "Incomplete"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
