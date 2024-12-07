FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies if needed (optional example)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (including app code, scripts, and CSV)
COPY . .

# Expose the port your FastAPI app runs on
EXPOSE 8080

# If you want to run init_data from this image for your init_data service:
# Just make sure python scripts/init_data.py can access cars.csv

# For the main API server, default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
