# backend/Dockerfile
FROM python:3.11-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (包含 Ollama 需要的 curl)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip show django

# Copy project
COPY . .

# Copy and set permissions for start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose ports for Django and Ollama
EXPOSE 8001 11434

# Use start script as entry point
CMD ["/start.sh"]