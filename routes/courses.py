from fastapi import APIRouter
from fastapi import HTTPException
from typing import List
from api import course
from models import EntryDoesNotExist
from schemas.req import CourseCreate, CourseUpdate
from schemas.res import CourseRes

router = APIRouter()


@router.get('/', response_model=List[CourseRes], summary='List Available Courses')
def get_all_courses():
    '''
    Returns a list of the courses available to the user.
    '''

    return [CourseRes.from_obj(obj) for obj in course.get_all()]


@router.get('/{guid}', response_model=CourseRes, summary='Get a Course')
async def get_course(guid: str):
    '''
    Returns a course identified by `guid`, if that is available to the user. Otherwise, returns 404.
    '''

    try:
        return CourseRes.from_obj(course.get(guid))
    except EntryDoesNotExist:
        raise HTTPException(status_code=404, detail='Entry does not exist.')


@router.post('/', status_code=201, response_model=CourseRes, summary='Create New Course')
async def create_course(data: CourseCreate) -> dict:
    '''
    Creates a new course. Only a curator can perform this action. Returns the created course.
    '''

    return CourseRes.from_obj(course.create(data.dict()))


@router.patch('/{guid}', response_model=CourseRes, summary='Update a Course')
def update_course(guid: str, data: CourseUpdate) -> dict:
    '''
    Updates an existing course identified by `guid`. Only a curator can perform this action. Returns the updated course.
    '''

    try:
        return CourseRes.from_obj(course.update(guid, data.dict(exclude_unset=True)))
    except EntryDoesNotExist:
        raise HTTPException(status_code=404, detail='Entry does not exist.')


@router.delete('/{guid}', status_code=204, summary='Delete a Course')
def delete_course(guid: str):
    '''
    Deletes an existing course identified by `guid`. Only a curator can perform this action.
    '''

    try:
        return course.delete(guid)
    except EntryDoesNotExist:
        raise HTTPException(status_code=404, detail='Entry does not exist.')
