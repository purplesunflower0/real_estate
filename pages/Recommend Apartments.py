import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Recommend Apartments",
    layout="centered",
    initial_sidebar_state="expanded",   # consistent with other pages
)

# ---------- Shared-style CSS (mirrors Predict Price page) ----------
st.markdown("""
<style>
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 780px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        padding: 0.5rem;
    }

    div.stButton > button {
        width: 100%;
        height: 3rem;
        font-weight: 600;
        border-radius: 10px;
    }

    .section-label {
        font-size: 24px;
        font-weight: 600;
        color: #374151;
        margin-top: 0.5rem;
        margin-bottom: 0.25rem;
    }

    .section-sub {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 1rem;
        margin-top: -0.25rem;
    }

    /* Nearby-property row */
    .nearby-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 0.65rem 1rem;
        margin-bottom: 0.5rem;
    }
    .nearby-name {
        font-weight: 500;
        color: #1f2937;
        font-size: 15px;
    }
    .nearby-dist {
        font-size: 13px;
        font-weight: 600;
        color: #2563eb;
        background: #dbeafe;
        border-radius: 999px;
        padding: 0.2rem 0.7rem;
        white-space: nowrap;
    }

    /* Recommendation card */
    .rec-card {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .rec-rank {
        flex-shrink: 0;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        font-weight: 700;
        font-size: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .rec-body {
        flex-grow: 1;
    }
    .rec-name {
        font-weight: 600;
        font-size: 15px;
        color: #1f2937;
        margin-bottom: 0.3rem;
    }
    .rec-bar-track {
        width: 100%;
        height: 6px;
        background: #e5e7eb;
        border-radius: 999px;
        overflow: hidden;
    }
    .rec-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #8b5cf6, #6366f1);
        border-radius: 999px;
    }
    .rec-score {
        flex-shrink: 0;
        font-weight: 700;
        font-size: 14px;
        color: #4338ca;
        min-width: 55px;
        text-align: right;
    }

    .empty-hint {
        color: #9ca3af;
        font-size: 14px;
        font-style: italic;
        padding: 0.5rem 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Load artifacts ----------
location_df_clean = pickle.load(open('datasets/location_distance.pkl', 'rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))


def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

    sim_scores = list(enumerate(cosine_sim_matrix[location_df_clean.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df_clean.index[top_indices].tolist()

    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df


# ---------- Header ----------
st.title("Recommend Apartments")
st.caption("Search apartments near a location, or find similar properties to one you already like.")

# ---------- Section 1: Location + radius search ----------
with st.container(border=True):
    st.markdown('<p class="section-label">Find properties near a location</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Pick a landmark or sector and a search radius to see nearby listed properties.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        selected_location = st.selectbox('Location', sorted(location_df_clean.columns.to_list()))
    with c2:
        radius = st.number_input('Radius (km)', min_value=0.0, step=0.5)

    search_clicked = st.button('Search Properties', type='primary')

    if search_clicked:
        result_ser = location_df_clean[location_df_clean[selected_location] < radius * 1000][selected_location].sort_values()

        if len(result_ser) == 0:
            st.markdown('<p class="empty-hint">No properties found within this radius. Try increasing it.</p>', unsafe_allow_html=True)
        else:
            st.write("")
            st.markdown(f"**{len(result_ser)} propert{'y' if len(result_ser) == 1 else 'ies'} found within {radius:g} km**")
            rows_html = ""
            for key, value in result_ser.items():
                rows_html += f"""
                <div class="nearby-row">
                    <span class="nearby-name">{key}</span>
                    <span class="nearby-dist">{round(value/1000, 1)} km</span>
                </div>
                """
            st.markdown(rows_html, unsafe_allow_html=True)

st.write("")

# ---------- Section 2: Similar apartment recommendations ----------
with st.container(border=True):
    st.markdown('<p class="section-label">Find similar apartments</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Choose an apartment and get the top matches based on amenities, pricing, and location similarity.</p>', unsafe_allow_html=True)

    selected_apartment = st.selectbox('Select an apartment', sorted(location_df_clean.index.to_list()))

    recommend_clicked = st.button('Recommend Similar Apartments', type='primary')

    if recommend_clicked:
        with st.spinner("Finding similar apartments..."):
            recommendation_df = recommend_properties_with_scores(selected_apartment)

        st.write("")
        cards_html = ""
        for i, row in recommendation_df.iterrows():
            pct = row['SimilarityScore'] * 100
            cards_html += f"""
            <div class="rec-card">
                <div class="rec-rank">{i + 1}</div>
                <div class="rec-body">
                    <div class="rec-name">{row['PropertyName']}</div>
                    <div class="rec-bar-track">
                        <div class="rec-bar-fill" style="width: {pct:.1f}%;"></div>
                    </div>
                </div>
                <div class="rec-score">{pct:.1f}%</div>
            </div>
            """
        st.markdown(cards_html, unsafe_allow_html=True)