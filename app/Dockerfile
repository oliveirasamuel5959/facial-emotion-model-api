FROM python:3.10-slim

WORKDIR /code

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN apt-get update && apt-get install -y curl pipx && \
    pipx install uv && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv && \
    apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 && \
    uv pip install --system --no-cache-dir -r requirements.txt

EXPOSE 8501

COPY . .

CMD ["streamlit", "run", "src/main.py", "--server.port=8501"]