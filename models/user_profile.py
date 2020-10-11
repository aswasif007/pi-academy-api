from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, String, VARCHAR, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from . import BaseModel


class UserProfile(BaseModel):
    __tablename__ = 'user_profiles'

    guid = Column(GUID, ForeignKey('users.guid', ondelete='CASCADE'), primary_key=True)
    bio = Column(String, default='')
    email = Column(VARCHAR(64), default='')
    interests = Column(ARRAY(String), default=[])

    user = relationship('User', uselist=False, back_populates='profile')
