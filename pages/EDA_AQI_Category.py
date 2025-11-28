import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# --------------------------------------------------------------
# PAGE LAYOUT
# --------------------------------------------------------------
st.markdown("""
<style>
.section-box {
    background-color: #F7F9FC;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #DFE6F0;
    margin-bottom: 20px;
}
.plot-container {
    background: #FFFFFF;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------------------
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
        st.error("Dataset missing.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.header("🌫️ AQI Category Comparison (Before vs After Imputation)")

    # --------------------------------------------------------------
    # FILTER SECTION
    # --------------------------------------------------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        cities = st.multiselect(
            "Select Cities (Optional)",
            sorted(df["City"].dropna().unique())
        )

    with col2:
        time_group = st.selectbox(
            "Time Granularity",
            ["Yearly", "Monthly", "Weekly"]
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------------
    filtered_df = df.copy()

    if cities:
        filtered_df = filtered_df[filtered_df["City"].isin(cities)]

    if filtered_df.empty:
        st.warning("No data available for selected cities.")
        return

    # --------------------------------------------------------------
    # COMBINED BAR CHART (BEFORE vs AFTER)
    # --------------------------------------------------------------
    st.subheader("📊 Category Distribution (Before vs After)")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    # BEFORE counts
    before_df = (
        filtered_df["AQI_Bucket"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Category", "AQI_Bucket": "Count"})
    )
    before_df["Type"] = "Before"

    # AFTER counts
    after_df = (
        filtered_df["AQI_Bucket_Recalc"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Category", "AQI_Bucket_Recalc": "Count"})
    )
    after_df["Type"] = "After"

    # Combine
    combined = pd.concat([before_df, after_df])

    # Sort categories in correct order
    cat_order = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]
    combined["Category"] = pd.Categorical(combined["Category"], cat_order)

    fig_bar = px.bar(
        combined,
        x="Category",
        y="Count",
        color="Type",
        barmode="group",
        color_discrete_sequence=["#4E79A7", "#F28E2B"],
        text="Count"
    )

    fig_bar.update_layout(
        xaxis_title="AQI Category",
        yaxis_title="Count",
        bargap=0.25,
        template="simple_white"
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------
    # LINE CHART WITH CATEGORY SHADING
    # --------------------------------------------------------------
    st.subheader("📈 AQI Trends (Before vs After)")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    temp = filtered_df.copy()

    # ---------------- Time Grouping ----------------
    if time_group == "Yearly":
        temp["Period"] = temp["Date"].dt.year
        x_label = "Year"

    elif time_group == "Monthly":
        temp["Period"] = temp["Date"].dt.month
        x_label = "Month"
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    elif time_group == "Weekly":
        temp["Period"] = temp["Date"].dt.isocalendar().week.astype(int)
        x_label = "Week Number"

    # Aggregate
    agg = temp.groupby("Period")[["AQI", "AQI_Recalc"]].mean().reset_index()

    # Percent Difference
    agg["Percent_Diff"] = ((agg["AQI_Recalc"] - agg["AQI"]) / agg["AQI"]) * 100

    # Category Function
    def categorize(aqi):
        if aqi <= 50: return "Good"
        elif aqi <= 100: return "Satisfactory"
        elif aqi <= 200: return "Moderate"
        elif aqi <= 300: return "Poor"
        elif aqi <= 400: return "Very Poor"
        else: return "Severe"

    agg["AQI_Category"] = agg["AQI"].apply(categorize)
    agg["AQI_Recalc_Category"] = agg["AQI_Recalc"].apply(categorize)

    # AQI Shading Bands
    bands = [
        ("Good", 0, 50, "rgba(0, 176, 80, 0.18)"),
        ("Satisfactory", 51, 100, "rgba(255, 255, 0, 0.18)"),
        ("Moderate", 101, 200, "rgba(255, 165, 0, 0.18)"),
        ("Poor", 201, 300, "rgba(255, 0, 0, 0.18)"),
        ("Very Poor", 301, 400, "rgba(128, 0, 128, 0.18)"),
        ("Severe", 401, 500, "rgba(128, 64, 0, 0.18)")
    ]

    fig_line = go.Figure()

    # Background shading
    for name, y0, y1, color in bands:
        fig_line.add_shape(
            type="rect",
            x0=agg["Period"].min(),
            x1=agg["Period"].max(),
            y0=y0,
            y1=y1,
            fillcolor=color,
            line=dict(width=0),
            layer="below"
        )

    # Colors
    line_colors = ["#4E79A7", "#F28E2B"]

    # BEFORE Line
    fig_line.add_trace(go.Scatter(
        x=agg["Period"],
        y=agg["AQI"],
        mode="lines+markers",
