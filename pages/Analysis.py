import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Real Estate Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Shared-style CSS (mirrors other pages) ----------
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        padding: 0.5rem;
    }

    .section-label {
        font-size: 22px;
        font-weight: 600;
        color: #374151;
        margin-top: 0.25rem;
        margin-bottom: 0.1rem;
    }

    .section-sub {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 1rem;
    }

    /* ---- Button-like bordered tabs, no emojis ---- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        flex-wrap: wrap;
        border-bottom: none;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        border: 1.5px solid #e5e7eb;
        border-radius: 999px;
        padding: 0.55rem 1.1rem;
        font-weight: 500;
        color: #4b5563;
        background-color: transparent;
        transition: all 0.15s ease-in-out;
    }
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #6366f1;
        color: #4338ca;
        background-color: #eef2ff;
    }
    .stTabs [aria-selected="true"] {
        border-color: #6366f1 !important;
        background-color: #6366f1 !important;
        color: white !important;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Load data ----------
new_df = pd.read_csv('datasets/data_viz1.csv')

with open('datasets/sector_feature_text.pkl', 'rb') as f:
    sector_feature_text = pickle.load(f)

group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()

# ---------- Header ----------
st.title("Real Estate Analytics")
st.caption("Explore pricing trends, sector-level features, and property distributions across the market.")

(tab_map, tab_words, tab_area, tab_bhk, tab_range, tab_dist,
 tab_furnish, tab_luxury, tab_corr, tab_sectors) = st.tabs([
    "Geomap", "Wordcloud", "Area vs Price", "BHK Split", "Price Range",
    "Distribution", "Furnishing Impact", "Luxury Impact", "What Drives Price", "Top Sectors"
])

# ---------- Tab 1: Geomap ----------
with tab_map:
    st.markdown('<p class="section-label">Sector Price per Sqft Geomap</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Bubble size reflects average built-up area; color reflects average price per sqft.</p>', unsafe_allow_html=True)

    fig = px.scatter_mapbox(
        group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
        mapbox_style="open-street-map", height=650, hover_name=group_df.index
    )
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

# ---------- Tab 2: Wordcloud ----------
with tab_words:
    st.markdown('<p class="section-label">Features Wordcloud</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Most commonly mentioned amenities and features, by sector.</p>', unsafe_allow_html=True)

    selected_sector = st.selectbox('Select Sector', sorted(sector_feature_text.keys()), key='wc_sector')
    feature_text = sector_feature_text[selected_sector]

    if feature_text.strip():
        wordcloud = WordCloud(width=800, height=800,
                               background_color='black',
                               stopwords=set(['s']),
                               min_font_size=10).generate(feature_text)
        fig_wc, ax = plt.subplots(figsize=(8, 8), facecolor=None)
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        plt.tight_layout(pad=0)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.pyplot(fig_wc)
    else:
        st.warning(f"No feature data available for {selected_sector}")

# ---------- Tab 3: Area vs Price ----------
with tab_area:
    st.markdown('<p class="section-label">Area vs Price</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Relationship between built-up area and price, colored by bedroom count.</p>', unsafe_allow_html=True)

    property_type = st.selectbox('Select Property Type', ['flat', 'house'], key='area_price_type')
    filtered_df = new_df[new_df['property_type'] == property_type]

    fig1 = px.scatter(
        filtered_df, x="built_up_area", y="price", color="bedRoom",
        title=None, height=550
    )
    st.plotly_chart(fig1, use_container_width=True)

# ---------- Tab 4: BHK Pie ----------
with tab_bhk:
    st.markdown('<p class="section-label">BHK Distribution</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Share of listings by number of bedrooms.</p>', unsafe_allow_html=True)

    sector_options = new_df['sector'].unique().tolist()
    sector_options.insert(0, 'overall')
    selected_sector_bhk = st.selectbox('Select Sector', sector_options, key='bhk_sector')

    if selected_sector_bhk == 'overall':
        fig2 = px.pie(new_df, names='bedRoom', height=500)
    else:
        fig2 = px.pie(new_df[new_df['sector'] == selected_sector_bhk], names='bedRoom', height=500)

    st.plotly_chart(fig2, use_container_width=True)

# ---------- Tab 5: BHK Price Range ----------
with tab_range:
    st.markdown('<p class="section-label">Side-by-Side BHK Price Comparison</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Price spread across 1-4 BHK configurations.</p>', unsafe_allow_html=True)

    fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', height=550)
    st.plotly_chart(fig3, use_container_width=True)

# ---------- Tab 6: Distribution ----------
with tab_dist:
    st.markdown('<p class="section-label">Price Distribution by Property Type</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">How house and flat prices are distributed across the market.</p>', unsafe_allow_html=True)

    fig4, ax = plt.subplots(figsize=(10, 4.5))
    sns.kdeplot(new_df[new_df['property_type'] == 'house']['price'], label='house', fill=True, alpha=0.3, ax=ax)
    sns.kdeplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat', fill=True, alpha=0.3, ax=ax)
    ax.set_xlabel("Price (Cr)")
    ax.set_ylabel("Density")
    ax.legend()
    st.pyplot(fig4)

# ---------- Tab 7: Furnishing Impact ----------
with tab_furnish:
    st.markdown('<p class="section-label">Does Furnishing Affect Price?</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Price spread for unfurnished, semi-furnished, and furnished properties.</p>', unsafe_allow_html=True)
 
    furnishing_labels = {0: 'unfurnished', 1: 'semi-furnished', 2: 'furnished'}
    furnish_plot_df = new_df.copy()
    furnish_plot_df['furnishing_type'] = furnish_plot_df['furnishing_type'].astype(int).map(furnishing_labels)
 
    fig5 = px.box(
        furnish_plot_df, x='furnishing_type', y='price', color='furnishing_type',
        category_orders={'furnishing_type': ['unfurnished', 'semi-furnished', 'furnished']},
        height=550
    )
    fig5.update_layout(showlegend=False, xaxis_title=" ", yaxis_title="Price (Cr)")
    st.plotly_chart(fig5, use_container_width=True)

# ---------- Tab 8: Luxury Impact ----------
with tab_luxury:
    st.markdown('<p class="section-label">Does Luxury Tier Affect Price?</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Average price and price per sqft across luxury categories.</p>', unsafe_allow_html=True)

    luxury_avg = new_df.groupby('luxury_score')[['price', 'price_per_sqft']].mean().reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig6a = px.bar(luxury_avg, x='luxury_score', y='price', color='luxury_score', height=450)
        fig6a.update_layout(showlegend=False, xaxis_title="Luxury Category", yaxis_title="Avg Price (Cr)")
        st.plotly_chart(fig6a, use_container_width=True)
    with c2:
        fig6b = px.bar(luxury_avg, x='luxury_score', y='price_per_sqft', color='luxury_score', height=450)
        fig6b.update_layout(showlegend=False, xaxis_title="Luxury Category", yaxis_title="Avg Price/Sqft")
        st.plotly_chart(fig6b, use_container_width=True)

# ---------- Tab 9: Correlation Heatmap ----------
with tab_corr:
    st.markdown('<p class="section-label">What Drives Price?</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Correlation between price and other numeric property attributes. Values closer to 1 or -1 indicate a stronger relationship.</p>', unsafe_allow_html=True)

    numeric_cols = ['price', 'price_per_sqft', 'built_up_area', 'bedRoom', 'bathroom']
    available_cols = [c for c in numeric_cols if c in new_df.columns]
    corr = new_df[available_cols].corr()

    fig7, ax = plt.subplots(figsize=(7, 5.5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="rocket_r", ax=ax, cbar_kws={'label': 'Correlation'})
    st.pyplot(fig7)

# ---------- Tab 10: Top Sectors ----------
with tab_sectors:
    st.markdown('<p class="section-label">Top Sectors by Average Price</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">The highest-priced sectors on average, useful for spotting premium micro-markets.</p>', unsafe_allow_html=True)

    top_n = st.slider('Number of sectors to show', min_value=5, max_value=25, value=10, key='top_n_sectors')
    top_sectors_df = new_df.groupby('sector')['price'].mean().sort_values(ascending=False).head(top_n).reset_index()

    fig8 = px.bar(
        top_sectors_df, x='price', y='sector', orientation='h',
        height=max(400, top_n * 32), color='price', color_continuous_scale='Blues'
    )
    fig8.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_title="Avg Price (Cr)", yaxis_title="")
    st.plotly_chart(fig8, use_container_width=True)