from flask import Flask
from flask import jsonify
from flask import request

from src.ml_classifier import EmotionDetection
from src.utils import face_detec, image_preprocessing, image64_decode

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

@app.route('/v1/predictions/<string:name>', methods=['GET'])
def get_predict(name):
    try:        
        if data_list[0]['author'] == name:
            return jsonify(data_list)
        else:
            return jsonify(message={"message": "Name not found"})
    except IndexError:
        return jsonify(message={"message": "IndexError"})

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
    

@app.route('/v1/predictions', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json()
        print(data['images'][0]['name'])
        image = image64_decode(data)
        face_image = face_detec(image_array=image)
        image_array = image_preprocessing(face_image)
        pred, acc = emd.predict(image_array=image_array, model=model)
            
        data_pred["prediction"] = pred
        data_pred["accuracy"] = acc
        data_pred["author"] = data['images'][0]['author']
        data_list.append(data_pred)
        
        return jsonify({'message': 'Data received', 'image': data['images'][0]['name']}), 201
    else:
        return jsonify({"message": "Data missing"})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)