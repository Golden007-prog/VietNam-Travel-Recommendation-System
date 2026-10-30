import pandas as pd
import pytest

from data_processing import build_features, build_vectorizer, load_and_process_data, preprocess_text
from recommendation import recommend_places


@pytest.fixture(scope="module")
def model():
    df = load_and_process_data("data/processed/places.csv")
    tfidf = build_vectorizer().fit(df["description_tokens"])
    return df, tfidf


def test_preprocess_removes_punctuation_digits_and_stopwords():
    assert preprocess_text("Di tích lịch sử và kiến trúc độc đáo, 2 tầng!") == "di_tích lịch_sử kiến_trúc độc_đáo tầng"


def test_features_keep_syllables_of_compound_words():
    assert build_features("Bãi biển đẹp và lịch sử") == "bãi biển đẹp lịch_sử lịch sử"


def test_preprocess_handles_empty_and_non_string():
    assert preprocess_text("   ") == ""
    assert preprocess_text(None) == ""


def test_dataset_loads_with_descriptions(model):
    df, _ = model
    assert len(df) == 315
    assert (df["description_tokens"].str.strip() != "").all()


def test_recommends_beaches_for_beach_query(model):
    df, tfidf = model
    result = recommend_places("bãi biển hoang sơ để tắm biển", df, tfidf, build_features)
    assert len(result) == 3
    assert result["similarity"].iloc[0] > 0
    assert result["description"].str.contains("biển").all()


def test_province_filter_uses_new_provinces(model):
    df, tfidf = model
    result = recommend_places("di tích lịch sử", df, tfidf, build_features, province="Ninh Bình")
    assert len(result) == 3
    assert (result["province"] == "Ninh Bình").all()
    assert set(result["old_province"]) <= {"Ninh Bình", "Hà Nam", "Nam Định"}


def test_empty_query_returns_empty_frame(model):
    df, tfidf = model
    result = recommend_places("!!!", df, tfidf, build_features)
    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_unknown_province_returns_empty_frame(model):
    df, tfidf = model
    result = recommend_places("di tích lịch sử", df, tfidf, build_features, province="Atlantis")
    assert result.empty
    assert list(result.columns) == ["name", "description", "similarity", "province", "old_province", "image_url"]


def test_results_are_sorted_by_similarity(model):
    df, tfidf = model
    result = recommend_places("chùa cổ", df, tfidf, build_features, num_recommendations=5)
    assert len(result) == 5
    assert result["similarity"].is_monotonic_decreasing
