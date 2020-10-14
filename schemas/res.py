from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from models.user import categories as user_cateogies
from models.event import event_types


class Token(BaseModel):
    access_token: str = Field(..., title='Signed JWT. Must be in the request cookie for authorization.')
    token_type: str = Field(..., title='Token type.', description='Ex: Bearer.')


class ResourceRes(BaseModel):
    guid: str = Field(..., title='Globally unique identifier of the object.')
    created_at: datetime = Field(..., title='Object creation timestamp.')
    updated_at: datetime = Field(..., title='Object last modification timestamp.')

    @staticmethod
    def from_obj(obj):
        return ResourceRes(
            guid=str(obj.guid),
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )


class CourseRes(ResourceRes):
    code: str = Field(..., title='Unique short-hand of the course.', description='Ex: ML-101')
    title: str = Field(..., title='Title of the course.', description='Ex: Introduction to Machine Learning')
    description: str = Field(..., title='Detailed course description.')
    outlines: List[str] = Field(..., title='Workflow of the course.')
    tags: List[str] = Field(..., title='Tags, useful in recommendation.')
    takeaways: List[str] = Field(..., title='Knowledge offered by the course.')

    @staticmethod
    def from_obj(obj):
        return CourseRes(
            code=obj.code,
            title=obj.title,
            description=obj.description,
            outlines=obj.outlines,
            tags=obj.tags,
            takeaways=obj.takeaways,
            **ResourceRes.from_obj(obj).dict()
        )


class UserRes(ResourceRes):
    name: str = Field(..., title='Full name of the user')
    avatar: Optional[str] = Field(None, title='User\'s avatar url.')
    username: str
    category: str = Field(..., title='Category of the user', description='One of {}'.format(' '.join(['`%s`' % v for v in user_cateogies])))

    @staticmethod
    def from_obj(obj):
        return UserRes(
            name=obj.name,
            username=obj.username,
            avatar=obj.avatar,
            category=obj.category,
            **ResourceRes.from_obj(obj).dict()
        )



class DiscussionRes(ResourceRes):
    body: str = Field(..., title='Text content.')
    author: UserRes = Field(..., title='Author of the text content.')

    @staticmethod
    def from_obj(obj):
        return DiscussionRes(
            body=obj.body,
            author=UserRes.from_obj(obj.author),
            **ResourceRes.from_obj(obj).dict()
        )


class ThreadRes(ResourceRes):
    post: DiscussionRes = Field(..., title='The first discussion of the conversation.')
    comments: List[DiscussionRes] = Field(..., title='Subsequent discussions of the conversation.')

    @staticmethod
    def from_obj(obj):
        return ThreadRes(
            post=DiscussionRes.from_obj(obj),
            comments=[DiscussionRes.from_obj(comm) for comm in obj.comments],
            **ResourceRes.from_obj(obj).dict()
        )


class ProfileRes(ResourceRes):
    bio: str = Field(..., title='Short intro of the user.')
    email: str = Field(..., title='Email address')
    interests: List[str] = Field(..., title='Topics that attracts the user.')

    @staticmethod
    def from_obj(obj):
        return ProfileRes(
            bio=obj.bio,
            email=obj.email,
            interests=obj.interests,
            **ResourceRes.from_obj(obj).dict()
        )


class EnrollmentRes(ResourceRes):
    code: str = Field(..., title='Enrollment\'s course-code')
    title: str = Field(..., title='Enrollment\'s course-title')

    @staticmethod
    def from_obj(obj):
        return EnrollmentRes(
            code=obj.course.code,
            title=obj.course.title,
            **ResourceRes.from_obj(obj).dict()
        )


class EnrollmentDetailsRes(ResourceRes):
    status: str = Field(..., title='Current status of the enrollment.')
    instructors: List[UserRes] = Field(..., title='List of professors instructing this course.')
    members: List[UserRes] = Field(..., title='List of students participating in this course.')
    course: CourseRes = Field(..., title='The course')

    @staticmethod
    def from_obj(obj):
        instructors = [user for user in obj.people if user.category == 'professor']
        members = [user for user in obj.people if user.category == 'student']
        return EnrollmentDetailsRes(
            status=obj.status,
            instructors=[UserRes.from_obj(user) for user in instructors],
            members=[UserRes.from_obj(user) for user in members],
            course=CourseRes.from_obj(obj.course),
            **ResourceRes.from_obj(obj).dict()
        )


class EventRes(ResourceRes):
    title: str = Field(..., title='Title of the event.')
    subtitle: str = Field(..., title='Extra bit of info apart from the title.')
    type: str = Field(..., title='Type of the event', description='One of {}'.format(' '.join(['`%s`' % v for v in event_types])))
    schedule: datetime = Field(..., title='Event schedule.')

    @staticmethod
    def from_obj(obj):
        return EventRes(
            subtitle=obj.subtitle,
            title=obj.title,
            type=obj.type,
            schedule=obj.schedule,
            **ResourceRes.from_obj(obj).dict(),
        )
