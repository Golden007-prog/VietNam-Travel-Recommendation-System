import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

RESULT_COLUMNS = ["name", "description", "similarity", "province", "old_province", "image_url"]


def recommend_places(user_input, df, tfidf, preprocess_text, num_recommendations=3, province=None):
    input_text = preprocess_text(user_input)
    if not input_text:
        return pd.DataFrame(columns=RESULT_COLUMNS)

    candidates = df if province is None else df[df["province"] == province]
    if candidates.empty:
        return pd.DataFrame(columns=RESULT_COLUMNS)

    input_vector = tfidf.transform([input_text])
    tfidf_matrix = tfidf.transform(candidates["description_tokens"])
    cosine_sim = cosine_similarity(input_vector, tfidf_matrix).flatten()

    indices = cosine_sim.argsort()[-num_recommendations:][::-1]
    recommendations = candidates.iloc[indices].copy()
    recommendations["similarity"] = (cosine_sim[indices] * 100).round(2)
    return recommendations[RESULT_COLUMNS]
