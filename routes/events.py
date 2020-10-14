from fastapi import APIRouter, HTTPException, Depends
from api import auth, event
from datetime import datetime
from models import EntryDoesNotExist, User
from schemas.res import EventRes
from schemas.req import EventCreate
from typing import List
router = APIRouter()


@router.get('/', response_model=List[EventRes], summary='List User Events')
def get_all_events(current_user: User = Depends(auth.get_current_user)):
    '''
    Returns a list of all events where the authorized user is among the target audience.
    '''

    objs = event.get_user_events(current_user)
    return [EventRes.from_obj(obj) for obj in objs]


@router.post('/', response_model=EventRes, status_code=201, summary='Create New Event')
def create_event(data: EventCreate):
    '''
    Creates a new event. Can only be performed by a professor. Returns the created event.
    '''

    try:
        obj = event.create(data.dict(exclude_unset=True))
        return EventRes.from_obj(obj)
    except EntryDoesNotExist:
        raise HTTPException(status_code=404)
