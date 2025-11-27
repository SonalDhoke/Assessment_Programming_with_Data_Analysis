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
        st.error("Dataset not loaded.")
        return

    st.header("🟢 AQI Category Analysis (Before vs After Recalculation)")

    # ----------------------------------------------------------
    # CHECK REQUIRED COLUMNS
    # ----------------------------------------------------------
    needed_cols = ["AQI", "AQI_Bucket", "AQI_Recalc", "AQI_Bucket_Recalc"]

    missing = [c for c in needed_cols if c not in df.columns]
    if missing:
        st.warning(f"Missing columns: {missing}. Please recalculate AQI in Data Cleaning page.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ----------------------------------------------------------
    # FILTER PANEL
    # ----------------------------------------------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        cities = st.multiselect(
            "Filter by City (optional)",
            sorted(df["City"].dropna().unique())
        )

    with col2:
        date_range = st.date_input(
            "Select Date Range",
            value=(df["Date"].min(), df["Date"].max())
        )

    st.markdown("</div>", unsafe_allow_html=True)

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
    # SUMMARY STATISTICS (Before vs After)
    # ----------------------------------------------------------
    st.subheader("📊 AQI Summary (Before vs After Recalculation)")

    stats_df = pd.DataFrame({
        "Metric": ["Mean", "Median", "Min", "Max"],
        "Original AQI": [
            filtered_df["AQI"].mean(),
            filtered_df["AQI"].median(),
            filtered_df["AQI"].min(),
            filtered_df["AQI"].max()
        ],
        "Recalculated AQI": [
            filtered_df["AQI_Recalc"].mean(),
            filtered_df["AQI_Recalc"].median(),
            filtered_df["AQI_Recalc"].min(),
            filtered_df["AQI_Recalc"].max()
        ]
    })

    st.dataframe(stats_df, use_container_width=True)

    st.markdown("---")

    # ----------------------------------------------------------
    # CATEGORY COUNTS (Before vs After)
    # ----------------------------------------------------------
    st.subheader("📦 Category Distribution Comparison")

    col_before, col_after = st.columns(2)

    # BEFORE
    with col_before:
        st.markdown("### 🟡 Before (AQI_Bucket)")
        fig1 = px.bar(
            filtered_df["AQI_Bucket"].value_counts().reset_index(),
            x="index",
            y="AQI_Bucket",
            color="index",
            text="AQI_Bucket",
            title="AQI Categories (Original)",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig1.update_layout(xaxis_title="Category", yaxis_title="Count")
        st.plotly_chart(fig1, use_container_width=True)

    # AFTER
    with col_after:
        st.markdown("### 🟢 After (AQI_Bucket_Recalc)")
        fig2 = px.bar(
            filtered_df["AQI_Bucket_Recalc"].value_counts().reset_index(),
            x="index",
            y="AQI_Bucket_Recalc",
            color="index",
            text="AQI_Bucket_Recalc",
            title="AQI Categories (Recalculated)",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig2.update_layout(xaxis_title="Category", yaxis_title="Count")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ----------------------------------------------------------
    # SIDE-BY-SIDE CATEGORY CHANGE TABLE
    # ----------------------------------------------------------
    st.subheader("🔄 Category Shift Analysis (Before → After)")

    filtered_df["Category Shift"] = (
        filtered_df["AQI_Bucket"] + " → " + filtered_df["AQI_Bucket_Recalc"]
    )

    shift_counts = filtered_df["Category Shift"].value_counts().reset_index()
    shift_counts.columns = ["Change", "Count"]

    fig_shift = px.bar(
        shift_counts,
        x="Change",
        y="Count",
        color="Change",
        text="Count",
        title="How AQI Categories Changed After Recalculation",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig_shift.update_layout(xaxis_title="Shift", yaxis_title="Count")
    st.plotly_chart(fig_shift, use_container_width=True)

    st.markdown("---")

    # ----------------------------------------------------------
    # CITY-WISE CATEGORY COMPARISON
    # ----------------------------------------------------------
    st.subheader("🏙 City-wise AQI Category Comparison")

    city_compare = filtered_df.groupby("City").agg({
        "AQI": "mean",
        "AQI_Recalc": "mean"
    }).reset_index()

    fig_city = px.bar(
        city_compare,
        x="City",
        y=["AQI", "AQI_Recalc"],
        barmode="group",
        title="Average AQI Before vs After (City-wise)",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig_city.update_layout(yaxis_title="Average AQI")
    st.plotly_chart(fig_city, use_container_width=True)

    # ----------------------------------------------------------
    # RAW DATA VIEWER
    # ----------------------------------------------------------
    with st.expander("📄 View Filtered Data"):
        st.dataframe(filtered_df, use_container_width=True)
