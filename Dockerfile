# docker build -t vertical-image-app .
# docker run --rm -d -p 8501:8501 -p 8000:8000 -p8282:8080 --name vertical-image-app vertical-image-app

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install supervisor for managing multiple services, and curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code and supervisor config
COPY . /app/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8501 8000 8080

# TODO Add Healtcheck for 8080 as well
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || curl --fail http://localhost:8000/docs || exit 1

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
