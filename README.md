# Secure CI/CD Supply Chain Pipeline – API

A minimal **Flask REST API** that demonstrates two endpoints and is fully covered by unit tests. It forms the foundation for the Secure CI/CD supply-chain pipeline project.

---

## Endpoints

| Method | Path      | Description                                           |
|--------|-----------|-------------------------------------------------------|
| `GET`  | `/health` | Health-check – returns `{ "status": "ok" }`           |
| `GET`  | `/items`  | List all items. Supports `?category=<value>` filter   |
| `POST` | `/items`  | Create a new item. Body: `{ "name", "category" }`     |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/wassimselmi/Secure-CICD-supply-chain-pipeline.git
cd Secure-CICD-supply-chain-pipeline

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the API
python app.py
```

The server will be available at `http://localhost:5000`.

---

## Running Tests

```bash
python -m pytest test_app.py -v
# or using the built-in runner
python -m unittest test_app -v
```

---

## Project Structure

```
.
├── app.py           # Flask application (endpoints)
├── test_app.py      # Unit tests (3 test cases)
├── requirements.txt # Python dependencies
└── README.md
```

---

## API Examples

```bash
# Health check
curl http://localhost:5000/health

# List all items
curl http://localhost:5000/items

# Filter by category
curl "http://localhost:5000/items?category=hardware"

# Create a new item
curl -X POST http://localhost:5000/items \
     -H "Content-Type: application/json" \
     -d '{"name": "Gadget X", "category": "electronics"}'
```
