# docker build -t insta-reel-cropper .
# docker run -d --name insta-reel-cropper insta-reel-cropper

# Use the official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install only curl for healthcheck, clean up apt cache in same layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && rm -rf /var/lib/apt/lists/*

# Copy requirements directly (create requirements.txt)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . /app/

# Expose Streamlit's default port
EXPOSE 8501

# Add healthcheck: checks if the app is responding on port 8501
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--browser.gatherUsageStats=false", "--server.port=8501", "--server.address=0.0.0.0"]
