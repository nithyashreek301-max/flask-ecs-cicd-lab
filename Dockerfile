# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy requirements first — better Docker layer caching
# (pip install only re-runs when requirements.txt changes, not on every code change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Run as non-root user (security best practice)
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 5000

# Use gunicorn for production (not Flask dev server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
