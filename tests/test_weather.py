import requests

import weather

PAYLOAD = {
    "main": {"temp": 28.46, "humidity": 74},
    "weather": [{"description": "mây rải rác", "icon": "03d"}],
}


class FakeResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload


def fake_api(monkeypatch, *responses):
    """Answer successive requests.get calls with `responses`; return the list of requests sent."""
    monkeypatch.setenv("OPENWEATHER_API_KEY", "test-key")
    queue, sent = list(responses), []

    def fake_get(url, params, timeout):
        sent.append(params)
        response = queue.pop(0)
        if isinstance(response, Exception):
            raise response
        return response

    monkeypatch.setattr(weather.requests, "get", fake_get)
    return sent


def test_returns_rounded_reading_and_icon_url(monkeypatch):
    sent = fake_api(monkeypatch, FakeResponse(200, PAYLOAD))

    assert weather.get_weather("Khánh Hòa") == {
        "temperature": 28.5,
        "description": "mây rải rác",
        "humidity": 74,
        "icon": "https://openweathermap.org/img/wn/03d@2x.png",
    }
    assert sent == [{"q": "Khanh Hoa,VN", "appid": "test-key", "units": "metric", "lang": "vi"}]


def test_retries_with_tinh_prefix_when_the_name_is_not_found(monkeypatch):
    sent = fake_api(monkeypatch, FakeResponse(404), FakeResponse(200, PAYLOAD))

    assert weather.get_weather("Hà Giang")["temperature"] == 28.5
    assert [p["q"] for p in sent] == ["Ha Giang,VN", "Tinh Ha Giang,VN"]


def test_returns_none_when_both_queries_fail(monkeypatch):
    fake_api(monkeypatch, FakeResponse(404), FakeResponse(500))
    assert weather.get_weather("Hà Giang") is None


def test_network_errors_count_as_failures(monkeypatch):
    fake_api(monkeypatch, requests.ConnectionError(), requests.Timeout())
    assert weather.get_weather("Huế") is None


def test_missing_fields_fall_back_to_defaults(monkeypatch):
    fake_api(monkeypatch, FakeResponse(200, {}))
    assert weather.get_weather("Huế") == {"temperature": 0, "description": "", "humidity": 0, "icon": None}


def test_api_key_is_read_from_the_environment_and_trimmed(monkeypatch):
    monkeypatch.setenv("OPENWEATHER_API_KEY", "  abc  ")
    assert weather.get_api_key() == "abc"
    monkeypatch.delenv("OPENWEATHER_API_KEY")
    assert weather.get_api_key() == ""
