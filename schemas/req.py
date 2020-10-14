from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models.event import event_types


class Credentials(BaseModel):
    username: str
    password: str


class CourseCreate(BaseModel):
    code: str = Field(..., title='Provide a unique short-hand for the course.', description='Ex: ML-101')
    title: str = Field(..., title='What is the course title?', description='Ex: Introduction to Machine Learning')
    description: str = Field(..., title='Provide detailed description.')
    outlines: Optional[List[str]] = Field([], title='Provide the workflow of the course.')
    tags: Optional[List[str]] = Field([], title='Set some tags to utilize in recommendation system.')
    takeaways: Optional[List[str]] = Field([], title='What are the things that a student will learn from the course?')


class CourseUpdate(CourseCreate):
    code: Optional[str] = Field(title='Provide a unique short-hand for the course.', description='Ex: ML-101')
    title: Optional[str] = Field(title='What is the course title?', description='Ex: Introduction to Machine Learning')
    description: Optional[str] = Field(title='Provide detailed description.')


class UserUpdate(BaseModel):
    bio: Optional[str] = Field(title='Describe yourself.', description='Ex: I come from a village loong looong way from...')
    email: Optional[str] = Field(title='What is your email address?')
    interests: Optional[List[str]] = Field(title='What are you interested in?')


class DiscussionCreate(BaseModel):
    body: str = Field(..., title='What do you want to say?')


class EventCreate(BaseModel):
    title: str = Field(..., title='What is the event title?')
    subtitle: Optional[str] = Field(title='Extra bit of info apart from the title.')
    type: Optional[str] = Field('notice', title='What is the event type?', description='One of {}'.format(' '.join(['`%s`' % v for v in event_types])))
    schedule: Optional[datetime] = Field(title='When does the event takes place?')
    enrollment_guid: Optional[str] = Field(title='Associate the event to a specific enrollment only.')
