from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/test")
async def test_endpoint(request: Request):
    return {"ping": "pong"}
