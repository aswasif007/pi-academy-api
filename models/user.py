import enum

from sqlalchemy import Column, VARCHAR, String
from sqlalchemy.orm import validates
from . import BaseModel

categories = ['student', 'professor', 'admin', 'curator']


class User(BaseModel):
    name = Column(VARCHAR(128), nullable=False)
    username = Column(VARCHAR(64), nullable=False, unique=True)
    password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    category = Column(VARCHAR(64), nullable=False, default=categories[0])

    @validates('category')
    def validate_category(self, key, value):
        assert value in categories
        return value
