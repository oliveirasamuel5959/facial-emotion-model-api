import streamlit as st
from PIL import Image
import numpy as np

import cv2

import requests
import json
import logging

from utils import image64_encode
from utils import send_image_api
from utils import get_predictions

st.title('Facial Emotion Recognition')

st.text('emotion detection using deep learning')

user_name = st.text_input('Enter your name:')
print(user_name)

st.write('Name:', user_name)

uploaded_image = st.file_uploader("Choose an image file", type="jpg")

if uploaded_image:
    image = Image.open(uploaded_image).convert('RGB')
    image_array = np.array(image)
    
    data = image64_encode(image, user_name)
    print(data['image']['content'][0:20])
    post_response = send_image_api(data)
    
    if post_response.status_code == 201:
        print("Successfully created data")    
    else:
        print(f"Error: {post_response.status_code} - {post_response.reason}")
        
    get_response = get_predictions(user_name)
    
    if get_response.status_code == 200:
        try:
            data = get_response.json()
            print(f"Data request response: {data}")
            x = data['image-props']['position'][0]
            y = data['image-props']['position'][1]
            width = data['image-props']['dimension'][0]
            height = data['image-props']['dimension'][1]
            image_array = cv2.rectangle(
                image_array, 
                (x, y), 
                (x + width, y + height), 
                (0, 255, 0), 
                2
            )
            image_array = cv2.putText(
                image_array, 
                f"{data['prediction']}", 
                (x + 30, y + height + 30), 
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )
            
            st.image(image_array, caption="Processed Image", use_container_width=True)
            
            st.text(f"Emotion: {data['prediction']}")
            st.text(f"Confidence: {data['accuracy']}")
            
        except Exception as e:
            logging.error(e)
    else:
        print(f"Error: {get_response.status_code} - {get_response.reason}")
        

    