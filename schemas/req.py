from pydantic import BaseModel
from typing import Optional, List


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
