from collections import Counter
import random
import re
from datetime import datetime
import nltk
from transformers import pipeline, RobertaTokenizer, RobertaForSequenceClassification
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from spacy import load as spacy_load
from scipy.special import softmax

nltk.download("punkt", quiet=True)
nltk.download("vader_lexicon", quiet=True)

class AdvancedRantAnalyzer:
    def __init__(self):
        """Initialize the analyzer with models and settings."""
        self.nlp = spacy_load("en_core_web_md")
        self.vader = SentimentIntensityAnalyzer()
        self.emotion_classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True,
        )
        self.tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
        self.model = RobertaForSequenceClassification.from_pretrained(
            "cardiffnlp/twitter-roberta-base-sentiment"
        )

    def analyze(self, text, user_id):
        """Analyze the given text for sentiment, emotion, and patterns."""
        vader_scores = self.vader.polarity_scores(text)
        emotion_results = self.detect_emotion_transformer(text)
        return {"sentiment": vader_scores, "emotions": emotion_results}

    def detect_emotion_transformer(self, text):
        """Use transformer models to detect emotions in the text."""
        results = self.emotion_classifier(text)[0]
        return {item["label"]: item["score"] for item in results}

    def generate_response(self, analysis_results):
        """Generate a human-like response based on analysis."""
        primary_emotion = max(analysis_results["emotions"], key=analysis_results["emotions"].get)
        return f"I sense you're feeling a lot of {primary_emotion}. It's important to take a moment to process your emotions."