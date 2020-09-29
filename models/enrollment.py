from datetime import datetime, timedelta
from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, VARCHAR, String, ARRAY, DateTime, ForeignKey, Table
from sqlalchemy.orm import validates, relationship
from . import BaseModel, Base

statuses = ['open', 'closed']


EnrollmentToUserAssociation = Table(
    'enrollment_to_user_associations',
    Base.metadata,
    Column('user_guid', GUID, ForeignKey('users.guid')),
    Column('enrollment_guid', GUID, ForeignKey('enrollments.guid'))
)


class Enrollment(BaseModel):
    course_guid = Column(GUID, ForeignKey('courses.guid'), nullable=False)
    status = Column(VARCHAR(32), nullable=False, default=statuses[0])
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=lambda: datetime.utcnow + timedelta(days=90))

    course = relationship('Course', back_populates='enrollments')
    people = relationship('User', secondary=EnrollmentToUserAssociation, back_populates='enrollments')
    events = relationship('Event', back_populates='enrollment')

    @validates('status')
    def status_validator(self, key, value):
        assert value in statuses
        return value
