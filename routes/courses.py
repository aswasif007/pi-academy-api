from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Optional
from api import course
from models import EntryDoesNotExist

router = APIRouter()


class CreateCourse(BaseModel):
    code: str
    title: str
    description: str
    outlines: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    takeaways: Optional[List[str]] = []


class UpdateCourse(CreateCourse):
    code: Optional[str]
    title: Optional[str]
    description: Optional[str]


@router.get('/')
def get_all_courses() -> List[dict]:
    return course.get_all()


@router.get('/{guid}')
async def get_course(guid: str) -> dict:
    try:
        return course.get(guid)
    except EntryDoesNotExist:
        raise HTTPException(status_code=404, detail='Entry does not exist.')


@router.post('/', status_code=201)
async def create_course(data: CreateCourse) -> dict:
    return course.create(data.dict())


@router.patch('/{guid}')
def update_course(guid: str, data: UpdateCourse) -> dict:
    try:
        return course.update(guid, data.dict(exclude_unset=True))
    except EntryDoesNotExist:
        raise HTTPException(status_code=404, detail='Entry does not exist.')


@router.delete('/{guid}', status_code=204)
def delete_course(guid: str) -> None:
    try:
        return course.delete(guid)
    except EntryDoesNotExist:
        raise HTTPException(status_code=404, detail='Entry does not exist.')
