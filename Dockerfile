FROM python:3.10

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "--config", "gunicorn_config.py", "src.app:app"]