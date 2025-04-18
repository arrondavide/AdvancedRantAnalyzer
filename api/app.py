from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from scipy.special import softmax
import re
import nltk
import os

# Set environment variables for writable cache directories
os.environ["NLTK_DATA"] = "/tmp/nltk_data"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/.cache/huggingface"

# Download necessary NLTK data
nltk.download("punkt", quiet=True)
nltk.download("vader_lexicon", quiet=True)

# Initialize FastAPI
app = FastAPI(title="Advanced Rant Analyzer API", version="1.0")

# Load NLP models and pipelines
nlp = spacy.load("en_core_web_md")
vader = SentimentIntensityAnalyzer()
device = 0 if torch.cuda.is_available() else -1

# Load Hugging Face Transformers pipelines
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True,
    device=device,
)
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
roberta_model = AutoModelForSequenceClassification.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment"
).to(device)

# Input data model
class RantInput(BaseModel):
    text: str
    quick_mode: Optional[bool] = False


@app.post("/analyze")
def analyze_rant(rant_input: RantInput):
    """Analyze the rant and return insights."""
    try:
        text = rant_input.text
        quick_mode = rant_input.quick_mode

        # Perform sentiment analysis (VADER and RoBERTa)
        vader_scores = vader.polarity_scores(text)
        encoded_text = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(device)
        roberta_output = roberta_model(**encoded_text)
        roberta_scores = softmax(roberta_output.logits[0].detach().cpu().numpy())
        roberta_sentiment = {
            "negative": float(roberta_scores[0]),
            "neutral": float(roberta_scores[1]),
            "positive": float(roberta_scores[2]),
        }

        # Detect emotional themes (simplified for speed in quick_mode)
        emotion_results = emotion_classifier(text)[0] if not quick_mode else {}

        # Detect intensity (caps, punctuation, etc.)
        caps_count = len(re.findall(r"\b[A-Z]{2,}\b", text))
        exclamation_count = text.count("!")
        intensity_score = min(caps_count * 0.05 + exclamation_count * 0.02, 1.0)

        # Return results
        return {
            "sentiment_vader": vader_scores,
            "sentiment_roberta": roberta_sentiment,
            "emotion_results": emotion_results,
            "intensity_score": intensity_score,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing rant: {str(e)}")