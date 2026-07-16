from fastapi import FastAPI
import uvicorn
from app.core.config import settings
from app.routes import router
from app.api.v1 import auth_router

app = FastAPI()
app.include_router(router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
