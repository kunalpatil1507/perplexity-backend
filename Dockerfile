# Use official Python slim image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install build dependencies only if you need them (optional)
# RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first (use Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# [Optional] Make sure sentence-transformers is in requirements.txt,
# OR install it explicitly here if not already in requirements.txt
# RUN pip install sentence-transformers

# Pre-download the embedding model into the container's cache
# This avoids runtime download failures when no internet access
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy the rest of your FastAPI app code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
