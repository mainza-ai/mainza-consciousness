# Mainza Consciousness System - Backend Dockerfile
FROM python:3.11-slim

# Cache busting arguments
ARG CACHE_BUST=1
ARG BUILD_DATE
ARG GIT_COMMIT

# Install system dependencies including build tools
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    curl \
    build-essential \
    g++ \
    gcc \
    libc6-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
# Use production requirements to include ML/audio deps (whisper, torch, etc.)
COPY requirements-docker.txt ./requirements.txt

# Install Python dependencies (this layer will be cached if requirements don't change)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend source code (this layer will be rebuilt when source changes)
COPY backend/ ./backend/

# Add build information and environment variables
RUN echo "Cache bust: $CACHE_BUST" && \
    echo "Build date: $BUILD_DATE" && \
    echo "Git commit: $GIT_COMMIT" && \
    echo "Backend build completed successfully"

# Set build environment variables
ENV BUILD_DATE=$BUILD_DATE
ENV GIT_COMMIT=$GIT_COMMIT
ENV CACHE_BUST=$CACHE_BUST

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash mainza
RUN chown -R mainza:mainza /app
USER mainza

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"] 