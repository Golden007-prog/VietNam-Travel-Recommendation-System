import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from underthesea import word_tokenize

# Tạo danh sách stopwords (từ không mang nghĩa)
vietnamese_stopwords = [
    "của",
    "và",
    "là",
    "theo",
    "như",
    "để",
    "trong",
    "có",
    "một",
    "này",
    "với",
    "nhưng",
    "lại",
    "thì",
    "ra",
    "nên",
    "đã",
    "được",
    "rằng",
    "nhất",
    "ở",
    "khi",
]


# Hàm tiền xử lý văn bản
def preprocess_text(text):
    if not isinstance(text, str) or not text.strip():
        return ""
    # Chuyển về chữ thường và loại bỏ ký tự không cần thiết
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)  # Loại bỏ dấu câu
    text = re.sub(r"\d+", "", text)  # Loại bỏ số
    # Tách từ và loại bỏ stopwords
    tokens = word_tokenize(text, format="text").split()
    tokens = [word for word in tokens if word not in vietnamese_stopwords]
    return " ".join(tokens) if tokens else ""


def build_features(text):
    """Segmented words plus the syllables of each compound word.

    A query for "biển" should still match "bãi_biển"; see reports/evaluation.md for the comparison.
    """
    words = preprocess_text(text)
    syllables = [s for word in words.split() if "_" in word for s in word.split("_")]
    return " ".join([words, *syllables]).strip()


def build_vectorizer():
    return TfidfVectorizer(ngram_range=(1, 2))


# Đọc dữ liệu đã làm sạch (scripts/build_dataset.py) và tiền xử lý
def load_and_process_data(file_path):
    df = pd.read_csv(file_path, keep_default_na=False)
    df["description_tokens"] = df["description"].apply(build_features)
    df = df[df["description_tokens"].str.strip() != ""].reset_index(drop=True)
    return df
