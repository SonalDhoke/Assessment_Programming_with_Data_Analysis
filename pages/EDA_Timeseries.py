import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------
# Pastel CSS
# ----------------------------------------------------------
st.markdown("""
<style>
.section-box {
    background-color: #F8FAFF;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E0E7FF;
    margin-bottom: 20px;
}

.plot-container {
    border-radius: 15px;
    padding: 12px;
    background: #ffffff;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

h3 {
    color: #344767;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------------
def show():

    # Load dataset
    df = None
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
    elif "current_df" in st.session_state:
        df = st.session_state.current_df
    elif "original_df" in st.session_state:
        df = st.session_state.original_df

    if df is None:
        st.error("Dataset not available.")
        return

    st.header("🔗 Correlation Matrix Analysis")

    # ----------------------------------------------------------
    # Detect numeric pollutant columns
    # ----------------------------------------------------------
    exclude = {"AQI", "AQI_Bucket", "AQI_Recalc", "AQI_Bucket_Recalc", "City"}
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and c not in exclude]

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ----------------------------------------------------------
    # FILTER PANEL
    # ----------------------------------------------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        method = st.selectbox(
            "Correlation Method",
            ["pearson", "spearman", "kendall"]
        )

    with col2:
        cities = st.multiselect(
            "Filter by City (optional)",
            sorted(df["City"].dropna().unique())
        )

    with col3:
        scale_min = st.number_input("Color Scale Min", -1.0, 1.0, -1.0)
        scale_max = st.number_input("Color Scale Max", -1.0, 1.0, 1.0)

    # Date range filter
    min_date = df["Date"].min()
    max_date = df["Date"].max()

    date_range = st.date_input("Select Date Range", (min_date, max_date))

    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------------
    # APPLY FILTERS
    # ----------------------------------------------------------
    filtered_df = df.copy()

    if cities:
        filtered_df = filtered_df[filtered_df["City"].isin(cities)]

    start, end = date_range
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(start)) &
        (filtered_df["Date"] <= pd.to_datetime(end))
    ]

    if filtered_df.empty:
        st.warning("No data available for selected filters.")
        return

    # ----------------------------------------------------------
    # COMPUTE CORRELATION MATRIX
    # ----------------------------------------------------------
    corr_matrix = filtered_df[num_cols].corr(method=method)

    # ----------------------------------------------------------
    # PLOT HEATMAP (pastel theme)
    # ----------------------------------------------------------
    st.markdown("### 🎨 Correlation Heatmap")
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    fig = px.imshow(
        corr_matrix,
        color_continuous_scale=px.colors.sequential.Blues,
        zmin=scale_min,
        zmax=scale_max,
        text_auto=True,
        aspect="auto",
    )

    fig.update_layout(
        height=550,
        xaxis_title="Pollutants",
        yaxis_title="Pollutants",
        coloraxis_colorbar=dict(
            title="Correlation",
            ticks="outside"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------------
    # DOWNLOAD MATRIX
    # ----------------------------------------------------------
    st.markdown("### 📥 Download Correlation Matrix")
    st.download_button(
        "Download as CSV",
        corr_matrix.to_csv().encode("utf-8"),
        file_name="correlation_matrix.csv",
        mime="text/csv"
    )

    # ----------------------------------------------------------
    # RAW DATA VIEWER
    # ----------------------------------------------------------
    with st.expander("📄 View Filtered Dataset"):
        st.dataframe(filtered_df, use_container_width=True)
