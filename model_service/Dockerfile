FROM python:3.10

WORKDIR /app

# Copy first to cache 
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8080", "src.app:app"]