import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------------------
# CSS for page layout
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

    # ---------------- Load dataset ----------------
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df.copy()
    elif "current_df" in st.session_state:
        df = st.session_state.current_df.copy()
    else:
        df = st.session_state.original_df.copy()

    if df is None:
        st.error("Dataset missing.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.header("🌫️ AQI Category Comparison (Before vs After)")

    # --------------------------------------------------------------
    # FILTERS SECTION
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
            "Choose Time Granularity",
            ["Yearly", "Monthly", "Weekly"]
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Apply Filters ----------------
    filtered = df.copy()
    if cities:
        filtered = filtered[filtered["City"].isin(cities)]

    if filtered.empty:
        st.warning("No data found for selected filters.")
        return

    # --------------------------------------------------------------
    # 1) COMBINED BAR CHART (Before vs After)
    # --------------------------------------------------------------
    st.subheader("📊 AQI Category Distribution (Before vs After)")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    # BEFORE
    before_df = (
        filtered["AQI_Bucket"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Category", "AQI_Bucket": "Count"})
    )
    before_df["Type"] = "Before"

    # AFTER
    after_df = (
        filtered["AQI_Bucket_Recalc"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Category", "AQI_Bucket_Recalc": "Count"})
    )
    after_df["Type"] = "After"

    # Merge
    combined = pd.concat([before_df, after_df])

    # Category order
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
        yaxis_title="Record Count",
        bargap=0.25,
        template="simple_white"
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------------------------------
    # 2) LINE CHART WITH CATEGORY SHADING
    # --------------------------------------------------------------
    st.subheader("📈 AQI Trends With Category Shading")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    temp = filtered.copy()

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
        x_label = "Week"

    # Aggregate AQI & AQI_Recalc
    agg = temp.groupby("Period")[["AQI", "AQI_Recalc"]].mean().reset_index()

    # Percent Difference
    agg["Percent_Diff"] = ((agg["AQI_Recalc"] - agg["AQI"]) / agg["AQI"]) * 100

    # Correct Category Function
    def categorize(aqi):
        if aqi <= 50: return "Good"
        elif aqi <= 100: return "Satisfactory"
        elif aqi <= 200: return "Moderate"
        elif aqi <= 300: return "Poor"
        elif aqi <= 400: return "Very Poor"
        else: return "Severe"

    agg["AQI_Category"] = agg["AQI"].apply(categorize)
    agg["AQI_Recalc_Category"] = agg["AQI_Recalc"].apply(categorize)

    # AQI Shades
    bands = [
        ("Good", 0, 50, "rgba(0, 176, 80, 0.18)"),
        ("Satisfactory", 51, 100, "rgba(255, 255, 0, 0.18)"),
        ("Moderate", 101, 200, "rgba(255, 165, 0, 0.18)"),
        ("Poor", 201, 300, "rgba(255, 0, 0, 0.18)"),
        ("Very Poor", 301, 400, "rgba(128, 0, 128, 0.18)"),
        ("Severe", 401, 500, "rgba(128, 64, 0, 0.18)")
    ]

    fig = go.Figure()

    # ---------------- Background Shading ----------------
    for name, y0, y1, color in bands:
        fig.add_shape(
            type="rect",
            x0=agg["Period"].min(),
            x1=agg["Period"].max(),
            y0=y0,
            y1=y1,
            fillcolor=color,
            line=dict(width=0),
            layer="below"
        )

    # ---------------- Lines ----------------
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
                "AQI Value: %{y:.1f}<br>" +
                "Percent Difference: %{customdata[0]:.2f}%<br>" +
                "Category: <b>%{customdata[1]}</b><extra></extra>"
        ))

    # ---------------- X-axis labels for month names ----------------
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
        yaxis_title="AQI Level",
        legend_title="Lines",
        height=500,
        margin=dict(t=60),
        plot_bgcolor="#FFFFFF"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

