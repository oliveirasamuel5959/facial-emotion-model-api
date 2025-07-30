import base64
import json
import logging
import os
from io import BytesIO

import cv2
import numpy as np
import requests
import tensorflow as tf
from PIL import Image

URL_POST = "https://ai.emovio.com.br/api/v1/predictions"
URL_GET = "https://ai.emovio.com.br/api/v1/predictions/Samuel"

# URL_POST_LOCAL = 'http://192.168.0.16/v1/predictions'
# URL_GET_LOCAL = 'http://192.168.0.16/v1/predictions/Samuel'

headers = {"content-type": "application/json"}

logging.basicConfig(
    filename="face.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

detect = cv2.CascadeClassifier("model/haarcascade_frontalface_default.xml")

if os.path.exists("model/haarcascade_frontalface_default.xml"):
    print("The path exists.")
else:
    print("The path does not exist.")


def crop_face(frame, pos, dim):
    """
    pos = [x, y]
    dim = [w, h]
    """
    faces = frame[pos[1] : pos[1] + dim[1], pos[0] : pos[0] + dim[0]]
    return faces


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
            logging.info(
                f"Completed image preprocessing for face {i + 1}. Image shape is {image.shape}."
            )
            image_list.append(image)
        logging.info(f"Completed image preprocessing for {len(face_image)} images.")
        return image_list
    except Exception as e:
        logging.error("Invalid image data.")
        logging.exception(e)


def save_image(image):
    resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    if resized.dtype != "uint8":
        resized = (resized * 255).astype("uint8")  # Se for float, normaliza
    cv2.imwrite("resized_frame.png", resized)


def save_image_crop(image_array):
    logging.info(f"Start face detection. Image shape is {image_array.shape}.")
    gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    gray_image = gray_image.astype("uint8")
    faces = detect.detectMultiScale(
        gray_image,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    print("faces:", faces)
    i = 0
    if len(faces) == 0:
        logging.info(f"face(s) not found for image {gray_image.shape}.")
    else:
        logging.info(f"this is face return variable {faces}.")
        logging.info(f"this is face return variable shape {faces.shape}.")
        num_faces = faces.shape[0]
        for x, y, w, h in faces:
            pos = (int(x), int(y))
            dim = (int(w), int(h))

            cv2.rectangle(image_array, (x, y), (x + w, y + h), (0, 255, 0), 3)
            face_image = crop_face(image_array, pos=pos, dim=dim)
            # cv2.imwrite(f"images/result/face_image_crop_{i}.png", face_image)
            i += 1

        # cv2.imwrite("../images/result/face_image.png", image_array)

        logging.info(
            f"Completed face detection. Face shape {faces} and found {num_faces} face(s)."
        )
        return face_image, num_faces, faces

    return 0, 0, 0


def image64_encode(image_array):
    try:
        image = Image.fromarray(image_array)

        buffered = BytesIO()
        image.save(buffered, format="PNG")

        image_bytes = buffered.getvalue()
        base64_bytes = base64.b64encode(image_bytes)
        base64_encoded = base64_bytes.decode()

        return base64_encoded
    except Exception as e:
        print("Error: ", e)


# def send_image_api(data_json):
#     response = requests.post(url=URL_POST, data=json.dumps(data_json), headers=headers)
#     return response

# def get_predictions():
#     response = requests.get(url=URL_GET, headers=headers)
#     return response


def face_detect(image_array):
    faces_array = []
    logging.info(f"Start face detection. Image shape is {image_array.shape}.")
    gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    gray_image = gray_image.astype("uint8")
    faces = detect.detectMultiScale(
        gray_image,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    if len(faces) == 0:
        logging.info(f"face not found for image {gray_image.shape}.")
    else:
        logging.info(f"face(s) positions and dimensions {faces}.")
        logging.info(f"faces(s) return shape {faces.shape}.")

        num_faces = faces.shape[0]

        for x, y, w, h in faces:
            pos = (int(x), int(y))
            dim = (int(w), int(h))

            cv2.rectangle(image_array, (x, y), (x + w, y + h), (0, 255, 0), 3)
            face_image = crop_face(image_array, pos=pos, dim=dim)

            faces_array.append(face_image)

        logging.info(
            f"Return completed face detection. Face shape {faces} and found {num_faces} face(s)."
        )
        return faces_array, num_faces, faces.tolist()


def draw_rectangle(image_array, num_faces, face_pos, pred_list, acc_list):
    for i in range(num_faces):
        x = face_pos[i][0]
        y = face_pos[i][1]
        width = face_pos[i][2]
        height = face_pos[i][3]

        image_array = cv2.rectangle(
            image_array,
            pt1=(x, y),
            pt2=(x + width, y + height),
            color=(0, 255, 0),
            thickness=3,
        )

        image_array = cv2.putText(
            img=image_array,
            text=f"{pred_list[i]}",
            org=(x + 5, y + height + 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=2.0,
            color=(0, 255, 0),
            thickness=3,
            lineType=cv2.LINE_AA,
        )

    return image_array


def image64_decode(image_post_data):
    logging.info("Start image decoding from base64 to PIL ndarray")
    image = Image.open(BytesIO(base64.b64decode(image_post_data["image"]["content"])))
    image_array = np.array(image)
    # image.save('images/post_image.jpg', 'JPEG')
    logging.info(f"Completed image decoding. Image shape is {image_array.shape}.")
    return image_array
