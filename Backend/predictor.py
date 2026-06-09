import os
import sys
import joblib
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass
import re
import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk
# Set the absolute path for NLTK data so Vercel can find it locally
BASE_DIR = Path(__file__).resolve().parent
nltk_data_path = str(BASE_DIR / "nltk_data")
nltk.data.path = [nltk_data_path]

# LOAD SAVED MODEL & VECTORIZER

loaded_model_path = BASE_DIR / "trained_models" / "multinomial_nb_model.pkl"
loaded_vectorizer_path = BASE_DIR / "trained_models" / "tfidf_vectorizer.pkl"
print("Loading pipeline components...")
loaded_model = joblib.load(str(loaded_model_path))
loaded_vectorizer = joblib.load(str(loaded_vectorizer_path))
print("Model and Vectorizer loaded successfully!\n")

def predict_sentiment (text):
    
# TEXT CLEANING PIPELINE

    ps = PorterStemmer()

    stop_words = set(stopwords.words('english'))
    negation_words = {
    'not', 'no', 'never', 'neither', 'nor', 'but', 'cannot', 
    'barely', 'hardly', 'scarcely', 'without', 'against'
    }
    contraction_remnants = {
    'don', 't', 'doesn', 'didn', 'wasn', 'weren', 'haven', 'hasn', 
    'hadn', 'won', 'wouldn', 'shann', 'shouldn', 'can', 'couldn', 
    'isn', 'aren', 'ain'
    }
    all_negations_to_keep = negation_words.union(contraction_remnants)
    stop_words = stop_words - all_negations_to_keep

    def clean_text(text):
        if not isinstance(text, str):
            return ""
        text = text.lower()

    # Clean out URLs and specific employee names
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'mr\.?\s*[a-z]+(\s+[a-z]+)?', '', text)

    # Remove punctuation and numbers
        text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
        text = re.sub(r'\d+', '', text)

    # Tokenize and stem
        words = word_tokenize(text)
        filtered_and_stemmed = [ps.stem(w.strip()) for w in words if w.strip() and (w not in stop_words) and len(w) > 1]

        return " ".join(filtered_and_stemmed)


# INPUT AND PREDICT

    raw_user_review = text
    cleaned_review = clean_text(raw_user_review)
    vectorized_review = loaded_vectorizer.transform([cleaned_review])

    # Generate the numerical prediction
    prediction = loaded_model.predict(vectorized_review)
    predicted_class = prediction[0]

    # Map all THREE numerical outputs correctly based on training labels

    
    if predicted_class == "Good":
        sentiment_result = "Positive ✨"
    elif predicted_class == "Bad":
        sentiment_result = "Negative ⚠️"
    else:
        sentiment_result = f"Unknown Class ({predicted_class})"

    
    # DISPLAY RESULTS
    
    print("--- Prediction Report ---")
    print(f"Raw Input:  \"{raw_user_review}\"")
    print(f"Prediction: {sentiment_result}")

    return sentiment_result