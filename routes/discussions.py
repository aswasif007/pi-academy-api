from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api import discussion, auth
from models import EntryDoesNotExist, User
from schemas.req import DiscussionCreate
from schemas.res import ThreadRes, DiscussionRes

router = APIRouter()


@router.get('/', response_model=List[ThreadRes], summary='List General Threads')
def get_general_threads():
    '''
    Returns a list of discussion-threads that are not assiciated to any enrollment.
    '''

    return [ThreadRes.from_obj(obj) for obj in discussion.get_general_posts()]


@router.post('/', status_code=201, response_model=ThreadRes, summary='Create New Post')
def create_general_thread(data: DiscussionCreate, current_user: User = Depends(auth.get_current_user)):
    '''
    Creates a new post as well as a new discussion thread. Returns the discussion thread.
    '''

    data = data.dict()
    data['author'] = current_user
    obj = discussion.create(data)
    return ThreadRes.from_obj(obj)


@router.post('/{guid}/comments', status_code=201, response_model=DiscussionRes, summary='Create New Comment')
def add_comment(guid: str, data: DiscussionCreate, current_user: User = Depends(auth.get_current_user)):
    '''
    Adds a comment to the post identified by `guid`. Returns the comment.
    '''

    data = data.dict()
    data['author'] = current_user
    data['post_guid'] = guid
    try:
        obj = discussion.create(data)
        return DiscussionRes.from_obj(obj)
    except EntryDoesNotExist:
        raise HTTPException(status_code=404)


@router.delete('/{guid}', status_code=204, summary='Delete a Discussion')
def delete_discussion(guid: str):
    '''
    Deletes a discussion identified by `guid`. It can be a post or a comment. In case of a post,
    all the associated comments will also be deleted.
    '''

    try:
        return discussion.delete(guid)
    except EntryDoesNotExist:
        raise HTTPException(status_code=404)
