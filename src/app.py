from flask import Flask
from flask import jsonify
from flask import request

from ml_classifier import EmotionDetection
from utils import face_detec, image_preprocessing

# Machine Learning Model class
CLASS_NAMES = ['angry', 'fear', 'happy', 'neutral', 'sad'] 

emd = EmotionDetection(CLASS_NAMES)
model = emd.load(path='model/model-26-0.7175.h5')

app = Flask(__name__)

data_pred = {}
data_list = []

@app.route('/default/predict', methods=['GET'])
def get_default_predict():
    return jsonify(data_list)

@app.route('/test/predict', methods=['POST'])
def test_predict():
    if request.method == 'POST':
        data = request.get_json()
        
        if data['image'] == 'default':
            face_image = face_detec(image_path='images/me.jpeg')
            image_array = image_preprocessing(face_image)
            pred, acc = emd.predict(image_array=image_array, model=model)
            
            data_pred["prediction"] = pred
            data_pred["accuracy"] = acc
            data_list.append(data_pred)
            
            return jsonify({'message': 'Data received', 'image': data['image']}), 201
    else:
        return jsonify({"message": "Data missing"})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)