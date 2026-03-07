from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.connection import get_db
from app.db.repository import app_repo
from app.schemas import AppCreate, AppResponse

# Import your new Bouncer!
from app.core.services.token import get_current_user 

router = APIRouter()

@router.post("/create", response_model=AppResponse)
def create_new_app(
    app_data: AppCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # <-- THE BOUNCER IS HERE!
):
    try:
        # We get the user_id securely straight from the verified token!
        secure_user_id = current_user.id 
        
        saved_app = app_repo.create_app(
            db=db,
            name=app_data.name,
            description=app_data.description,
            user_id=secure_user_id  # Pass the secure ID to the database
        )
        return saved_app
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 1. THE GET ENDPOINT: Fetch all apps for the logged-in user
@router.get("/", response_model=List[AppResponse])
def get_my_apps(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # The Bouncer
):
    # Get all apps belonging to this secure user ID
    apps = app_repo.get_user_apps(db=db, user_id=current_user.id)
    return apps


# 2. THE DELETE ENDPOINT: Remove a specific app
@router.delete("/{app_id}")
def delete_my_app(
    app_id: int, # FastAPI grabs this number from the URL!
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # The Bouncer
):
    # First, find the app and prove this user actually owns it
    target_app = app_repo.get_app_by_id(db=db, app_id=app_id, user_id=current_user.id)
    
    # If the app doesn't exist, or it belongs to someone else, block them!
    if not target_app:
        raise HTTPException(
            status_code=404, 
            detail="App not found or you don't have permission to delete it."
        )
    
    # If they pass the security check, delete it
    app_repo.delete_app(db=db, app=target_app)
    
    return {"message": f"App '{target_app.name}' has been successfully deleted!"}