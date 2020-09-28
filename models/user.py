import enum
import bcrypt

from sqlalchemy import Column, VARCHAR, String
from sqlalchemy.orm import validates, relationship
from . import BaseModel
from .enrollment import EnrollmentToUserAssociation


categories = ['student', 'professor', 'admin', 'curator']


class User(BaseModel):
    name = Column(VARCHAR(128), nullable=False)
    username = Column(VARCHAR(64), nullable=False, unique=True)
    password_hash = Column('password', String, nullable=False)
    avatar = Column(String, nullable=True)
    category = Column(VARCHAR(64), nullable=False, default=categories[0])

    enrollments = relationship('Enrollment', secondary=EnrollmentToUserAssociation, back_populates='people')

    @validates('category')
    def category_validator(self, key, value):
        assert value in categories
        return value

    @property
    def password(self):
        raise Exception('write-only field.')

    @password.setter
    def password(self, value):
        self.password_hash = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def validate_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
