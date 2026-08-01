import streamlit as st

st.set_page_config(
    page_title="Gurgaon Real Estate Analytics",
    page_icon=" ",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 780px;
    }

    .hero-title {
        font-size: 40px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.4rem;
    }
    .hero-sub {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 2rem;
        line-height: 1.5;
    }

    /* Feature card */
    .feature-icon {
        font-size: 28px;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-size: 18px;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.3rem;
    }
    .feature-desc {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 0;
    }

    /* Make st.page_link look like a button inside the card */
    div[data-testid="stPageLink"] {
        margin-top: 0.7rem;
    }
    div[data-testid="stPageLink"] a {
        border: 1.5px solid #6366f1;
        border-radius: 8px;
        padding: 0.4rem 0.9rem;
        color: #4338ca !important;
        font-weight: 600;
        font-size: 14px;
        text-decoration: none !important;
    }
    div[data-testid="stPageLink"] a:hover {
        background-color: #eef2ff;
    }

    .footer-note {
        text-align: center;
        color: #9ca3af;
        font-size: 13px;
        margin-top: 2.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-title"> Gurgaon Real Estate Analytics</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Explore pricing trends, predict property values, and discover apartments '
    'that match what you\'re looking for — all in one place. Use the cards below or the sidebar to get started.</div>',
    unsafe_allow_html=True
)

with st.container(border=True):
    st.markdown('<div class="feature-icon"></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-desc">Dive into pricing trends, sector-level maps, furnishing and luxury impact, and what actually drives price across the market.</div>', unsafe_allow_html=True)
    st.page_link("pages/Analysis.py", label="Open Analytics →")

with st.container(border=True):
    st.markdown('<div class="feature-icon"></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">Predict Price</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-desc">Enter a property\'s details: location, size, furnishing, luxury tier, and get an instant estimated price range.</div>', unsafe_allow_html=True)
    st.page_link("pages/Predict Price.py", label="Open Predict Price →")

with st.container(border=True):
    st.markdown('<div class="feature-icon"></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">Recommend Apartments</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-desc">Search properties near a location within a set radius, or find apartments similar to one you already like.</div>', unsafe_allow_html=True)
    st.page_link("pages/Recommend Apartments.py", label="Open Recommendations →")

st.markdown('<div class="footer-note">Built by Harekrishna Thakur.</div>', unsafe_allow_html=True)