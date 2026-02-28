"""
Voice-to-text conversion for civic issue reporting.
Uses SpeechRecognition library with Google Speech API.
"""

import os
from typing import Optional


class VoiceToText:
    """Converts audio recordings to text for issue reporting."""

    def transcribe_file(self, audio_path: str, language: str = "en-IN") -> Optional[str]:
        """
        Transcribe an audio file to text.
        Supports WAV, AIFF, FLAC formats.
        """
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=language)
            return text
        except ImportError:
            print("[VoiceToText] SpeechRecognition not installed")
            return None
        except Exception as e:
            print(f"[VoiceToText] Transcription failed: {e}")
            return None

    def transcribe_bytes(self, audio_bytes: bytes, language: str = "en-IN") -> Optional[str]:
        """Transcribe audio from raw bytes."""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            tmp_path = f.name
        try:
            return self.transcribe_file(tmp_path, language=language)
        finally:
            os.unlink(tmp_path)

    def get_supported_languages(self):
        """Return supported language codes."""
        return {
            "en-IN": "English (India)",
            "hi-IN": "Hindi",
            "bn-IN": "Bengali",
        }


voice_to_text = VoiceToText()
