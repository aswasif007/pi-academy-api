from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, VARCHAR, String, ARRAY, ForeignKey
from sqlalchemy.orm import relationship, backref
from . import BaseModel
from uuid import uuid4


class Discussion(BaseModel):
    guid = Column(GUID, primary_key=True, default=uuid4, index=True)
    body = Column(String, nullable=False, default='')
    author_guid = Column(GUID, ForeignKey('users.guid', ondelete='CASCADE'), nullable=False)
    enrollment_guid = Column(GUID, ForeignKey('enrollments.guid', ondelete='SET NULL'), nullable=True)
    post_guid = Column(GUID, ForeignKey('discussions.guid', ondelete='CASCADE'), nullable=True)

    author = relationship('User')
    enrollment = relationship('Enrollment')
    post = relationship('Discussion', remote_side=[guid], back_populates='comments')
    comments = relationship('Discussion', back_populates='post')
