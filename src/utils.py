import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras

def crop_face(frame, pos, dim):
    '''
    pos = [x, y]
    dim = [w, h]
    '''
    faces = frame[pos[1]:pos[1] + dim[1], pos[0]: pos[0] + dim[0]]
    return faces

def face_detec(image_path):
    image = cv2.imread(image_path)
    detec = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = detec.detectMultiScale(gray, 1.3, 3)
    
    for (x, y, w, h) in face:
        pos = [x, y]
        dim = [w, h]
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        face = crop_face(image, pos=pos, dim=dim)
        
    cv2.imwrite('images/face_image.png', image)
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
    
