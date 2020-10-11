from fastapi import APIRouter, HTTPException, Depends
from api import user_profile, auth
from models import EntryDoesNotExist, User
from schemas.res import ProfileRes
from schemas.req import UserUpdate

router = APIRouter()


@router.get('/current-user', response_model=ProfileRes)
def get_current_user_profile(current_user: User = Depends(auth.get_current_user)):
    return ProfileRes.from_obj(current_user.profile)


@router.patch('/current-user', response_model=ProfileRes)
def update_current_user_profile(data: UserUpdate, current_user: User = Depends(auth.get_current_user)):
    obj = user_profile.update(current_user.guid, data.dict(exclude_unset=True))
    return ProfileRes.from_obj(obj)


@router.get('/{guid}', response_model=ProfileRes)
def get_user_profile(guid: str):
    try:
        obj = user_profile.get(guid)
        return ProfileRes.from_obj(obj)
    except EntryDoesNotExist:
        raise HTTPException(status_code=404)
