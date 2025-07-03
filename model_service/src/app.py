# from flask import Flask
# from flask import jsonify
# from flask import request

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.ml_classifier import EmotionDetection
from src.utils import face_detect, image_preprocessing, image64_decode, draw_rectangle, image64_encode

# Machine Learning Model class
CLASS_NAMES = ['angry', 'fear', 'happy', 'neutral', 'sad'] 

emd = EmotionDetection(CLASS_NAMES)
model = emd.load(path='model/model-26-0.7175.h5')

# app = Flask(__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_pred = {}
image_props = {}

@app.get('/')
async def home(request: Request):
    return "<h1>Hello from API</h1>"

@app.get('/v1/predictions/{name}')
async def get_predict(name, req: Request):
    try:        
        return JSONResponse(data_pred)
    except Exception as e:
        return JSONResponse(message={f"{e}"})
    
    
@app.get('v1/predictions/image')
async def get_predict_image(req: Request):
    try:
        return JSONResponse(data_pred)
    except Exception as e:
        return JSONResponse(message={f"Failed: {e}"})

@app.post('/v1/login')
async def login(req: Request):
    if req.method == 'POST':
        data = await req.json()
        print(data)
        
        return JSONResponse({'message': 'Data received', 'data': data}), 201
    else:
        return JSONResponse({"message": "Error post request"})
    
@app.post('/v1/predictions')
async def predict(req: Request):
    if req.method == 'POST':
        data_pred.clear()
        data = await req.json()
        print(data['image']['content'][0:20])
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
        
        return JSONResponse({'message': 'Data received', 'image': data['image']['name']}), 201
    else:
        return JSONResponse({"message": "Data missing"})
    

@app.post('/v1/predictions/from/image')
async def predict_image(req: Request):
    if req.method == 'POST':
        data_pred.clear()
        data = await req.json()
        print(data['image']['content'][0:20])
        image_array = image64_decode(data)
        face_image_array, num_faces, face_pos = face_detect(image_array)
        image_array_for_model  = image_preprocessing(face_image_array)
        pred_list, acc_list = emd.predict(image_array_list=image_array_for_model, model=model)

        image_pred_array = draw_rectangle(image_array=image_array, num_faces=num_faces, face_pos=face_pos, pred_list=pred_list, acc_list=acc_list)
        image_base64 = image64_encode(image_array=image_pred_array)
        
        return JSONResponse(content={"pred_image": image_base64}), 201
    else:
        return JSONResponse({"pred_image": "Error"})
    
if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8080, reload=True)