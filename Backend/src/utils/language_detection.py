from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0  # Ensure consistent results

def detect_language(text: str) -> str:
    """Detect the language of the given text."""
    try:
        lang = detect(text)
        return lang
    except Exception as e:
        return "unknown"  # Return unknown if detection fails