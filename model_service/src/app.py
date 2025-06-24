from flask import Flask
from flask import jsonify
from flask import request

from src.ml_classifier import EmotionDetection
from src.utils import face_detect, image_preprocessing, image64_decode

# Machine Learning Model class
CLASS_NAMES = ['angry', 'fear', 'happy', 'neutral', 'sad'] 

emd = EmotionDetection(CLASS_NAMES)
model = emd.load(path='model/model-26-0.7175.h5')

app = Flask(__name__)

data_pred = {}
image_props = {}

@app.route('/')
def home():
    return "<h1>Hello from API</h1>"

@app.route('/v1/predictions/<string:name>', methods=['GET'])
def get_predict(name):
    try:        
        if data_pred['name'] == name:
            return jsonify(data_pred)
        else:
            return jsonify(message={"message": "Name not found"})
    except Exception:
        return jsonify(message={"IndexError"})

@app.route('/v1/predictions', methods=['POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json()
        image = image64_decode(data)
        image_array = image_preprocessing(image)
        face_image_array, pos, dim = face_detect(image_array=image_array)
        pred, acc = emd.predict(image_array=face_image_array, model=model)

        image_props["position"] = pos
        image_props["dimension"] = dim
        
        data_pred["prediction"] = pred
        data_pred["accuracy"] = acc
        data_pred["name"] = data['image']['name']
        data_pred["image-props"] = image_props
        
        return jsonify({'message': 'Data received', 'image': data['image']['name']}), 201
    else:
        return jsonify({"message": "Data missing"})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)