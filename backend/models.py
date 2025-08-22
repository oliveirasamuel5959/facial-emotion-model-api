from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Emotion(Base):
    __tablename__ = 'emotions'
    
    id = Column(Integer, primary_key=True, index=True)
    emotion = Column(String, index=True)
