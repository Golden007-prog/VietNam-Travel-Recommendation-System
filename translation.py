from deep_translator import GoogleTranslator


def translate_to_vietnamese(text):
    """Return the Vietnamese translation, or None if the translation service fails."""
    try:
        return GoogleTranslator(source="en", target="vi").translate(text)
    except Exception:
        return None
