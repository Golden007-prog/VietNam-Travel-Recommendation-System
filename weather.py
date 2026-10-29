import os

import requests
from dotenv import load_dotenv
from unidecode import unidecode

load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_api_key():
    return os.getenv("OPENWEATHER_API_KEY", "").strip()


def fetch_weather(query, api_key):
    params = {"q": query, "appid": api_key, "units": "metric", "lang": "vi"}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.RequestException:
        return None
    return response.json() if response.status_code == 200 else None


def get_weather(city):
    api_key = get_api_key()
    if not api_key:
        return None

    # OpenWeatherMap matches province names without diacritics more reliably.
    city_no_diacritics = unidecode(city)
    data = fetch_weather(f"{city_no_diacritics},VN", api_key)
    if data is None:
        data = fetch_weather(f"Tinh {city_no_diacritics},VN", api_key)
    if data is None:
        return None

    main = data.get("main", {})
    weather = data.get("weather", [{}])[0]
    icon = weather.get("icon")
    return {
        "temperature": round(main.get("temp", 0), 1),
        "description": weather.get("description", ""),
        "humidity": main.get("humidity", 0),
        "icon": f"https://openweathermap.org/img/wn/{icon}@2x.png" if icon else None,
    }
