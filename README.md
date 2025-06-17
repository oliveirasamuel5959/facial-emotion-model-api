## **Facial Emotion Recognition Flask API**

## **Table of Contents**

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
#### Local Development
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
