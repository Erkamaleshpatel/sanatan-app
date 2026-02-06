# Use official Python runtime as base image
FROM python:3.11-slim

# Install system dependencies required by MoviePy
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 10000

# Set environment variable
ENV PORT=10000

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--workers", "1", "--timeout", "300", "--chdir", "/app", "web.app:app"]
