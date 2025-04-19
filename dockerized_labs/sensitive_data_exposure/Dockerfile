# Stage 1: Builder
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && \
    useradd -r -g appuser -u 1001 appuser && \
    mkdir -p /app/static /app/media /app/logs /app/staticfiles && \
    chown -R appuser:appuser /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appuser . .

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=sensitive_data_lab.settings \
    CREATE_SUPERUSER=0 \
    CREATE_DEMO_USERS=1 \
    DEBUG=0

# Copy and secure entrypoint
COPY --chown=appuser:appuser entrypoint.sh /entrypoint.sh
RUN chmod 750 /entrypoint.sh

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "sensitive_data_lab.wsgi:application"]