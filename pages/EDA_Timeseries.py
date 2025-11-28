import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------
# Pastel CSS
# ------------------------------------------
st.markdown("""
<style>
.section-box {
    background-color: #F8FAFF;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E0E7FF;
    margin-bottom: 22px;
}

.grid-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 22px;
    margin-top: 15px;
}

.plot-box {
    background: #ffffff;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------
# MAIN FUNCTION
# ------------------------------------------
def show():

    # ------------------- Load Data -----------------------
    df = None
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
    elif "current_df" in st.session_state:
        df = st.session_state.current_df
    else:
        df = st.session_state.original_df

    if df is None:
        st.error("Dataset not found.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.header("📉 Time-Series Analysis")

    # ---------------- Detect pollutant columns ----------------
    exclude = {"City", "AQI", "AQI_Recalc", "AQI_Bucket", "AQI_Bucket_Recalc"}
    pollutants = [
        col for col in df.columns
        if col not in exclude and pd.api.types.is_numeric_dtype(df[col])
    ]

    # ---------------- Sidebar Filters ----------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        pollutant = st.selectbox("Select Pollutant", pollutants)

    with col2:
        cities = st.multiselect(
            "Select Cities",
            sorted(df["City"].dropna().unique()),
            default=None
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # If no cities selected → auto-select all
    if not cities:
        cities = sorted(df["City"].dropna().unique())

    # Filter dataset
    df = df[df["City"].isin(cities)]

    # ----------------- GRID LAYOUT ------------------

    st.markdown("### 📊 City-wise Time Series (Grid Layout)")
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)

    # Pastel line colors
    pastel_colors = px.colors.qualitative.Pastel2

    # Create charts
    for i, city in enumerate(cities):
        city_df = df[df["City"] == city].sort_values("Date")

        st.markdown('<div class="plot-box">', unsafe_allow_html=True)

        fig = px.line(
            city_df,
            x="Date",
            y=pollutant,
            title=f"{city} — {pollutant} Trend",
            markers=False,
            color_discrete_sequence=[pastel_colors[i % len(pastel_colors)]]
        )

        fig.update_layout(
            xaxis_title="",
            yaxis_title="",
            title_font_size=16,
            margin=dict(l=10, r=10, t=40, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close grid

    # ---------------- Summary Statistics ------------------
    st.markdown("### 📌 Summary Statistics (All Selected Cities Combined)")
    summary = df.groupby("City")[pollutant].describe()
    st.dataframe(summary, use_container_width=True)
