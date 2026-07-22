import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Flat Price Predictor",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------- Light custom CSS (small, targeted tweaks only) ----------
st.markdown("""
<style>
    /* Tighten the default top padding */
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 780px;
    }

    /* Card-style container (used via st.container(border=True)) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        padding: 0.5rem;
    }

    /* Predict button: full width, slightly taller, bold */
    div.stButton > button {
        width: 100%;
        height: 3rem;
        font-weight: 600;
        border-radius: 10px;
    }

    /* Section subheaders */
    .section-label {
        font-size: 0.95rem;
        font-weight: 600;
        color: #374151;
        margin-top: 0.5rem;
        margin-bottom: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Load artifacts ----------
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

# ---------- Header ----------
st.title("🏠 Flat & House Price Predictor")
st.caption("Fill in the property details below to get an estimated price range.")

# ---------- Inputs, grouped into cards ----------
with st.container(border=True):
    st.markdown('<p class="section-label">Basic details</p>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        property_type = st.selectbox('Property Type', ['flat', 'house'])
        bedrooms = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))
        balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))
    with c2:
        sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
        bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))
        property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))

st.write("")  # small spacer

with st.container(border=True):
    st.markdown('<p class="section-label">Area & extra rooms</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        built_up_area = float(st.number_input('Built Up Area (sqft)', min_value=0.0, step=50.0))
    with c2:
        servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))
    with c3:
        store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

st.write("")

with st.container(border=True):
    st.markdown('<p class="section-label">Finish & quality</p>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
    with c2:
        luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
    with c3:
        floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

st.write("")

# ---------- Predict ----------
predict_clicked = st.button('Predict Price', type="primary")

if predict_clicked:
    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age,
              built_up_area, servant_room, store_room, furnishing_type,
              luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    one_df = pd.DataFrame(data, columns=columns)

    with st.spinner("Estimating price..."):
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = round(base_price - 0.22, 2)
        high = round(base_price + 0.22, 2)

    st.markdown('<p class="section-label">Estimated price range</p>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    m1.metric("Lower bound", f"₹ {round(low, 2)} Cr")
    m2.metric("Upper bound", f"₹ {round(high, 2)} Cr")

    st.success(f"The estimated price is between **₹{round(low, 2)} Cr** and **₹{round(high, 2)} Cr**.")