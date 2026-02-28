"""Unit tests for AI components."""

from ai.urgency_predictor import UrgencyPredictor
from ai.fake_detector import FakeDetector
from ai.duplicate_detector import DuplicateDetector
from ai.sentiment_analyzer import SentimentAnalyzer


def test_urgency_predictor_water_leak():
    predictor = UrgencyPredictor()
    score = predictor.predict("water_leak", "burst pipe flooding street")
    assert score > 0.8


def test_urgency_predictor_low_priority():
    predictor = UrgencyPredictor()
    score = predictor.predict("other", "minor cosmetic issue")
    assert score < 0.6


def test_fake_detector_short_text():
    detector = FakeDetector()
    is_fake, confidence, reason = detector.analyze("a", "b")
    assert is_fake is True
    assert confidence > 0


def test_fake_detector_valid_report():
    detector = FakeDetector()
    is_fake, confidence, reason = detector.analyze(
        "Large pothole on Main Street",
        "There is a dangerous pothole near the bus stop",
        latitude=23.3, longitude=85.3,
    )
    assert is_fake is False


def test_fake_detector_outside_jharkhand():
    detector = FakeDetector()
    is_fake, confidence, reason = detector.analyze(
        "Issue Title", "Description here", latitude=0.0, longitude=0.0
    )
    assert is_fake is True
    assert "Coordinates" in reason


def test_duplicate_detector_similar():
    detector = DuplicateDetector()
    existing = [
        {"id": 1, "title": "Pothole on Main Road", "description": "large pothole near bus stop",
         "latitude": 23.3, "longitude": 85.3},
    ]
    dupes = detector.find_duplicates(
        "Pothole on Main Road", "large pothole near bus stop",
        23.3, 85.3, existing
    )
    assert len(dupes) > 0
    assert dupes[0]["issue_id"] == 1


def test_duplicate_detector_different():
    detector = DuplicateDetector()
    existing = [
        {"id": 2, "title": "Streetlight not working", "description": "broken light",
         "latitude": 25.0, "longitude": 87.0},
    ]
    dupes = detector.find_duplicates(
        "Garbage pile on street", "overflowing dustbin",
        23.0, 85.0, existing
    )
    assert len(dupes) == 0


def test_sentiment_analyzer_positive():
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("The issue was resolved quickly, excellent work, thank you!")
    assert result["sentiment"] == "positive"


def test_sentiment_analyzer_negative():
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("terrible service, issue still not resolved, very disappointed")
    assert result["sentiment"] == "negative"


def test_sentiment_analyzer_neutral():
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("The team came and looked at the issue")
    assert result["sentiment"] == "neutral"
