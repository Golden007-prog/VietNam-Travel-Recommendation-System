import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer

from data_processing import load_and_process_data, preprocess_text
from recommendation import recommend_places
from translation import translate_to_vietnamese
from weather import get_api_key, get_weather

DATA_PATH = "data/DataSet.xlsx"


@st.cache_resource
def load_model():
    df = load_and_process_data(DATA_PATH)
    tfidf = TfidfVectorizer()
    tfidf.fit(df["Mô tả sau tách"])
    return df, tfidf


df, tfidf = load_model()

st.title("Vietnam Travel Recommendation System")
user_input = st.text_area("Nhập mô tả mong muốn của bạn:")

if st.button("Tìm kiếm"):
    if not user_input.strip():
        st.error("Vui lòng nhập mô tả mong muốn.")
    else:
        if user_input.isascii():
            st.info("Phát hiện ngôn ngữ là tiếng Anh. Đang dịch sang tiếng Việt...")
            translated = translate_to_vietnamese(user_input)
            if translated:
                user_input = translated
                st.write(f"Mô tả: {user_input}")
            else:
                st.warning("Không dịch được, sẽ tìm kiếm với nội dung gốc.")

        recommendations = recommend_places(user_input, df, tfidf, preprocess_text)

        if recommendations.empty:
            st.write("Không tìm thấy địa điểm phù hợp với yêu cầu của bạn.")
        else:
            show_weather = bool(get_api_key())
            for _, row in recommendations.iterrows():
                st.subheader(row["Tên địa điểm"])
                st.write(f"**Mô tả:** {row['Mô tả']}")

                with st.expander("Chi tiết"):
                    col1, col2 = st.columns([3, 2])

                    with col1:
                        st.write(f"**Địa chỉ:** {row['Vị trí']}")
                        weather_info = get_weather(row["Vị trí"]) if show_weather else None
                        if weather_info:
                            st.write(f"**Nhiệt độ:** {weather_info['temperature']}°C")
                            st.write(f"**Thời tiết:** {weather_info['description']}")
                            st.write(f"**Độ ẩm:** {weather_info['humidity']}%")
                            if weather_info["icon"]:
                                st.image(weather_info["icon"], width=80)
                        elif show_weather:
                            st.write("Không thể lấy thông tin thời tiết cho địa điểm này.")

                    with col2:
                        if pd.notnull(row["Ảnh"]):
                            st.image(row["Ảnh"], caption=f"Hình ảnh {row['Tên địa điểm']}", width="stretch")
                        else:
                            st.write("Không có hình ảnh cho địa điểm này.")
