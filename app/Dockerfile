FROM python:3.10

WORKDIR /code

COPY requirements.txt .

RUN apt-get update && apt-get install -y curl pipx && \
    pipx install uv && \
    ln -s /root/.local/bin/uv /usr/local/bin/uv

RUN uv pip install --system --no-cache-dir -r requirements.txt

EXPOSE 8501

COPY . .

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false", "--server.headless=true"]