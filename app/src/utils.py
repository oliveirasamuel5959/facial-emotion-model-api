import base64
import json
import requests
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

URL = 'http://emovio.com.br/api/v1/predictions'
headers = {'content-type': 'application/json'}

def image64_encode(base_image, name):
    try:
        buffered = BytesIO()
        base_image.save(buffered, format='JPEG')
        
        image_bytes = buffered.getvalue()
        base64_bytes = base64.b64encode(image_bytes)
        base64_encoded = base64_bytes.decode()
        
        data = {
            'image':
                {
                    'name': str(name),
                    'timestamp': 1215456,
                    'content': base64_encoded
                },
            'collection_name': 'Image base64 for data analysis'
        }

        return data
        
    except Exception as e:
        print("Error: ", e)
    

def send_image_api(data_json):
    response = requests.post(url=URL, data=json.dumps(data_json), headers=headers)
    return response    
    
def get_predictions(name):
    response = requests.get(url=f'http://emovio.com.br/api/v1/predictions/{name}', headers=headers)
    return response