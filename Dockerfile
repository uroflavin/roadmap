# Multi-stage build for optimized image size and security
# This Dockerfile builds a Python application named "roadmap"

# ====================================
# Builder Stage
# ====================================

FROM cgr.dev/chainguard/python:latest-dev as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --user

# ====================================
# Final Stage
# ====================================

# Use a slimmer Python image for smaller container size
FROM cgr.dev/chainguard/python:latest
WORKDIR /app

# Copies only installed dependencies from the builder stage, reducing image size.
COPY --from=builder /home/nonroot/.local/lib/python3.12/site-packages /home/nonroot/.local/lib/python3.12/site-packages

# Copy application and resources
COPY helloworld.py .

COPY roadmap.py .
COPY roadmap.env .

# Copy additional data folders
COPY schema /app/schema
COPY templates /app/templates

# Define volumes for persistent data
VOLUME /app/working

# Set default command to run the script
ENTRYPOINT [ "python", "/app/roadmap.py" ]
