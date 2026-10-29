# Vietnam Travel Recommendation System

## Overview

The Vietnam Travel Recommendation System is a web application built using Streamlit that assists users in discovering suitable travel destinations in Vietnam based on their interests. By entering keywords related to their preferences, users receive personalized recommendations along with relevant information such as weather conditions and images of the locations.

## Features

- **Description-Based Recommendations:** Users describe the trip they want and get the three most similar destinations (TF-IDF + cosine similarity).
- **Weather Information:** The application fetches real-time weather data for the recommended locations.
- **Image Display:** Each recommended location is accompanied by an image for better visualization.
- **English Input:** English descriptions are translated to Vietnamese before matching; weather descriptions come in Vietnamese from OpenWeatherMap.

## Technologies Used

- **Programming Language:** Python
- **Web Framework:** Streamlit
- **Data Manipulation:** Pandas
- **Natural Language Processing:** Underthesea (for Vietnamese word tokenization)
- **Machine Learning:** Scikit-learn (for TF-IDF and cosine similarity)
- **API Requests:** Requests (for fetching weather data)
- **Translation:** deep-translator (English input to Vietnamese)

## Installation

Requires Python 3.11+.

```bash
git clone https://github.com/HongTin2104/VietNam-Travel-Recommendation-System.git
cd VietNam-Travel-Recommendation-System
pip install -r requirements.txt
streamlit run main.py
```

Then open http://localhost:8501 and describe the trip you want (for example "bãi biển hoang sơ để tắm biển").
English input is translated to Vietnamese before matching.

Weather is optional. To enable it, get a free key from
[OpenWeatherMap](https://home.openweathermap.org/api_keys), copy `.env.example` to `.env` and set
`OPENWEATHER_API_KEY`. Never commit `.env`.

### Docker

```bash
docker build -t vietnam-travel .
docker run --env-file .env -p 8501:8501 vietnam-travel
```

### Tests

```bash
pip install pytest ruff
ruff check . && pytest
```

## Example

![demov2](https://github.com/user-attachments/assets/48d31579-e4c0-4bf6-8612-1bf72b21025f)



