# Handles /login and /register endpoints
from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/login")
def login(username: str, password: str):
    return {"status": "running", "message": "this is login endpoint!"}

@router.post("/auth/register")
def register(username: str, password: str, email: str):
    return {"status": "running", "message": "this is register endpoint!"}