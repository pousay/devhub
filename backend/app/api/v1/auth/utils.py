from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Annotated
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Literal
from app.utils.tz import time_zone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)


def authenticate_user(username: str, password: str):
    pass
    # user = fake_users.get(username)
    # if not user:
    #     return None
    # if not verify_password(password, user.hashed_password):
    #     return None
    # return user


def create_token(payload: dict, _type: Literal["access", "refresh"]):
    payload["exp"] = datetime.now(time_zone) + timedelta(
        minutes=(
            settings.ACCESS_TOKEN_EXPIRE_MINUTES
            if _type == "access"
            else settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(username: str):
    payload = {"username": username}
    return create_token(payload, "access")


def create_refresh_token(username: str):
    payload = {"username": username}
    return create_token(payload, "refresh")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # user = fake_users.get(username)
    # if user is None:
    #     raise credentials_exception

    # return user
