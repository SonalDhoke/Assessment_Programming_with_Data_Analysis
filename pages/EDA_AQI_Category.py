import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------------------
# CSS for layout & pastel-dark theme
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
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------------------
def show():

    # Load dataset
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df.copy()
    elif "current_df" in st.session_state:
        df = st.session_state.current_df.copy()
    else:
        df = st.session_state.original_df.copy()

    if df is None:
        st.error("Dataset unavailable.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.header("🌫️ AQI Category Analysis (Before vs After Recalculation)")

    # --------------------------------------------------------------
    # FILTERS
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
            "Time Grouping",
            ["Yearly", "Monthly", "Weekly"]
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply city filter
    data = df.copy()
    if cities:
        data = data[data["City"].isin(cities)]

    if data.empty:
        st.warning("No data available for selected cities.")
        return

    # --------------------------------------------------------------
    # 1️⃣ COMBINED BAR CHART (Before vs After)
    # --------------------------------------------------------------
    st.subheader("📊 AQI Category Distribution (Before vs After)")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    # BEFORE
    before_df = data["AQI_Bucket"].value_counts().reset_index()
    before_df.columns = ["Category", "Count"]
    before_df["Type"] = "Before"

    # AFTER
    after_df = data["AQI_Bucket_Recalc"].value_counts().reset_index()
    after_df.columns = ["Category", "Count"]
    after_df["Type"] = "After"

    # Merge
    combined = pd.concat([before_df, after_df], ignore_index=True)

    category_order = [
        "Good", "Satisfactory", "Moderate",
        "Poor", "Very Poor", "Severe"
    ]

    combined["Category"] = pd.Categorical(combined["Category"], category_order)

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
        yaxis_title="Total Records",
        bargap=0.25,
        template="simple_white"
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------
    # 2️⃣ LINE CHART WITH AQI CATEGORY SHADING
    # --------------------------------------------------------------
    st.subheader("📈 AQI Trend Comparison (Before vs After)")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    temp = data.copy()

    # ---------------- Time grouping logic ----------------
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
        x_label = "Week"

    # Aggregate
    agg = temp.groupby("Period")[["AQI", "AQI_Recalc"]].mean().reset_index()
    agg["Percent_Diff"] = ((agg["AQI_Recalc"] - agg["AQI"]) / agg["AQI"]) * 100

    # Category function
    def categorize(aqi):
        if aqi <= 50: return "Good"
        elif aqi <= 100: return "Satisfactory"
        elif aqi <= 200: return "Moderate"
        elif aqi <= 300: return "Poor"
        elif aqi <= 400: return "Very Poor"
        else: return "Severe"

    agg["AQI_Category"] = agg["AQI"].apply(categorize)
    agg["AQI_Recalc_Category"] = agg["AQI_Recalc"].apply(categorize)

    # AQI SHADING BANDS
    bands = [
        ("Good", 0, 50, "rgba(0, 176, 80, 0.18)"),
        ("Satisfactory", 51, 100, "rgba(255, 255, 0, 0.18)"),
        ("Moderate", 101, 200, "rgba(255, 165, 0, 0.18)"),
        ("Poor", 201, 300, "rgba(255, 0, 0, 0.18)"),
        ("Very Poor", 301, 400, "rgba(128, 0, 128, 0.18)"),
        ("Severe", 401, 500, "rgba(128, 64, 0, 0.18)")
    ]

    fig = go.Figure()

    # ------------------- SHADING -------------------
    x_min = agg["Period"].min()
    x_max = agg["Period"].max()

    for name, y0, y1, color in bands:
        fig.add_shape(
            type="rect",
            x0=x_min, x1=x_max,
            y0=y0, y1=y1,
            fillcolor=color,
            line=dict(width=0),
            layer="below"
        )

    # ------------------- LINES ---------------------
    colors = ["#4E79A7", "#F28E2B"]
    lines = ["AQI", "AQI_Recalc"]

    for line_name, clr in zip(lines, colors):
        category_col = "AQI_Category" if line_name == "AQI" else "AQI_Recalc_Category"

        fig.add_trace(go.Scatter(
            x=agg["Period"],
            y=agg[line_name],
            mode="lines+markers",
            name=line_name,
            line=dict(color=clr, width=3),
            marker=dict(size=8),
            customdata=agg[["Percent_Diff", category_col]].values,
            hovertemplate=
                "<b>%{fullData.name}</b><br>" +
                f"{x_label}: %{x}<br>" +
                "AQI: %{y:.1f}<br>" +
                "Δ %: %{customdata[0]:.2f}%<br>" +
                "Category: %{customdata[1]}<extra></extra>"
        ))

    # ---------------- Month name labels ----------------
    if time_group == "Monthly":
        fig.update_xaxes(
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=month_names
        )

    # ---------------- Layout ----------------
    fig.update_layout(
        template="simple_white",
        xaxis_title=x_label,
        yaxis_title="AQI",
        height=520,
        legend_title="AQI Lines",
        plot_bgcolor="#FFFFFF"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
