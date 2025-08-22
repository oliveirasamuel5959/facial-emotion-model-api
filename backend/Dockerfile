FROM python:3.10-slim-bookworm

WORKDIR /app

COPY .env /app/.env

# Copy first to cache 
COPY requirements.txt .

RUN apt-get update -y && \
        apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        libgl1 \
        libglib2.0-0 && \
        pip install --no-cache-dir -r requirements.txt     

# Ensure pip-installed CLI tools like `uvicorn` are accessible
ENV PATH="/root/.local/bin:$PATH"

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]