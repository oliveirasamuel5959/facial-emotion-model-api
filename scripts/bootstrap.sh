#!bin/bash

export FLASK_APP=./src/app.py
flask --app src/app run

# WSGI
gunicorn --config gunicorn_config.py src.app:app

# Docker
docker run -it --name {container name} -p 8080:8080 {image name}