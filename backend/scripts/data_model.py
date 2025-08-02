from pydantic import BaseModel
from typing import Dict
from datetime import datetime

class ImageDataInput(BaseModel):
    image: Dict[str, datetime]
    collection_name: str
    
class ImageDataOutput(BaseModel):
    model_name: str
    num_faces: int
    face_pos: list[list[int]]
    score: list[float]
    class_name: list[str]
    prediction_time: float
    