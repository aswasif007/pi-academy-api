import jwt

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from datetime import timedelta, datetime
from typing import Optional

from models import User
from config import Config


class OAuth2PasswordBearerCookie(OAuth2PasswordBearer):

    async def __call__(self, request: Request) -> Optional[str]:
        cookie_authorization: str = request.cookies.get("Authorization")
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if cookie_scheme.lower() != 'bearer':
            raise HTTPException(status_code=403, detail="Not authenticated")

        return cookie_param


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl='auth/login')


def authenticate_user(username, password) -> User:
    user = User.get_one(username=username)
    if user and user.validate_password(password):
        return user


def create_access_token(user: User):
    payload = {
        'sub': user.username,
        'exp': datetime.utcnow() + timedelta(minutes=3600)
    }
    
    token = jwt.encode(payload, Config.secret, algorithm='HS256')
    return token.decode('utf-8')


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = is_authorized(token)
    user = User.get_one(username=payload['sub'])
    if user:
        return user

    raise HTTPException(status_code=401, detail='Unauthorized.')


def is_authorized(token: str = Depends(oauth2_scheme)):
    try:
        return jwt.decode(token, Config.secret, algorithms=['HS256'])
    except Exception:
        raise HTTPException(status_code=401, detail='Unauthorized.')
