from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["Auth"])




# ==========================
# Routes
# ==========================
@router.post("/login", response_model=Token)
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
