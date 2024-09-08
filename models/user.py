#!/usr/bin/python3
"""User Class"""


from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from hashlib import md5

class User(BaseModel, Base):
    """User Representation"""
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    bio = Column(String(255))
    gender = Column(String(10))
    age = Column(Integer)
    interests = Column(String(125))
    location = Column(String(100))
    profile_picture = Column(String(255))