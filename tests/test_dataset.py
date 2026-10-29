import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from build_dataset import build, parse_keywords, parse_rating  # noqa: E402
from province_mapping import MERGERS, NEW_PROVINCES, OLD_TO_NEW  # noqa: E402


def test_mapping_covers_63_old_and_34_new_provinces():
    assert len(OLD_TO_NEW) == 63
    assert len(NEW_PROVINCES) == 34
    assert OLD_TO_NEW["Hà Giang"] == "Tuyên Quang"
    assert OLD_TO_NEW["Bình Dương"] == "TP. Hồ Chí Minh"
    assert OLD_TO_NEW["Thừa Thiên Huế"] == "Huế"
    assert OLD_TO_NEW["Quảng Ninh"] == "Quảng Ninh"


def test_each_old_province_merges_into_exactly_one_new_one():
    olds = [old for group in MERGERS.values() for old in group]
    assert len(olds) == len(set(olds))


def test_parse_rating():
    assert parse_rating("4.5/5") == 4.5
    assert parse_rating("4,4/5") == 4.4
    assert parse_rating("47/5") == 4.7
    assert parse_rating("3") == 3.0
    assert parse_rating(float("nan")) is None


def test_parse_keywords_accepts_both_formats():
    assert parse_keywords('"biển" , "chụp ảnh " ,"văn hóa"') == "biển, chụp ảnh, văn hóa"
    assert parse_keywords("núi, thiên nhiên,  hùng vĩ.") == "núi, thiên nhiên, hùng vĩ"
    assert parse_keywords(None) == ""


def test_processed_csv_is_up_to_date():
    expected = build()
    actual = pd.read_csv("data/processed/places.csv", keep_default_na=False)
    assert len(actual) == len(expected) == 315
    assert actual["province"].nunique() == 34
    assert list(actual["province"]) == list(expected["province"])
    assert list(actual["name"]) == list(expected["name"])
