from sqlalchemy import Column, VARCHAR, String, ARRAY
from sqlalchemy.orm import relationship
from . import BaseModel


class Course(BaseModel):
    code = Column(VARCHAR(16), nullable=False, unique=True)
    title = Column(VARCHAR(128), nullable=False)
    description = Column(String, nullable=False)
    outlines = Column(ARRAY(String), default=[])
    tags = Column(ARRAY(String), default=[])
    takeaways = Column(ARRAY(String), default=[])

    enrollments = relationship('Enrollment', back_populates='course')
