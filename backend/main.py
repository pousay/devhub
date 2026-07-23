from fastapi import FastAPI
import uvicorn
from app.core.config import settings
from app.routes import router
from app.api.v1 import auth_router

from fastapi.middleware.cors import CORSMiddleware
# fastapi objects
app = FastAPI()
app.include_router(router)
app.include_router(auth_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (development only)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
