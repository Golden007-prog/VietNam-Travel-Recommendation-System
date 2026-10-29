import pandas as pd
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer

from data_processing import load_and_process_data, preprocess_text
from recommendation import recommend_places


@pytest.fixture(scope="module")
def model():
    df = load_and_process_data("data/processed/places.csv")
    tfidf = TfidfVectorizer().fit(df["description_tokens"])
    return df, tfidf


def test_preprocess_removes_punctuation_digits_and_stopwords():
    assert preprocess_text("Di tích lịch sử và kiến trúc độc đáo, 2 tầng!") == "di_tích lịch_sử kiến_trúc độc_đáo tầng"


def test_preprocess_handles_empty_and_non_string():
    assert preprocess_text("   ") == ""
    assert preprocess_text(None) == ""


def test_dataset_loads_with_descriptions(model):
    df, _ = model
    assert len(df) == 315
    assert (df["description_tokens"].str.strip() != "").all()


def test_recommends_beaches_for_beach_query(model):
    df, tfidf = model
    result = recommend_places("bãi biển hoang sơ để tắm biển", df, tfidf, preprocess_text)
    assert len(result) == 3
    assert result["similarity"].iloc[0] > 0
    assert result["description"].str.contains("biển").all()


def test_province_filter_uses_new_provinces(model):
    df, tfidf = model
    result = recommend_places("di tích lịch sử", df, tfidf, preprocess_text, province="Ninh Bình")
    assert len(result) == 3
    assert (result["province"] == "Ninh Bình").all()
    assert set(result["old_province"]) <= {"Ninh Bình", "Hà Nam", "Nam Định"}


def test_empty_query_returns_empty_frame(model):
    df, tfidf = model
    result = recommend_places("!!!", df, tfidf, preprocess_text)
    assert isinstance(result, pd.DataFrame)
    assert result.empty
