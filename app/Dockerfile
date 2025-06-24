FROM python:3.10

WORKDIR /code

COPY requirements.txt .

RUN apt-get update && apt-get install -y curl pipx && \
    pipx install uv && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv

RUN apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0

RUN uv pip install --system --no-cache-dir -r requirements.txt

EXPOSE 8501

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["streamlit", "run", "src/main.py", "--server.port=8501"]