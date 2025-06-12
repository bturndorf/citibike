FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies with --break-system-packages flag
RUN pip install --break-system-packages -r requirements.txt

# Copy the rest of the application
COPY . .

# Change to backend directory
WORKDIR /app/backend

# Expose the port
EXPOSE 8080

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"] 