import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

import base64
from PIL import Image
from io import BytesIO

import logging
logging.basicConfig(filename='./model_service.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def crop_face(frame, pos, dim):
    faces = frame[pos[1]:pos[1] + dim[1], pos[0]: pos[0] + dim[0]]
    return faces

def face_detect(image_array):
    # image_array = cv2.resize(image_array, (367, 367))
    logging.info(f"Start face detection. Image shape is {image_array.shape}.")
    gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    gray_image = gray_image.astype('uint8')
    detect = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')
    face = detect.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    
    if face is None:
        logging.info(f"face not found for image {gray_image.shape}.")
    else:
        for (x, y, w, h) in face:
            pos = (int(x), int(y))
            dim = (int(w), int(h))
            
            cv2.rectangle(image_array, (x, y), (x + w, y + h), (0, 255, 0), 3)
            face = crop_face(image_array, pos=pos, dim=dim)
            
        cv2.imwrite("images/face_image.png", image_array)
        
        logging.info(f"Completed face detection. Face shape {face.shape} and found {len(face)} face(s).")    
        return face, pos, dim
    
    
def image_preprocessing(face_image):
    try:
        logging.info("Start image preprocessing...")
        image = cv2.resize(face_image, (224, 224))
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = image / 255.0  # Normalize
        logging.info(f"Completed image preprocessing. Image shape is {image.shape}.")    
        return image
    except Exception as e:
        logging.error("Invalid image data.")
        logging.exception(e)
    

def image64_decode(image_post_data):
    logging.info("Start image decoding from base64 to PIL ndarray")
    image = Image.open(BytesIO(base64.b64decode(image_post_data['image']['content'])))
    image_array = np.array(image)    
    image.save('images/post_image.jpg', 'JPEG')
    logging.info(f"Completed image decoding. Image shape is {image_array.shape}.")    
    return image_array