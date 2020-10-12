from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Credentials(BaseModel):
    username: str
    password: str


class CourseCreate(BaseModel):
    code: str
    title: str
    description: str
    outlines: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    takeaways: Optional[List[str]] = []


class CourseUpdate(CourseCreate):
    code: Optional[str]
    title: Optional[str]
    description: Optional[str]


class UserUpdate(BaseModel):
    bio: Optional[str]
    email: Optional[str]
    interests: Optional[List[str]]


class DiscussionCreate(BaseModel):
    body: str


class EventCreate(BaseModel):
    subtitle: Optional[str]
    title: str
    type: Optional[str] = 'notice'
    schedule: Optional[datetime]
    enrollment_guid: Optional[str]
