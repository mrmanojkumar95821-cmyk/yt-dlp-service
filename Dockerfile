FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Render automatically sets PORT → don't hardcode
EXPOSE 5000

# Set default port for local debugging (Render overrides)
ENV PORT=5000

# Run app using gunicorn
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
