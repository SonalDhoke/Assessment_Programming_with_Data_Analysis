import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------
# Pastel Theme CSS
# ----------------------------------------------------------
st.markdown("""
<style>
/* Section container */
.section-box {
    background-color: #F8FAFF;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E0E7FF;
    margin-bottom: 20px;
}

/* Dropdowns & widgets */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

/* Plot shading */
.plot-container {
    border-radius: 15px;
    padding: 12px;
    background: #ffffff;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

/* Title styling */
h3 {
    color: #344767;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------------
def show():

    # Load dataframe automatically (cleaned or raw)
    df = None
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
    elif "current_df" in st.session_state:
        df = st.session_state.current_df
    elif "original_df" in st.session_state:
        df = st.session_state.original_df

    if df is None:
        st.error("Dataset not found.")
        return

    st.header("📈 Distribution Analysis")
    
    # ----------------------------------------------------------
    # Detect pollutant columns (numeric)
    # ----------------------------------------------------------
    exclude = {"AQI", "AQI_Bucket", "AQI_Recalc", "AQI_Bucket_Recalc", "City", "Date"}
    pollutant_cols = [c for c in df.columns if c not in exclude and pd.api.types.is_numeric_dtype(df[c])]

    if not pollutant_cols:
        st.warning("No numeric pollutant columns found.")
        return

    # ----------------------------------------------------------
    # FILTER BOX
    # ----------------------------------------------------------
    with st.container():
        st.markdown('<div class="section-box">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            pollutant = st.selectbox("Select Pollutant", pollutant_cols)

        with col2:
            cities = st.multiselect(
                "Filter by City (optional)",
                sorted(df["City"].dropna().unique()),
                default=None
            )

        with col3:
            outliers = st.checkbox("Highlight Outliers", value=False)

        # Date Range Filter
        min_date = df["Date"].min()
        max_date = df["Date"].max()

        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date)
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # Apply filters
    filtered_df = df.copy()

    if cities:
        filtered_df = filtered_df[filtered_df["City"].isin(cities)]

    start_date, end_date = date_range
    filtered_df = filtered_df[(filtered_df["Date"] >= pd.to_datetime(start_date)) &
                              (filtered_df["Date"] <= pd.to_datetime(end_date))]

    if filtered_df.empty:
        st.warning("No data available for selected filters.")
        return

    # ----------------------------------------------------------
    # VISUALIZATIONS
    # ----------------------------------------------------------
    st.markdown("### 📊 Distribution Visualizations")

    col_hist, col_box = st.columns([2, 1])

    # -------------------------------
    # Histogram + KDE (left)
    # -------------------------------
    with col_hist:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        fig = px.histogram(
            filtered_df,
            x=pollutant,
            nbins=50,
            marginal="rug",
            opacity=0.75,
            color_discrete_sequence=["#A7C4FF"],
        )

        fig.update_layout(
            title=f"Distribution of {pollutant}",
            xaxis_title=pollutant,
            yaxis_title="Count",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------
    # Boxplot (right)
    # -------------------------------
    with col_box:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        fig2 = px.box(
            filtered_df,
            y=pollutant,
            points="all" if outliers else False,
            color_discrete_sequence=["#FFB3C6"],
        )

        fig2.update_layout(
            title=f"Boxplot of {pollutant}",
            yaxis_title=pollutant,
            showlegend=False
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # Summary Stats
    # ----------------------------------------------------------
    st.markdown("### 📌 Summary Statistics")

    stats_df = filtered_df[pollutant].describe().to_frame().T
    st.dataframe(stats_df, use_container_width=True)

    # ----------------------------------------------------------
    # Show Raw Data
    # ----------------------------------------------------------
    with st.expander("🔎 View Raw Filtered Data"):
        st.dataframe(filtered_df, use_container_width=True)
