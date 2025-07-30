import logging

import numpy as np
import tensorflow as tf
from tensorflow import keras

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class EmotionDetection:
    def __init__(self, class_names):
        self.class_names = class_names

    def load(self, path):
        """
        Load keras model weights in .h5 format
        """
        self.model = tf.keras.models.load_model(path)
        logging.info("Model Load successfuly!")
        return self.model

    def predict(self, image_array_list, model):
        confidence_list = []
        predicted_class_list = []
        """
        model load and stored in model variable
        image must be in the format: (1, 224, 224, 3)
        class names must be in the same order that was trained
        
        return class name prediction and accuracy
        """
        logging.info(f"Start Prediction for {len(image_array_list)} images")
        for i in range(len(image_array_list)):
            logging.info(f"Start Prediction for image {i + 1}")
            predictions = model.predict(image_array_list[i])[0]
            predicted_index = np.argmax(predictions)
            predicted_class = self.class_names[predicted_index]
            confidence = float(predictions[predicted_index])
            confidence = round(confidence, 2) * 100

            predicted_class_list.append(predicted_class)
            confidence_list.append(confidence)

            logging.info(f"Return prediction for image {i + 1} : {predicted_class}")
            logging.info(f"Return confidence value for image {i + 1} : {confidence}")
            logging.info(f"Completed prediction for image {i + 1}")

        logging.info(f"Completed prediction for {len(image_array_list)} images.")
        return [predicted_class_list, confidence_list]
