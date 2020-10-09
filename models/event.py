from . import BaseModel

from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, String, DateTime, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship, validates

eventTypes = ['notice', 'test', 'test_result']
statuses = ['active', 'expired']


class Event(BaseModel):
    subtitle = Column(String, default=None)
    title = Column(String, nullable=False)
    type = Column(VARCHAR(32), default=eventTypes[0])
    status = Column(VARCHAR(32), default=statuses[0])
    schedule = Column(DateTime, default=None)
    enrollment_guid = Column(GUID, ForeignKey('enrollments.guid', ondelete='SET NULL'), default=None)
    user_guid = Column(GUID, ForeignKey('users.guid', ondelete='SET NULL'), default=None)

    enrollment = relationship('Enrollment', back_populates='events')
    user = relationship('User', back_populates='events')

    @validates('type')
    def type_validator(self, key, value):
        assert value in eventTypes
        return value

    @validates('status')
    def status_validator(self, key, value):
        assert value in statuses
        return value
