# Handles /submit-review and /get-reviews endpoints
from fastapi import APIRouter, Depends, HTTPException
from app.core.services.ai_predict import predictor
from app.db.connection import get_db
from app.db.repository import review_repo
from app.schemas import ReviewRecieve, ReviewResponse
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/predict", response_model=ReviewResponse)
def predict_review(review: ReviewRecieve, db: Session = Depends(get_db)):
    
    prediction_result = predictor.predict_review_category(review.text, review.rating)

    try:
        review_repo.save_review(
            db=db, 
            app_id=review.app_id, 
            text=review.text, 
            rating=review.rating, 
            sentiment=prediction_result
        )
    except Exception as e:
        # If the app_id doesn't exist, Supabase will block it. 
        # This catches the error and tells the frontend what went wrong!
        raise HTTPException(status_code=400, detail=f"Could not save review. Make sure the app_id exists. Error: {str(e)}")
    
    return {
        "text": review.text,
        "rating": review.rating,
        "sentiment": prediction_result,
        "app_id": review.app_id
    }