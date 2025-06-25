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
from utils import get_face_position
from utils import get_face_rect

st.title('Facial Emotion Recognition')

st.text('emotion detection using deep learning')

user_name = st.text_input('Enter your name:')
print(user_name)

st.write('Name:', user_name)

uploaded_image = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

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
    
    predict_btn = st.button("Predict", type="primary")
    
    if predict_btn:
        get_response = get_predictions(user_name)
        if get_response.status_code == 200:
            try:
                data = get_response.json()
                print(f"Data request response: {data}")
                
                get_face_rect(data=data, image_array=image_array)
                
                st.text(f"Emotion: {data['prediction']}")
                st.text(f"Confidence: {data['accuracy']}")
                
            except Exception as e:
                logging.error(f"Error status code {e}")
        else:
            print(f"Error: {get_response.status_code} - {get_response.reason}")
    else:
        st.text("use the button to predict image emotion.")
    
        

    