from fastapi import APIRouter, Response, Depends
from fastapi import HTTPException
from pydantic import BaseModel
from uuid import UUID

from api import auth
from models import User

router = APIRouter()


class CredentialsIn(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str


@router.post('/login')
def login(response: Response, form_data: CredentialsIn) -> TokenOut:
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username/password")

    token = auth.create_access_token(user)
    response.set_cookie(
        'Authorization',
        value=f'Bearer {token}',
        httponly=True,
        max_age=1800,
        expires=1800,
    )

    return TokenOut(access_token=token, token_type='bearer')


@router.post('/logout')
def logout(response: Response):
    response.delete_cookie('Authorization')
    return {}


@router.get('/current-user')
def get_current_user(current_user: User = Depends(auth.get_current_user)):
    return current_user.to_dict()
