import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

import base64
from PIL import Image
from io import BytesIO

def crop_face(frame, pos, dim):
    '''
    pos = [x, y]
    dim = [w, h]
    '''
    faces = frame[pos[1]:pos[1] + dim[1], pos[0]: pos[0] + dim[0]]
    return faces

def face_detec(image_path='None', image_array='None'):
    #image = cv2.imread(image_path)
    detec = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    face = detec.detectMultiScale(gray, 1.3, 3)
    
    for (x, y, w, h) in face:
        pos = [x, y]
        dim = [w, h]
        
        cv2.rectangle(image_array, (x, y), (x + w, y + h), (0, 255, 0), 3)
        face = crop_face(image_array, pos=pos, dim=dim)
        
    cv2.imwrite('images/face_image.png', image_array)
    cv2.imwrite('images/face_crop_image.png', face)
    
    return face
    
    
def image_preprocessing(face_image):
    try:
        image = cv2.resize(face_image, (224, 224))
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = image / 255.0  # Normalize
        return image
    except Exception as e:
        raise ValueError("Invalid image data") from e
    

def image64_decode(image_post_data):
    image_pil = Image.open(BytesIO(base64.b64decode(image_post_data['images'][0]['content'])))
    cv2_image = np.array(image_pil)    
    image_pil.save('images/post_image.jpg', 'JPEG')    
    return cv2_image