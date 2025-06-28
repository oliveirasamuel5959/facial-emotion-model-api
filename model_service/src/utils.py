import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

import base64
from PIL import Image
from io import BytesIO

import logging
logging.basicConfig(filename='./model_service.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

detect = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')

def crop_face(frame, pos, dim):
    faces = frame[pos[1]:pos[1] + dim[1], pos[0]: pos[0] + dim[0]]
    return faces

def face_detect(image_array):
    faces_array = []
    logging.info(f"Start face detection. Image shape is {image_array.shape}.")
    gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    gray_image = gray_image.astype('uint8')
    faces = detect.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    
    if len(faces) == 0:
        logging.info(f"face not found for image {gray_image.shape}.")
    else:
        logging.info(f"face(s) positions and dimensions {faces}.")
        logging.info(f"faces(s) return shape {faces.shape}.")
        
        num_faces = faces.shape[0]
        
        for (x, y, w, h) in faces:
            pos = (int(x), int(y))
            dim = (int(w), int(h))
            
            cv2.rectangle(image_array, (x, y), (x + w, y + h), (0, 255, 0), 3)
            face_image = crop_face(image_array, pos=pos, dim=dim)
            
            faces_array.append(face_image)
            
        cv2.imwrite("images/face_image.png", image_array)
        
        logging.info(f"Completed face detection. Face shape {faces} and found {num_faces} face(s).")    
        return faces_array, num_faces, faces.tolist()
        
def image_preprocessing(face_image):
    image_list = []
    try:
        logging.info("Start image preprocessing...")
        for i in range(len(face_image)):
            logging.info(f"Start image preprocessing for face {i + 1}")
            image = cv2.resize(face_image[i], (224, 224))
            image = tf.keras.preprocessing.image.img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = image / 255.0  # Normalize
            logging.info(f"Completed image preprocessing for face {i + 1}. Image shape is {image.shape}.")    
            image_list.append(image)
        logging.info(f"Completed image preprocessing for {len(face_image)} images.")
        return image_list
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