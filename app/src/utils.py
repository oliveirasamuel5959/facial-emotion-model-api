import base64
import json
import requests
from io import BytesIO
import logging

import streamlit as st

import cv2

logger = logging.getLogger(__name__)

URL = 'http://emovio.com.br/api/v1/predictions'
headers = {'content-type': 'application/json'}

def image64_encode(base_image, name):
    try:
        buffered = BytesIO()
        base_image.save(buffered, format='JPEG')
        
        image_bytes = buffered.getvalue()
        base64_bytes = base64.b64encode(image_bytes)
        base64_encoded = base64_bytes.decode()
        
        data = {
            'image':
                {
                    'name': str(name),
                    'timestamp': 1215456,
                    'content': base64_encoded
                },
            'collection_name': 'Image base64 for data analysis'
        }

        return data
        
    except Exception as e:
        print("Error: ", e)
    

def send_image_api(data_json):
    response = requests.post(url=URL, data=json.dumps(data_json), headers=headers)
    return response    
    
def get_predictions(name):
    response = requests.get(url=f'http://emovio.com.br/api/v1/predictions/{name}', headers=headers)
    return response

def get_face_position(data):
    num_of_faces = data["image-props"]["num_of_faces"]
    if num_of_faces == 1:
        x = data['image-props']['faces_positions'][0][0]
        y = data['image-props']['faces_positions'][0][1]
        width = data['image-props']['faces_positions'][0][2]
        height = data['image-props']['faces_positions'][0][3]
        
        return x, y, width, height
    
def get_face_rect(data, image_array):
    num_of_faces = data["image-props"]["num_of_faces"]
    class_and_accuracy = list(zip(data["prediction"], data["accuracy"]))
    class_and_position = list(zip(data["prediction"], data["image-props"]["faces_positions"]))
    
    print("class and accuracy:", class_and_accuracy)
    print("class and position:", class_and_position)
    
    for i in range(num_of_faces):
        x = class_and_position[i][1][0]
        y = class_and_position[i][1][1]
        width = class_and_position[i][1][2]
        height = class_and_position[i][1][3]
        
        image_array = cv2.rectangle(
            image_array, 
            (class_and_position[i][1][0], class_and_position[i][1][1]), 
            (x + width, y + height), 
            (0, 255, 0), 
            2
        )
        
        image_array = cv2.putText(
            image_array, 
            f"{class_and_position[i][0]}", 
            (x + 30, y + height + 30), 
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )
        
    st.image(image_array, caption="Processed Image", use_container_width=True)
        