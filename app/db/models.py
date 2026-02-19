#Defines your SQL Database Tables (User, Review)
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    
    # Relationship to Apps
    apps = relationship("App", back_populates="owner")

class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="apps")
    reviews = relationship("Review", back_populates="app")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    review_text = Column(Text)
    predicted_category = Column(String) # Bug, Noise, Feature
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    app_id = Column(Integer, ForeignKey("apps.id"))
    
    # Relationship
    app = relationship("App", back_populates="reviews")