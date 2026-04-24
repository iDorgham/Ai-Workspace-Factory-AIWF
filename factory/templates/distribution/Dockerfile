# 🐳 AIWF Shard Dockerfile (v1.0.0)
# Multi-stage build for OMEGA-tier efficiency

# Stage 1: Build & Dependencies
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production Runtime
FROM python:3.11-slim
WORKDIR /app

# Compliance: Non-root user enforcement
RUN useradd -m aiwf
USER aiwf

# Copy dependencies and core factory logic
COPY --from=builder /home/aiwf/.local /home/aiwf/.local
COPY factory/ /app/factory/
COPY .env.production .env

ENV PATH=/home/aiwf/.local/bin:$PATH
EXPOSE 8080

ENTRYPOINT ["python", "factory/core/runner.py"]
CMD ["swarm"]
