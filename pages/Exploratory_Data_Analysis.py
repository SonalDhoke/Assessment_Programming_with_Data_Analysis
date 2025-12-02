import streamlit as st
import plotly.express as px
import pandas as pd

def show():
    st.title("📊 Exploratory Data Analysis")

    # -----------------------------------------
    # Load dataset from session_state
    # -----------------------------------------
    df = None
    
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
    elif "current_df" in st.session_state:
        df = st.session_state.current_df
    elif "original_df" in st.session_state:
        df = st.session_state.original_df
    
    if df is None:
        st.error("No dataset found. Please load data from the Dataset Information page.")
        return

    pollutants = ['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene']

    # ----------------------------------------------------------
    #  SECTION 1 — DASHBOARD OVERVIEW (Always at top)
    # ----------------------------------------------------------
    st.markdown("## 🧭 Dashboard Overview")
    st.write("Quick insights into air quality patterns across India.")

    # ----- KPI CALCULATIONS -----
    avg_aqi = df["AQI_recalc"].mean()
    severe_days = df[df["AQI_recalc"] > 400].shape[0]

    city_rank = df.groupby("City")["AQI_recalc"].mean().sort_values()
    cleanest_city = city_rank.index[0]
    most_polluted_city = city_rank.index[-1]

    top_pollutant = df[pollutants].mean().idxmax()

    # ----- KPI CARDS -----
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("🌫 Avg AQI", f"{avg_aqi:.1f}")
    k2.metric("🔥 Severe Days", severe_days)
    k3.metric("🏙 Most Polluted", most_polluted_city)
    k4.metric("🌿 Cleanest", cleanest_city)
    k5.metric("🔝 Top Pollutant", top_pollutant)

    st.markdown("---")

    # ----- Mini AQI Trend Chart -----
    df_month = df.groupby("Month")["AQI_recalc"].mean().reset_index()
    fig_trend = px.line(df_month, x="Month", y="AQI_recalc", markers=True, title="📉 Monthly AQI Trend")
    fig_trend.update_layout(height=260, margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # ----- Mini Donut Chart for Pollutants -----
    poll_mean = df[pollutants].mean().sort_values(ascending=False)
    fig_donut = px.pie(
        names=poll_mean.index, values=poll_mean.values, 
        hole=0.5, 
        title="🫧 Pollutant Composition",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_donut.update_layout(height=260, showlegend=False)
    st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

    # ----- Mini Bar Chart: Top 10 Polluted Cities -----
    city_rank_plot = city_rank.sort_values(ascending=False).reset_index().head(10)
    fig_city = px.bar(city_rank_plot, x="City", y="AQI_recalc", title="🏙 Top Polluted Cities")
    fig_city.update_layout(height=300, xaxis_tickangle=45)
    st.plotly_chart(fig_city, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📂 Choose an analysis module to explore deeper insights:")

    # ----------------------------------------------------------
    # BUTTON STYLING
    # ----------------------------------------------------------
    st.markdown(
        """
        <style>
        div.stButton > button {
            width: 100%;
            border-radius: 12px;
            border: 1px solid #A7C4FF;
            background-color: #E9F2FF;
            color: #344767;
            padding: 0.6rem 1rem;
            font-size: 16px;
            font-weight: 500;
        }
        div.stButton > button:hover {
            background-color: #D5E4FF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ----------------------------------------------------------
    # SECTION 2 — MODULE SELECTION BUTTONS
    # ----------------------------------------------------------
    if "eda_mode" not in st.session_state:
        st.session_state.eda_mode = "Distribution Analysis"

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📈 Distribution Analysis"):
            st.session_state.eda_mode = "Distribution Analysis"

        if st.button("🔗 Correlation Matrix"):
            st.session_state.eda_mode = "Correlation Matrix"

        if st.button("🍂 Seasonal Patterns"):
            st.session_state.eda_mode = "Seasonal Patterns"

    with col2:
        if st.button("🕒 Time-Series Analysis"):
            st.session_state.eda_mode = "Time-Series Analysis"

        if st.button("🟢 AQI Category Analysis"):
            st.session_state.eda_mode = "AQI Category Analysis"

        if st.button("🔍 Comparison Tool"):
            st.session_state.eda_mode = "Comparison Tool"

    st.markdown(f"**Selected module:** `{st.session_state.eda_mode}`")
    st.markdown("---")

    # ----------------------------------------------------------
    # SECTION 3 — ROUTE TO SELECTED ANALYSIS MODULE
    # ----------------------------------------------------------
    mode = st.session_state.eda_mode

    if mode == "Distribution Analysis":
        import pages.EDA_Distribution as pg
        pg.show()

    elif mode == "Time-Series Analysis":
        import pages.EDA_Timeseries as pg
        pg.show()

    elif mode == "Correlation Matrix":
        import pages.EDA_Correlation as pg
        pg.show()

    elif mode == "AQI Category Analysis":
        import pages.EDA_AQI_Category as pg
        pg.show()

    elif mode == "Seasonal Patterns":
        import pages.EDA_Seasonal as pg
        pg.show()

    elif mode == "Comparison Tool":
        import pages.EDA_Comparison as pg
        pg.show()
