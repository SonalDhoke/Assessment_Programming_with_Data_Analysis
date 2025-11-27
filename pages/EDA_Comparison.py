import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------
# PASTEL CSS
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
</style>
""", unsafe_allow_html=True)


def show():

    # ----------------------------------------------------------
    # LOAD DATA
    # ----------------------------------------------------------
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

    st.header("🔍 Comparison Tool")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ----------------------------------------------------------
    # DETECT POLLUTANTS
    # ----------------------------------------------------------
    exclude = {"AQI", "AQI_Bucket", "AQI_Recalc", "AQI_Bucket_Recalc", "City"}
    pollutant_cols = [
        c for c in df.columns
        if pd.api.types.is_numeric_dtype(df[c]) and c not in exclude
    ]


    # ----------------------------------------------------------
    # FILTER PANEL
    # ----------------------------------------------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        pollutants = st.multiselect(
            "Select Pollutants to Compare",
            pollutant_cols,
            default=pollutant_cols[:2]
        )

    with col2:
        cities = st.multiselect(
            "Select Cities to Compare",
            sorted(df["City"].dropna().unique()),
            default=None
        )

    min_date, max_date = df["Date"].min(), df["Date"].max()

    date_range = st.date_input(
        "Date Range",
        (min_date, max_date)
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # APPLY FILTERS
    # ----------------------------------------------------------
    filtered_df = df.copy()

    s, e = date_range
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(s)) &
        (filtered_df["Date"] <= pd.to_datetime(e))
    ]

    if cities:
        filtered_df = filtered_df[filtered_df["City"].isin(cities)]

    if filtered_df.empty:
        st.warning("No data matches filters.")
        return

    # ----------------------------------------------------------
    # MULTI-POLLUTANT LINE CHART
    # ----------------------------------------------------------
    st.subheader("📈 Pollutant Comparison Over Time")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    if pollutants:
        melted = filtered_df.melt(
            id_vars=["Date", "City"],
            value_vars=pollutants,
            var_name="Pollutant",
            value_name="Value"
        )

        fig_time = px.line(
            melted,
            x="Date",
            y="Value",
            color="Pollutant",
            line_group="City" if cities else None,
            hover_data=["City"],
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Pollutant Levels Over Time"
        )

        st.plotly_chart(fig_time, use_container_width=True)

    else:
        st.info("Select pollutants to show comparison.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # CITY-WISE BAR CHART COMPARISON
    # ----------------------------------------------------------
    st.subheader("🏙 Average Pollutant Comparison (City-wise)")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    if pollutants and cities:
        avg_city = filtered_df.groupby("City")[pollutants].mean().reset_index()

        avg_city_melt = avg_city.melt(
            id_vars="City",
            value_vars=pollutants,
            var_name="Pollutant",
            value_name="Average Value"
        )

        fig_city = px.bar(
            avg_city_melt,
            x="City",
            y="Average Value",
            color="Pollutant",
            barmode="group",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Average Pollutant Levels (City-wise)"
        )

        st.plotly_chart(fig_city, use_container_width=True)

    else:
        st.info("Select both cities and pollutants to compare.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # POLLUTANT-WISE BAR COMPARISON
    # ----------------------------------------------------------
    st.subheader("🔢 Pollutant-wise Comparison (Overall)")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    if pollutants:
        overall_avg = filtered_df[pollutants].mean().reset_index()
        overall_avg.columns = ["Pollutant", "Average Value"]

        fig_poll = px.bar(
            overall_avg,
            x="Pollutant",
            y="Average Value",
            color="Pollutant",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Average Values of Selected Pollutants"
        )

        st.plotly_chart(fig_poll, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # RAW DATA
    # ----------------------------------------------------------
    with st.expander("📄 View Filtered Data"):
        st.dataframe(filtered_df, use_container_width=True)
