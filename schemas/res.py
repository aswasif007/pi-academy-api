from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class ResourceRes(BaseModel):
    guid: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_obj(obj):
        return ResourceRes(
            guid=str(obj.guid),
            created_at=obj.created_at,
            updated_at=obj.updated_at,
        )


class CourseRes(ResourceRes):
    code: str
    title: str
    description: str
    outlines: List[str]
    tags: List[str]
    takeaways: List[str]

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
    name: str
    avatar: Optional[str] = None
    username: str
    category: str

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
    body: str
    author: UserRes

    @staticmethod
    def from_obj(obj):
        return DiscussionRes(
            body=obj.body,
            author=UserRes.from_obj(obj.author),
            **ResourceRes.from_obj(obj).dict()
        )


class ThreadRes(ResourceRes):
    post: DiscussionRes
    comments: List[DiscussionRes]

    @staticmethod
    def from_obj(obj):
        return ThreadRes(
            post=DiscussionRes.from_obj(obj),
            comments=[DiscussionRes.from_obj(comm) for comm in obj.comments],
            **ResourceRes.from_obj(obj).dict()
        )


class ProfileRes(ResourceRes):
    bio: str
    email: str
    interests: List[str]

    @staticmethod
    def from_obj(obj):
        return ProfileRes(
            bio=obj.bio,
            email=obj.email,
            interests=obj.interests,
            **ResourceRes.from_obj(obj).dict()
        )
