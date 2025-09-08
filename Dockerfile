FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY examples/ ./examples/
COPY tests/ ./tests/
COPY auto_setup_enhanced.py .
COPY simple_listener.py .
COPY simple_processor.py .
COPY send_message.py .

# Make scripts executable
RUN chmod +x auto_setup_enhanced.py

# Set Python path
ENV PYTHONPATH=/app/src

# Default command
CMD ["python", "auto_setup_enhanced.py"]



