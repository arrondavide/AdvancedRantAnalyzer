# Use a lightweight Python base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for writable directories
ENV TRANSFORMERS_CACHE=/workspace/cache
ENV NLTK_DATA=/workspace/nltk_data

# Create writable directories
RUN mkdir -p /workspace/cache /workspace/nltk_data

# Set working directory
WORKDIR /workspace

# Copy requirements.txt for dependency installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application codebase
COPY . .

# Expose port for application
EXPOSE 8000