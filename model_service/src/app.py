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
        return jsonify(data_pred)
    except Exception as e:
        return jsonify(message={f"{e}"})

@app.route('/v1/predictions', methods=['POST'])
def predict():
    if request.method == 'POST':
        data_pred.clear()
        data = request.get_json()
        image_array = image64_decode(data)
        face_image_array, num_of_faces, faces_positions = face_detect(image_array)
        image_array_for_model  = image_preprocessing(face_image_array)
        pred_list, acc_list = emd.predict(image_array_list=image_array_for_model, model=model)

        image_props["num_of_faces"] = num_of_faces
        image_props["faces_positions"] = faces_positions
        
        data_pred["prediction"] = pred_list
        data_pred["accuracy"] = acc_list
        data_pred["name"] = data['image']['name']
        data_pred["image-props"] = image_props
        
        print(data_pred)
        
        return jsonify({'message': 'Data received', 'image': data['image']['name']}), 201
    else:
        return jsonify({"message": "Data missing"})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)