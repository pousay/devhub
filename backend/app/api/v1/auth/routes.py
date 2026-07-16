from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .utils import (
    authenticate_user,
    create_access_token,
    get_current_user,
    create_refresh_token,
)
from .models import ResponseToken

router = APIRouter(prefix="/auth", tags=["Auth"])


class User:
    pass


@router.post("/login", response_model=ResponseToken)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    access_token = create_access_token("user.username")
    refresh_token = create_refresh_token("user.username")

    return ResponseToken(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me")
def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
