# A complete Python backend using FastAPI
import os
import sys


try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from predictor import predict_sentiment

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI()

# Allow origins to be configured dynamically, default to "*" (allow all) for local development
allowed_origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],      # Allows all HTTP methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],      # Allows all headers
)


class ReviewData(BaseModel):
    review: str

@app.post("/predict")
def get_prediction(data: ReviewData):
    # Catch the request directly from the frontend
    text = data.review
    #print(text)
    result = predict_sentiment(text)
    
    
    return {"result": result}