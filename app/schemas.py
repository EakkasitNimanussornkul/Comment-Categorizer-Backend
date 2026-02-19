# Defines Pydantic models (Data validation for inputs/outputs)
from pydantic import BaseModel, Field
from typing import Optional

class ReviewRecieve(BaseModel):
    # description is for /docs
    text: str = Field(..., min_length=1, max_length=1000, description="The review content")
    #ge stands for "greater than or equal to", le stands for "less than or equal to"
    # This means the rating must be between 1 and 5 (inclusive)
    rating: int = Field(..., ge=1, le=5, description="Star rating from 1 to 5")


class ReviewResponse(BaseModel):
    text: str
    rating: int
    sentiment: str  # e.g., "Bug", "Feature", "Noise"
    
    # This config line is for pydantic to read a sql object instead of a dict
    class Config:
        from_attributes = True