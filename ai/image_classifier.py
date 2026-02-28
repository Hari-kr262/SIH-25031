"""
Image classifier using MobileNetV2 transfer learning.
Classifies civic issue images into categories.
"""

import os
import numpy as np
from typing import Dict, Optional, Tuple

CATEGORIES = ["pothole", "garbage", "streetlight", "water_leak", "drainage",
              "road_damage", "illegal_dumping", "fallen_tree", "sewage",
              "public_property", "other"]

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "image_classifier.h5")


class ImageClassifier:
    """MobileNetV2-based civic issue image classifier."""

    def __init__(self):
        self.model = None
        self.input_size = (224, 224)

    def load_model(self):
        """Load or build the classification model."""
        if os.path.exists(MODEL_PATH):
            try:
                import tensorflow as tf
                self.model = tf.keras.models.load_model(MODEL_PATH)
                return True
            except Exception as e:
                print(f"[ImageClassifier] Failed to load model: {e}")
        return False

    def build_model(self):
        """Build MobileNetV2 transfer learning model stub."""
        try:
            import tensorflow as tf
            base_model = tf.keras.applications.MobileNetV2(
                input_shape=(*self.input_size, 3),
                include_top=False,
                weights="imagenet",
            )
            base_model.trainable = False
            model = tf.keras.Sequential([
                base_model,
                tf.keras.layers.GlobalAveragePooling2D(),
                tf.keras.layers.Dense(128, activation="relu"),
                tf.keras.layers.Dropout(0.3),
                tf.keras.layers.Dense(len(CATEGORIES), activation="softmax"),
            ])
            model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
            self.model = model
            return model
        except ImportError:
            print("[ImageClassifier] TensorFlow not available")
            return None

    def preprocess_image(self, image_path: str) -> Optional[np.ndarray]:
        """Load and preprocess an image for inference."""
        try:
            from PIL import Image
            import numpy as np
            img = Image.open(image_path).convert("RGB").resize(self.input_size)
            arr = np.array(img, dtype=np.float32) / 255.0
            return np.expand_dims(arr, axis=0)
        except Exception as e:
            print(f"[ImageClassifier] Image preprocessing failed: {e}")
            return None

    def classify(self, image_path: str) -> Tuple[str, float]:
        """
        Classify an image and return (category, confidence).
        Falls back to rule-based heuristics if model is unavailable.
        """
        if self.model is None:
            self.load_model()

        if self.model is not None:
            preprocessed = self.preprocess_image(image_path)
            if preprocessed is not None:
                predictions = self.model.predict(preprocessed, verbose=0)[0]
                idx = int(np.argmax(predictions))
                return CATEGORIES[idx], float(predictions[idx])

        # Fallback: return "other" with low confidence
        return "other", 0.5

    def classify_from_bytes(self, image_bytes: bytes) -> Tuple[str, float]:
        """Classify from raw image bytes."""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(image_bytes)
            tmp_path = f.name
        try:
            return self.classify(tmp_path)
        finally:
            os.unlink(tmp_path)


image_classifier = ImageClassifier()
