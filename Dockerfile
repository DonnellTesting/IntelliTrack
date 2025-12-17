FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# System deps (safe minimal set)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (won't crash if none)
RUN python manage.py collectstatic --noinput || true

# Cloud Run entrypoint
CMD gunicorn ojt_tracker.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4