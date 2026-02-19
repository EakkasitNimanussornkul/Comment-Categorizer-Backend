# Handles /submit-review and /get-reviews endpoints
from fastapi import APIRouter
from app.core.services.ai_predict import predictor
from app.schemas import ReviewRecieve, ReviewResponse

router = APIRouter()

@router.post("/predict", response_model=ReviewResponse)
def predict_review(review: ReviewRecieve):
    prediction_result = predictor.predict_review_category(review.text, review.rating)
    return {
        "text": review.text,
        "rating": review.rating,
        "sentiment": prediction_result
    }