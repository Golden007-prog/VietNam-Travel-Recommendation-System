import re

import pandas as pd
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


# Đọc dữ liệu đã làm sạch (scripts/build_dataset.py) và tiền xử lý
def load_and_process_data(file_path):
    df = pd.read_csv(file_path, keep_default_na=False)
    df["description_tokens"] = df["description"].apply(preprocess_text)
    df = df[df["description_tokens"].str.strip() != ""].reset_index(drop=True)
    return df
