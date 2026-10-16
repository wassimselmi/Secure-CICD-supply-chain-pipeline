# ─────────────────────────────────────────────────────────────────────────────
# ⚠️  DELIBERATELY VULNERABLE — vuln-test branch only
#
# Changes vs production Dockerfile (on main):
#   1. Base image: python:3.8-slim  ← EOL as of Oct 2024; ~30 unfixed OS CVEs
#      (vs python:3.12-slim on main)
#   2. Installs cryptography==38.0.0 via requirements.txt
#      CVE-2023-23931  CRITICAL  CVSS 9.1  fixed in >=39.0.1
#
# PURPOSE: confirm that the Trivy gates in the CI pipeline block this image
# from being pushed. This file MUST NOT be merged to main.
# ─────────────────────────────────────────────────────────────────────────────

# ── Stage 1: Builder ─────────────────────────────────────────────────────────
# 🔴 python:3.8-slim is deliberately old (EOL).
# Trivy will flag OS-level CVEs (openssl, glibc, etc.) with fixes available.
FROM python:3.8-slim AS builder

WORKDIR /install

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install/deps -r requirements.txt


# ── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM python:3.8-slim AS runtime

RUN groupadd --gid 1001 appgroup && \
    useradd  --uid 1001 --gid appgroup --no-create-home --shell /sbin/nologin appuser

WORKDIR /app

COPY --from=builder /install/deps /usr/local
COPY app.py .

USER appuser

ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
