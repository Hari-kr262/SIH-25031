"""
Text classifier using TF-IDF + SVM.
Classifies issue descriptions into categories.
"""

import os
import pickle
from typing import Tuple, Optional

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "text_classifier.pkl")

# Training data (minimal examples for demonstration)
TRAINING_DATA = [
    ("pothole on road", "pothole"),
    ("road has big hole", "pothole"),
    ("damaged road surface", "pothole"),
    ("garbage pile on street", "garbage"),
    ("waste not collected", "garbage"),
    ("illegal dumping of waste", "illegal_dumping"),
    ("streetlight not working", "streetlight"),
    ("broken street light", "streetlight"),
    ("water pipe leaking", "water_leak"),
    ("water leak in road", "water_leak"),
    ("drain blocked", "drainage"),
    ("drainage overflow", "drainage"),
    ("tree fallen on road", "fallen_tree"),
    ("road damage after rain", "road_damage"),
    ("sewage overflow", "sewage"),
    ("sewage smell on street", "sewage"),
    ("public property vandalized", "public_property"),
]


class TextClassifier:
    """TF-IDF + SVM civic issue text classifier."""

    def __init__(self):
        self.vectorizer = None
        self.classifier = None

    def train(self):
        """Train the TF-IDF + SVM model on sample data."""
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.svm import SVC
            from sklearn.pipeline import Pipeline

            texts = [d[0] for d in TRAINING_DATA]
            labels = [d[1] for d in TRAINING_DATA]

            pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
                ("svm", SVC(kernel="linear", probability=True)),
            ])
            pipeline.fit(texts, labels)
            self.classifier = pipeline

            os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
            with open(MODEL_PATH, "wb") as f:
                pickle.dump(pipeline, f)
            return True
        except ImportError:
            print("[TextClassifier] scikit-learn not available")
            return False

    def load_model(self):
        """Load pre-trained model from disk."""
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    self.classifier = pickle.load(f)
                return True
            except Exception:
                pass
        return False

    def classify(self, text: str) -> Tuple[str, float]:
        """
        Classify text and return (category, confidence).
        Auto-trains if model not available.
        """
        if self.classifier is None:
            if not self.load_model():
                self.train()

        if self.classifier is not None:
            try:
                category = self.classifier.predict([text])[0]
                proba = self.classifier.predict_proba([text])[0]
                confidence = float(max(proba))
                return category, confidence
            except Exception as e:
                print(f"[TextClassifier] Prediction failed: {e}")

        return self._rule_based_classify(text)

    def _rule_based_classify(self, text: str) -> Tuple[str, float]:
        """Simple keyword-based fallback classification."""
        text_lower = text.lower()
        keywords = {
            "pothole": ["pothole", "hole in road", "road hole"],
            "garbage": ["garbage", "waste", "trash", "litter"],
            "streetlight": ["streetlight", "street light", "lamp", "light not working"],
            "water_leak": ["water leak", "pipe burst", "flooding"],
            "drainage": ["drain", "drainage", "blocked drain"],
            "road_damage": ["road damage", "road broken", "road crack"],
            "sewage": ["sewage", "sewer", "smell"],
            "fallen_tree": ["fallen tree", "tree fallen", "tree blocking"],
            "illegal_dumping": ["illegal dump", "dumping"],
        }
        for category, kws in keywords.items():
            if any(kw in text_lower for kw in kws):
                return category, 0.7
        return "other", 0.5


text_classifier = TextClassifier()
