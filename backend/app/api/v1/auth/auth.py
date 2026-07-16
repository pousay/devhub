from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .utils import authenticate_user, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


class User:
    pass


@router.post("/login")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    token = create_access_token({"sub": user.username})
    return {"access_token": token}


@router.get("/me")
def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
