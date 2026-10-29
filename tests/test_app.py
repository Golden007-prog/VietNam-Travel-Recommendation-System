from streamlit.testing.v1 import AppTest

import weather


def test_weather_is_skipped_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    assert weather.get_weather("Khánh Hòa") is None


def test_app_shows_recommendations(monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    at = AppTest.from_file("../main.py", default_timeout=120).run()
    assert not at.exception

    at.text_area[0].input("bãi biển hoang sơ để tắm biển").run()
    at.button[0].click().run()

    assert not at.exception
    assert len(at.subheader) == 3


def test_app_rejects_empty_input(monkeypatch):
    monkeypatch.delenv("OPENWEATHER_API_KEY", raising=False)
    at = AppTest.from_file("../main.py", default_timeout=120).run()
    at.button[0].click().run()
    assert at.error[0].value == "Vui lòng nhập mô tả mong muốn."
