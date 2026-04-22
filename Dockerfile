# Use a minimal Python 3.11 base image to reduce attack surface and image size
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Cloud Run injects PORT env var; default to 8080
ENV PORT=8080
EXPOSE 8080

# Run with Gunicorn (production WSGI server), 2 workers for concurrency
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
