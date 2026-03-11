FROM python:3.11-slim

# Container working directory.
WORKDIR /app

# Install runtime dependencies first for better layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service source code.
COPY . .

# Run the FastAPI app on the default Cloud Run port.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
