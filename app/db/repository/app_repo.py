# Functions to save new apps or find existing ones
from sqlalchemy.orm import Session
from app.db.models import App

def create_app(db: Session, name: str, description: str, user_id: str):
    # 1. Package the data into your SQLAlchemy blueprint
    new_app = App(
        name=name,
        description=description,
        user_id=user_id # This is the secure UUID from the Bouncer
    )
    
    # 2. Stage the new app in the database session
    db.add(new_app)
    
    # 3. Commit (push) the changes to Supabase
    db.commit()
    
    # 4. Refresh the object to get the auto-generated ID 
    db.refresh(new_app)
    
    # 5. Return the saved database object back to the router
    return new_app

def get_user_apps(db: Session, user_id: str):
    # Ask the database for ALL apps that belong to this specific user
    return db.query(App).filter(App.user_id == user_id).all()

def get_app_by_id(db: Session, app_id: int, user_id: str):
    # Find ONE specific app, but strictly ensure it belongs to this user!
    return db.query(App).filter(App.id == app_id, App.user_id == user_id).first()

def delete_app(db: Session, app: App):
    # Tell the database to delete this specific app
    db.delete(app)
    db.commit()