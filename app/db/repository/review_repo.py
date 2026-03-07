# Functions to save reviews
from sqlalchemy.orm import Session
from app.db.models import Review  # Make sure this imports your Review SQLAlchemy model

def save_review(db: Session, app_id: int, text: str, rating: int, sentiment: str):
    # 1. Package the data into your SQLAlchemy blueprint
    new_review = Review(
        app_id=app_id,
        review_text=text,
        rating=rating,
        sentiment=sentiment
    )
    
    # 2. Add it to the current database session
    db.add(new_review)
    
    # 3. Commit (push) the changes to Supabase
    db.commit()
    
    # 4. Refresh the object to get the auto-generated ID and created_at timestamp
    db.refresh(new_review)
    
    # 5. Return the saved database object (optional, but good practice)
    return new_review

def get_reviews_by_app(db: Session, app_id: int):
    # Fetch all reviews that belong to this specific app
    return db.query(Review).filter(Review.app_id == app_id).all()

def delete_review_from_db(db: Session, review: Review):
    # 1. Stage the deletion
    db.delete(review)
    
    # 2. Commit (push) the changes to Supabase
    db.commit()
    
    return True