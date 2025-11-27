import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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
    margin-bottom: 22px;
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

    # ------------------- Load Data -----------------------
    df = None
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
    elif "current_df" in st.session_state:
        df = st.session_state.current_df
    else:
        df = st.session_state.original_df

    if df is None:
        st.error("Dataset not available.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.header("📈 Distribution Analysis")

    # ------------------- Detect Pollutants --------------
    exclude = {
        "City", "AQI", "AQI_Bucket", "AQI_Recalc",
        "AQI_Bucket_Recalc", "Year", "Month_Name", "Week"
    }

    pollutant_cols = [
        c for c in df.columns
        if c not in exclude and pd.api.types.is_numeric_dtype(df[c])
    ]

    # ------------------- Filter Panel ---------------------
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
        time_group = st.selectbox(
            "Group Data By",
            ["None", "Yearly", "Monthly", "Weekly"],
            index=0
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------- Apply City Filter -------------------
    filtered_df = df.copy()
    if cities:
        filtered_df = filtered_df[filtered_df["City"].isin(cities)]

    # --------------------- Time Grouping Logic -------------------
    if time_group == "Yearly":
        filtered_df["Year"] = filtered_df["Date"].dt.year.astype(str)
        grouped_df = (
            filtered_df.groupby(["Year"] + (["City"] if cities else []))[pollutant]
            .mean().reset_index()
        )
        x_col = "Year"

    elif time_group == "Monthly":
        filtered_df["Month"] = filtered_df["Date"].dt.month
        filtered_df["Month_Name"] = filtered_df["Date"].dt.strftime("%B")

        month_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        grouped_df = (
            filtered_df.groupby(["Month_Name"] + (["City"] if cities else []))[pollutant]
            .mean().reset_index()
        )
        grouped_df["Month_Name"] = pd.Categorical(
            grouped_df["Month_Name"], categories=month_order, ordered=True
        )
        grouped_df = grouped_df.sort_values("Month_Name")
        x_col = "Month_Name"

    elif time_group == "Weekly":
        filtered_df["Week"] = filtered_df["Date"].dt.isocalendar().week.astype(int)
        grouped_df = (
            filtered_df.groupby(["Week"] + (["City"] if cities else []))[pollutant]
            .mean().reset_index()
        )
        x_col = "Week"

    else:
        grouped_df = filtered_df.copy()
        x_col = pollutant

    if grouped_df.empty:
        st.warning("No data available for selected filters.")
        return

    # --------------------- Visualization Section -------------------
    st.markdown("### 📊 Distribution Visualizations")

    st.markdown('<div class="plot-container">', unsafe_allow_html=True)

    # ----------------------------------------------------
    # MAIN CHART — Histogram or Bar (Stacked for multi-city)
    # ----------------------------------------------------

    # --- MULTIPLE CITIES → STACKED BAR ---
    if time_group != "None" and len(cities) > 1:
        fig = px.bar(
            grouped_df,
            x=x_col,
            y=pollutant,
            color="City",
            barmode="stack",
            color_discrete_sequence=px.colors.qualitative.Pastel2,
            title=f"{pollutant} - {time_group} (Stacked by City)"
        )

    # --- SINGLE CITY or NO CITY with GROUPING → Simple Bar ---
    elif time_group != "None":
        fig = px.bar(
            grouped_df,
            x=x_col,
            y=pollutant,
            color_discrete_sequence=px.colors.qualitative.Pastel1,
            title=f"{pollutant} - {time_group} Average"
        )

    # --- NO GROUPING → HISTOGRAM ---
    else:
        fig = px.histogram(
            grouped_df,
            x=x_col,
            nbins=40,
            opacity=0.8,
            color_discrete_sequence=px.colors.qualitative.Pastel2,
            title=f"Distribution of {pollutant}"
        )

    # Pretty layout
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title="Value",
        title_font_size=20
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------
    # SUMMARY STATISTICS
    # ----------------------------------------------------
    st.markdown("### 📌 Summary Statistics")
    stats_df = grouped_df.describe().T
    st.dataframe(stats_df, use_container_width=True)
