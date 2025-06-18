#!bin/bash

export FLASK_APP=./src/app.py
flask --app src/app run

# WSGI
gunicorn --config gunicorn_config.py src.app:app

# Docker
docker run -p 8080:8080 {image name}

# Curl
curl "

# nginx ssl https letsencrypt certificate
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d emovio.com.br