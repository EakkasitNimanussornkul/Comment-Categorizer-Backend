import numpy as np
from scipy.sparse import hstack
from app.core.services.text_cleaner import preprocess
import joblib

class ReviewPredictor:
    # Initialize as None
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.scaler = None

    # load the model and vectorizer from disk (called at startup)
    def load_models(self):
        try:
            self.model = joblib.load("model/model_nb.pkl")
            self.vectorizer = joblib.load("model/tfidf_vectorizer.pkl")
            self.scaler = joblib.load("model/scaler.pkl")
            print("AI Models loaded successfully!")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to load models. {e}")
            raise e  # This stops the backend from starting
        
    # takes a raw review text and star rating, returns predicted category 
    # (e.g., "Bug", "Feature Request", "Other")
    # should add some error handling maybe later
    def predict_review_category(self,raw_text: str, star_rating: int):
        
        # Step 1: Clean the text
        cleaned_text = preprocess(raw_text)
        
        # Step 2: Vectorize the text
        text_features = self.vectorizer.transform([cleaned_text])
        
        # Step 3: Scale the score
        score_features = self.scaler.transform([[star_rating]])
        
        # Step 4: Combine them (hstack)
        final_features = hstack([text_features, score_features])
        
        # Step 5: Predict
        prediction = self.model.predict(final_features)
        
        # Return the result (e.g., "Bug")
        return prediction[0]

# Create one global instance to be used everywhere
predictor = ReviewPredictor()