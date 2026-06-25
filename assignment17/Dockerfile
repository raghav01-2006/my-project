# Use python:3.12-slim as the base image
FROM python:3.12-slim

# Install OpenJDK (required for running PySpark JVM backend)
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy python script and dataset
COPY assignment17.py .
COPY sales.csv .

# Execute the PySpark application automatically when the container starts
CMD ["python", "assignment17.py"]
