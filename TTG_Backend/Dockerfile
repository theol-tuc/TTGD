# syntax=docker/dockerfile:1

# --- Builder stage (for future extensibility, e.g., compiling dependencies) ---
FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Final stage ---
FROM python:3.10-slim

# Create a non-root user
RUN useradd -m appuser
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy backend code
COPY . ./

# Set environment variables (use .env for secrets in production)
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose FastAPI port
EXPOSE 8000

# Switch to non-root user
USER appuser

# Healthcheck (optional, for production)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/docs || exit 1

# Run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"] 