FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy project specification files first for Docker layer caching
COPY pyproject.toml /app/

# Install all dependencies from pyproject.toml
RUN pip install --no-cache-dir "fastapi[standard]" "uvicorn[standard]" psycopg2-binary pydantic pydantic-settings sqlalchemy python-dotenv asyncpg

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]