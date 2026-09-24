# ---------------------------------------------------------
# FastBox Mystery Delivery System - Production Dockerfile
# ---------------------------------------------------------

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install security updates and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and data
COPY src/ /app/src/
COPY web/ /app/web/
COPY tests/ /app/tests/
COPY data/ /app/data/
COPY main.py /app/main.py
COPY dashboard.py /app/dashboard.py
COPY run_tests.py /app/run_tests.py
COPY data.json /app/data.json

# Create outputs directory
RUN mkdir -p /app/outputs

# Create a non-root user for security
RUN useradd -m -u 1000 fastbox && \
    chown -R fastbox:fastbox /app

USER fastbox

# Expose web dashboard port if running static web server
EXPOSE 8080

# Default command: Run the delivery simulation
CMD ["python", "main.py"]

