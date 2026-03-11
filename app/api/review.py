from fastapi import APIRouter, Depends, HTTPException
from realtime import List
from sqlalchemy.orm import Session

from app.core.services.ai_predict import predictor
from app.schemas import ReviewRecieve, ReviewResponse
from app.db.connection import get_db
from app.db.repository import review_repo
from app.core.services.token import get_current_user
from app.db.models import App

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
    if str(target_app.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this app.")

    # 3. If they pass the security check, get the AI prediction
    prediction_result = predictor.predict_review_category(review.text, review.rating)
    
    # 4. Save the review to the database
    try:
        saved_review = review_repo.save_review(
            db=db, 
            app_id=review.app_id, 
            text=review.text, 
            rating=review.rating, 
            sentiment=prediction_result
        )
        print(f"this is saved_review: {saved_review}")
        # Because of from_attributes=True, Pydantic converts this object directly into JSON!
        return saved_review

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving review: {str(e)}")
    

@router.get("/{app_id}", response_model=List[ReviewResponse])
def get_app_reviews(
    app_id: int, # FastAPI grabs this from the URL (e.g., /reviews/5)
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # The Bouncer!
):
    # SECURITY CHECK: Make sure the user owns the app they are trying to look at
    target_app = db.query(App).filter(App.id == app_id).first()
    
    if not target_app:
        raise HTTPException(status_code=404, detail="App not found.")
    if str(target_app.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Forbidden: You do not own this app.")

    # If they pass security, fetch the reviews!
    reviews = review_repo.get_reviews_by_app(db=db, app_id=app_id)
    return reviews

@router.delete("/{review_id}")
def delete_review_endpoint(
    review_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) # 1. The Bouncer checks if logged in
):
    # 2. Find the review in the database
    # (Assuming you imported Review from app.db.models)
    from app.db.models import Review 
    target_review = db.query(Review).filter(Review.id == review_id).first()
    
    if not target_review:
        raise HTTPException(status_code=404, detail="Review not found.")

    # 3. Find the app this review belongs to
    target_app = db.query(App).filter(App.id == target_review.app_id).first()
    
    if not target_app:
        raise HTTPException(status_code=404, detail="App associated with this review not found.")

    # 4. THE SECURITY CHECK: Does the current user own this app?
    if str(target_app.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=403, 
            detail="Forbidden: You do not own the app this review belongs to."
        )

    # 5. If they pass all checks, delete the review
    try:
        # Using a repo function (defined below) to keep DB logic separate
        review_repo.delete_review_from_db(db=db, review=target_review)
        return {"message": f"Review {review_id} successfully deleted."}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting review: {str(e)}")