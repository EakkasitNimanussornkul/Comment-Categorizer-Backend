from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.services.ai_predict import predictor
from app.schemas import ReviewRecieve, ReviewResponse
from app.db.connection import get_db
from app.db.repository import review_repo
from app.core.services.token import get_current_user
from app.db.models import App  # <-- Import the App model for our security check!

router = APIRouter()

@router.post("/predict", response_model=ReviewResponse)
def predict_review(
    review: ReviewRecieve, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # 1. The Bouncer makes sure they are logged in
):
    # 2. THE SECURITY CHECK: Find the app in the database
    target_app = db.query(App).filter(App.id == review.app_id).first()
    
    # If the app doesn't exist at all
    if not target_app:
        raise HTTPException(status_code=404, detail="App not found.")
        
    # If the app exists, but it belongs to a different user!
    if target_app.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this app.")

    # 3. If they pass the security check, get the AI prediction
    prediction_result = predictor.predict_review_category(review.text, review.rating)
    
    # 4. Save the review to the database
    try:
        review_repo.save_review(
            db=db, 
            app_id=review.app_id, 
            text=review.text, 
            rating=review.rating, 
            sentiment=prediction_result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving review: {str(e)}")
    
    return {
        "text": review.text,
        "rating": review.rating,
        "sentiment": prediction_result
    }