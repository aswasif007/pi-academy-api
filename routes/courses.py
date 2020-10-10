from fastapi import APIRouter
from fastapi import HTTPException
from typing import List
from api import course
from models import EntryDoesNotExist
from schemas.req import CourseCreate, CourseUpdate
from schemas.res import CourseRes

router = APIRouter()


@router.get('/', response_model=List[CourseRes])
def get_all_courses():
    return [CourseRes.from_obj(obj) for obj in course.get_all()]


@router.get('/{guid}', response_model=CourseRes)
async def get_course(guid: str):
    try:
        return CourseRes.from_obj(course.get(guid))
    except EntryDoesNotExist:
        raise HTTPException(status_code=404, detail='Entry does not exist.')


@router.post('/', status_code=201, response_model=CourseRes)
async def create_course(data: CourseCreate) -> dict:
    return CourseRes.from_obj(course.create(data.dict()))


@router.patch('/{guid}', response_model=CourseRes)
def update_course(guid: str, data: CourseUpdate) -> dict:
    try:
        return CourseRes.from_obj(course.update(guid, data.dict(exclude_unset=True)))
    except EntryDoesNotExist:
        raise HTTPException(status_code=404, detail='Entry does not exist.')


@router.delete('/{guid}', status_code=204)
def delete_course(guid: str):
    try:
        return course.delete(guid)
    except EntryDoesNotExist:
        raise HTTPException(status_code=404, detail='Entry does not exist.')
