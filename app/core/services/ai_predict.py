import numpy as np
import pandas as pd
from scipy.sparse import hstack
from app.core.services.text_cleaner import preprocess
import joblib

class ReviewPredictor:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.scaler = None

    def load_models(self):
        try:
            self.model = joblib.load("model/model_nb.pkl")
            self.vectorizer = joblib.load("model/tfidf_vectorizer.pkl")
            self.scaler = joblib.load("model/scaler.pkl")
            print("AI Models loaded successfully!")
        except Exception as e:
            print(f"CRITICAL ERROR: Failed to load models. {e}")
            raise e  
        
    def predict_review_category(self, raw_text: str, star_rating: int):
        # Step 1: Clean the text
        cleaned_text = preprocess(raw_text)
        
        # Step 2: Vectorize the text
        text_features = self.vectorizer.transform([cleaned_text])
        
        # Step 3: Scale the score (THE FIX IS HERE)
        # Change 'rating' to whatever column name you used when training!
        score_df = pd.DataFrame([[star_rating]], columns=['score']) 
        score_features = self.scaler.transform(score_df)
        
        # Step 4: Combine them
        final_features = hstack([text_features, score_features])
        
        # Step 5: Predict
        prediction = self.model.predict(final_features)
        
        return prediction[0]

predictor = ReviewPredictor()