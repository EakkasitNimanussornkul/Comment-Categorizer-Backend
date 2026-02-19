# Handles /stats endpoint for your pie chart
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    return {"status": "running", "message": "Comment Category API is healthy!"}