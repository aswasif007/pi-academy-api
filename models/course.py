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

    def to_dict(self):
        obj = super().to_dict()
        obj.update({
            'code': self.code,
            'title': self.title,
            'description': self.description,
            'outlines': self.outlines,
            'tags': self.tags,
            'takeaways': self.takeaways,
        })
        return obj
