# ─────────────────────────────────────────────────────────────────────────────
# Stage 1 – Builder
#   Full Python image used only to install dependencies into a clean prefix.
#   Nothing from this stage leaks into the final image.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /install

# Copy only the dependency manifest first (layer-cache friendly)
COPY requirements.txt .

# Install into an isolated directory so we can copy it cleanly later
RUN pip install --no-cache-dir --prefix=/install/deps -r requirements.txt


# ─────────────────────────────────────────────────────────────────────────────
# Stage 2 – Runtime  (slim, non-root)
#   Only the installed packages + application code land here.
#   No build tools, no pip, no root shell.
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# ── Security: create a dedicated non-root user ────────────────────────────────
RUN groupadd --gid 1001 appgroup && \
    useradd  --uid 1001 --gid appgroup --no-create-home --shell /sbin/nologin appuser

WORKDIR /app

# ── Copy installed site-packages from the builder stage ──────────────────────
COPY --from=builder /install/deps /usr/local

# ── Copy only application source (no tests, no dev files) ────────────────────
COPY app.py .

# ── Drop to non-root before the process starts ───────────────────────────────
USER appuser

# Flask will listen on all interfaces inside the container
ENV FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

# Prefer the explicit python invocation so PID 1 is the app, not a shell
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
