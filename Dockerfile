# Use a lightweight Python base image
FROM python:3.9-slim

# Set environment variables for writable directories
ENV TRANSFORMERS_CACHE=/workspace/cache
ENV NLTK_DATA=/workspace/nltk_data

# Create writable directories
RUN mkdir -p /workspace/cache /workspace/nltk_data

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Download Spacy model if required
RUN python -m spacy download en_core_web_md

# Copy the application codebase
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Command to start the FastAPI app with debugging logs enabled
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]