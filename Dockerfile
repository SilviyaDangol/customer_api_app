FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy project specification files
COPY pyproject.toml /app/

# Install dependencies
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" psycopg2-binary pydantic pydantic-settings sqlalchemy python-dotenv

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
