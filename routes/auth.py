from fastapi import APIRouter, Response, Depends
from fastapi import HTTPException
from api import auth
from models import User
from schemas.req import Credentials
from schemas.res import Token, UserRes

router = APIRouter()


@router.post('/login', response_model=Token, summary='User Login')
def login(response: Response, form_data: Credentials):
    '''
    Upon verification of the username and password, returns signed JWT and set to cookie as 'Authorization'.
    This token is required in subsequent api calls to identify the authorized user. The token gets expired after
    30 minutes.
    '''

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

    return Token(access_token=token, token_type='bearer')


@router.post('/logout', summary='User Logout')
def logout(response: Response):
    '''
    Removes the 'Authorization' cookie. However, the signed JWT remains valid, until it gets expired automatically.
    '''

    response.delete_cookie('Authorization')


@router.get('/current-user', response_model=UserRes, summary='Get Current User')
def get_current_user(current_user: User = Depends(auth.get_current_user)):
    '''
    Identifies the authorized user from the signed JWT and returns the user object.
    '''

    return UserRes.from_obj(current_user)
