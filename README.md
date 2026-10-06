# Secure CI/CD Supply Chain Pipeline – API

[![CI](https://github.com/wassimselmi/Secure-CICD-supply-chain-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/wassimselmi/Secure-CICD-supply-chain-pipeline/actions/workflows/ci.yml)

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
├── app.py              # Flask application (2 endpoints)
├── test_app.py         # Unit tests (4 test cases)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Multi-stage, slim runtime, non-root user  ✅
├── Dockerfile.naive    # Single-stage baseline (size comparison only)
├── .dockerignore       # Excludes tests, venv, secrets from build context
└── README.md
```

---

## Docker

### Multi-stage build (production-ready)

The `Dockerfile` uses two stages:

| Stage | Base image | Purpose |
|-------|-----------|---------|
| **builder** | `python:3.12-slim` | Installs dependencies into an isolated prefix |
| **runtime** | `python:3.12-slim` | Copies only the installed packages + `app.py` |

Security hardening applied in the runtime stage:
- Dedicated non-root user `appuser` (UID/GID 1001) — no shell, no home dir
- `PYTHONDONTWRITEBYTECODE=1` + `PYTHONUNBUFFERED=1` for clean logs
- No build tools, no pip, no package manager in the final image

```bash
# Build the optimised multi-stage image
docker build -t secure-api:slim .

# Build the naive baseline (for size comparison)
docker build -f Dockerfile.naive -t secure-api:naive .

# Compare sizes
docker images secure-api

# Run the optimised image
docker run -p 5000:5000 secure-api:slim
```

### .dockerignore

`.dockerignore` keeps the build context lean by excluding:
- Virtual environments (`.venv/`, `venv/`)
- Test files (`test_app.py`, `.pytest_cache/`)
- Editor / OS noise (`.idea/`, `.DS_Store`, …)
- Secrets (`.env`, `*.pem`, `*.key`)
- CI configs and documentation

### 📊 Image size comparison (measured)

| Image | Base | Stages | Runs as | Size |
|-------|------|--------|---------|------|
| `secure-api:naive` | `python:3.12` | 1 (single-stage) | root | **1.12 GB** |
| `secure-api:slim` | `python:3.12-slim` | 2 (multi-stage) | `appuser` (uid 1001) | **124 MB** |

> **~9× smaller** — from 1.12 GB down to 124 MB.  
> The slim image also runs as a non-root user with no shell, no pip, and no build tools.

---

## CI/CD Pipeline (GitHub Actions)

Workflow: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

Three jobs run in sequence on every push/PR to `main`:

```
lint  ──►  test  ──►  build (Docker)
```

| Job | What it does | Matrix |
|-----|-------------|--------|
| **lint** | Runs `flake8` against `app.py` and `test_app.py` | Python 3.11 & 3.12 |
| **test** | Runs all unit tests with `unittest` | Python 3.11 & 3.12 |
| **build** | Multi-stage Docker build + verifies non-root user | — |

### Caching strategy

| Cache | Key |
|-------|-----|
| `pip` downloads (lint) | OS + Python version + `requirements*.txt` hash |
| `pip` downloads (test) | OS + Python version + `requirements.txt` hash |
| Docker BuildKit layers | OS + commit SHA (with fallback restore) |

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
