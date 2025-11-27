import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------
# Pastel Theme CSS
# ----------------------------------------------------------
st.markdown("""
<style>
.section-box {
    background-color: #F8FAFF;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E0E7FF;
    margin-bottom: 18px;
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

    # Load dataframe
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

    st.header("🕒 Time-Series Analysis")

    # ----------------------------------------------------------
    # Detect Numeric Pollutants
    # ----------------------------------------------------------
    exclude = {"AQI", "AQI_Bucket", "AQI_Recalc", "AQI_Bucket_Recalc", "City"}
    pollutant_cols = [
        c for c in df.columns
        if c not in exclude and pd.api.types.is_numeric_dtype(df[c])
    ]

    # Ensure Date is datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ----------------------------------------------------------
    # FILTER PANEL
    # ----------------------------------------------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        pollutant = st.selectbox("Select Pollutant", pollutant_cols)

    with col2:
        cities = st.multiselect(
            "Filter by City (optional)",
            sorted(df["City"].dropna().unique())
        )

    with col3:
        roll_window = st.selectbox(
            "Rolling Average Window",
            [None, 7, 14, 30],
            format_func=lambda x: "No Smoothing" if x is None else f"{x}-Day Average"
        )

    show_trend = st.checkbox("Show Linear Trendline", value=False)

    min_date = df["Date"].min()
    max_date = df["Date"].max()

    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date)
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------------
    # FILTER DATA
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
    # APPLY ROLLING AVERAGE
    # ----------------------------------------------------------
    if roll_window is not None:
        filtered_df = filtered_df.sort_values("Date")
        filtered_df[f"{pollutant}_smoothed"] = (
            filtered_df[pollutant].rolling(roll_window, min_periods=1).mean()
        )
        plot_col = f"{pollutant}_smoothed"
    else:
        plot_col = pollutant

    # ----------------------------------------------------------
    # TIME-SERIES PLOT
    # ----------------------------------------------------------
    st.markdown("### 📈 Time-Series Plot")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    fig = px.line(
        filtered_df,
        x="Date",
        y=plot_col,
        color="City" if cities else None,
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )

    title_suffix = f" ({roll_window}-Day Avg)" if roll_window else ""
    fig.update_layout(
        title=f"{pollutant}{title_suffix} Over Time",
        xaxis_title="Date",
        yaxis_title=pollutant,
        hovermode="x unified"
    )

    if show_trend:
        fig.add_traces(
            px.scatter(filtered_df, x="Date", y=plot_col, trendline="ols").data[1:]
        )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------------
    # MULTI-POLLUTANT OVERLAY
    # ----------------------------------------------------------
    st.markdown("### 🔀 Compare Multiple Pollutants")

    with st.expander("Show Comparison Chart"):
        compare_cols = st.multiselect(
            "Select pollutants to compare",
            pollutant_cols,
            default=[pollutant]
        )

        if compare_cols:
            comp_df = filtered_df.copy()
            comp_df = comp_df.melt(
                id_vars=["Date", "City"],
                value_vars=compare_cols,
                var_name="Pollutant",
                value_name="Value"
            )

            fig2 = px.line(
                comp_df,
                x="Date",
                y="Value",
                color="Pollutant",
                markers=True,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            fig2.update_layout(
                title="Multi-Pollutant Comparison Over Time",
                hovermode="x unified"
            )

            st.plotly_chart(fig2, use_container_width=True)

    # ----------------------------------------------------------
    # RAW DATA VIEW
    # ----------------------------------------------------------
    with st.expander("📄 View Filtered Data"):
        st.dataframe(filtered_df, use_container_width=True)
