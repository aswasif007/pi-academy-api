from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, VARCHAR, String, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from . import BaseModel


class Discussion(BaseModel):
    body = Column(String, nullable=False, default='')
    author_guid = Column(GUID, ForeignKey('users.guid'), nullable=False)
    enrollment_guid = Column(GUID, ForeignKey('enrollments.guid'), nullable=True)

    author = relationship('User')
    enrollment = relationship('Enrollment')
