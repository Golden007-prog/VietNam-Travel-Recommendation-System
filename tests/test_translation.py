import translation


class FakeTranslator:
    def __init__(self, source, target):
        assert (source, target) == ("en", "vi")

    def translate(self, text):
        return {"quiet beach": "bãi biển yên tĩnh"}[text]


class BrokenTranslator(FakeTranslator):
    def translate(self, text):
        raise ConnectionError("translation service unreachable")


def test_translates_english_to_vietnamese(monkeypatch):
    monkeypatch.setattr(translation, "GoogleTranslator", FakeTranslator)
    assert translation.translate_to_vietnamese("quiet beach") == "bãi biển yên tĩnh"


def test_returns_none_when_the_service_fails(monkeypatch):
    monkeypatch.setattr(translation, "GoogleTranslator", BrokenTranslator)
    assert translation.translate_to_vietnamese("quiet beach") is None
