from fastapi import APIRouter, HTTPException, Depends
from api import auth, enrollment, discussion
from models import EntryDoesNotExist, User
from schemas.res import ThreadRes, EnrollmentRes, EnrollmentDetailsRes
from schemas.req import DiscussionCreate
from typing import List

router = APIRouter()


@router.get('/', response_model=List[EnrollmentRes], summary='List User Enrollments')
def get_all_enrollments(current_user: User = Depends(auth.get_current_user)):
    '''
    Returns a list of enrollments for the authorized user.
    '''

    objs = current_user.enrollments
    return [EnrollmentRes.from_obj(obj) for obj in objs]


@router.get('/{guid}/details', response_model=EnrollmentDetailsRes, summary='Get Enrollment Details')
def get_enrollment_detail(guid: str, current_user: User = Depends(auth.get_current_user)):
    '''
    Returns detailed info of the enrollment identified by `guid`. If the enrollment does not belong to the
    authorized user, it returns 404.
    '''

    try:
        obj = enrollment.get(guid)
        if current_user not in obj.people:
            raise EntryDoesNotExist

        return EnrollmentDetailsRes.from_obj(obj)
    except EntryDoesNotExist:
        raise HTTPException(status_code=404)


@router.get('/{guid}/discussions', response_model=List[ThreadRes], summary='List Enrollment Threads')
def get_enrollment_threads(guid: str, current_user: User = Depends(auth.get_current_user)):
    '''
    Returns list of discussion threads of the enrollment identified by `guid`. If the enrollment does not belong to the
    authorized user, it returns 404.
    '''

    try:
        enrollment_obj = enrollment.get(guid)
        if current_user not in enrollment_obj.people:
            raise EntryDoesNotExist

        objs = discussion.get_enrollment_posts(guid)
        return [ThreadRes.from_obj(obj) for obj in objs]
    except EntryDoesNotExist:
        raise HTTPException(status_code=404)


@router.post('/{guid}/discussions', response_model=ThreadRes, status_code=201, summary='Create New Post in Enrollment')
def create_enrollment_threads(guid: str, data: DiscussionCreate, current_user: User = Depends(auth.get_current_user)):
    '''
    Creates a new post as well as a new discussion thread in the enrollment identified by `guid`. If the enrollment
    does not belong to the authorized user, it returns 404. Else, returns the created thread.
    '''

    try:
        enrollment_obj = enrollment.get(guid)
        if current_user not in enrollment_obj.people:
            raise EntryDoesNotExist

        data = data.dict()
        data['author'] = current_user
        data['enrollment'] = enrollment_obj
        obj = discussion.create(data)
        return ThreadRes.from_obj(obj)
    except EntryDoesNotExist:
        raise HTTPException(status_code=404)
