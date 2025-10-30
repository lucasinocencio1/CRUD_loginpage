FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from project root (build context set to repo root)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy backend code
COPY backend/ /app

# Expose API port
EXPOSE 8000

# Default envs (override via compose)
ENV DB_HOST=db \
    DB_PORT=5432

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


