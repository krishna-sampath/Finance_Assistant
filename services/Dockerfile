FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy service code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command (override per service in docker-compose)
CMD ["uvicorn", "services.api_service:app", "--host", "0.0.0.0", "--port", "8001"]
