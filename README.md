## **Table of Contents**
- [**Table of Contents**](#table-of-contents)
- [**How to Use**](#how-to-use)
  - [**Prerequisites**](#prerequisites)
  - [**Environment Variables**](#environment-variables)
  - [**Running the Application**](#running-the-application)
    - [**Local Development**](#local-development)
    - [**Docker Deployment**](#docker-deployment)
## **How to Use**
Instruction for setting up and running the REST API server.

### **Prerequisites**

- Python 3.10
- Docker
- Nginx

### **Environment Variables**
Create a .env file in the project root with the following variables:

````python
FLASK_APP=app_name
PORT=8080
````

### **Running the Application**

#### **Local Development**
1. Create the .env file as described above
2. Create a python virtual environment according to your preference
````python
python3 -m virtualenv .env
source .env/bin/activate
````
3. Install the dependencies of the application:
````python
pip install -r requirements.txt
````
4. Run the application with gunicorn wsgi:
````python
gunicorn --bind 0.0.0.0:8080 src.app:app
````
5. Open the browser in http://127.0.0.1:8080

#### **Docker Deployment**
1. Build the containers using docker-compose.yaml
````python
docker-compose up --build -d
````
2. Check images running and ports
````python
docker ps
````
3. Open the browser in http://127.0.0.1:8080
