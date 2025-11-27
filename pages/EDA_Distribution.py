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
    exclude = {"City", "AQI", "AQI_Bucket", "AQI_Recalc", "AQI_Bucket_Recalc"}
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

    outliers = st.checkbox("Highlight Outliers", value=False)

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------- Apply City Filter -------------------
    filtered_df = df.copy()
    if cities:
        filtered_df = filtered_df[filtered_df["City"].isin(cities)]

    # --------------------- Apply Time Group Filter -------------
    if time_group == "Yearly":
        filtered_df["Year"] = filtered_df["Date"].dt.year
        filtered_df = filtered_df.groupby("Year")[pollutant].mean().reset_index()
        x_col = "Year"

    elif time_group == "Monthly":
        filtered_df["Month"] = filtered_df["Date"].dt.to_period("M").astype(str)
        filtered_df = filtered_df.groupby("Month")[pollutant].mean().reset_index()
        x_col = "Month"

    elif time_group == "Weekly":
        filtered_df["Week"] = filtered_df["Date"].dt.isocalendar().week
        filtered_df = filtered_df.groupby("Week")[pollutant].mean().reset_index()
        x_col = "Week"

    else:  # No grouping
        x_col = pollutant

    if filtered_df.empty:
        st.warning("No data available for selected filters.")
        return

    # --------------------- Visualization Section -------------------
    st.markdown("### 📊 Distribution Visualizations")

    col_hist, col_box = st.columns([2, 1])

    # ------------ Histogram + KDE ------------
    with col_hist:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        if time_group == "None":
            # Normal pollutant distribution
            fig = px.histogram(
                filtered_df,
                x=pollutant,
                nbins=40,
                opacity=0.75,
                color_discrete_sequence=["#A7C4FF"],
                marginal="rug"
            )
            fig.update_layout(
                title=f"Distribution of {pollutant}",
                xaxis_title=pollutant,
                yaxis_title="Frequency"
            )
        else:
            # Distribution of grouped averages
            fig = px.bar(
                filtered_df,
                x=x_col,
                y=pollutant,
                color_discrete_sequence=["#A7C4FF"],
                title=f"{pollutant} - {time_group} Average"
            )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------ Box Plot ------------
    with col_box:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        if time_group == "None":
            fig2 = px.box(
                filtered_df,
                y=pollutant,
                points="all" if outliers else False,
                color_discrete_sequence=["#FFB3C6"]
            )
            fig2.update_layout(title=f"Boxplot of {pollutant}")
        else:
            fig2 = px.box(
                filtered_df,
                y=pollutant,
                color_discrete_sequence=["#FFB3C6"],
                title=f"{pollutant} Distribution ({time_group})"
            )

        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Summary Statistics ------------------
    st.markdown("### 📌 Summary Statistics")
    stats_df = filtered_df.describe().T
    st.dataframe(stats_df, use_container_width=True)
