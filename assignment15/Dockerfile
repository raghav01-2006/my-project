# Use python:3.12-slim as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy the Python script into the container
COPY assignment15.py .

# Run the script when the container starts
CMD ["python", "assignment15.py"]
