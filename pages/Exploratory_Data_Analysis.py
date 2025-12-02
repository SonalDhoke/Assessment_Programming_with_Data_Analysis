import streamlit as st
import plotly.express as px
import pandas as pd


def show():
    st.title("📊 Exploratory Data Analysis")

    # ==========================================================
    # LOAD DATASET FROM SESSION STATE
    # ==========================================================
    df = None
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
    elif "current_df" in st.session_state:
        df = st.session_state.current_df
    elif "original_df" in st.session_state:
        df = st.session_state.original_df

    if df is None:
        st.error("❌ No dataset found. Please upload a dataset or run Data Cleaning.")
        return

    # ==========================================================
    # ENSURE REQUIRED COLUMNS EXIST
    # ==========================================================
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    if "AQI_recalc" not in df.columns:
        st.warning("⚠ 'AQI_recalc' missing — using 'AQI' instead. Run Data Cleaning for recalculation.")
        df["AQI_recalc"] = df["AQI"]

    # Create Month Number & Month Name
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%B")

    pollutants = ['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene']


    # ==========================================================
    # SECTION 1 — DASHBOARD OVERVIEW (KPI CARDS)
    # ==========================================================
    st.markdown("## 🧭 Dashboard Overview")

    # KPI 1 — Average AQI
    avg_aqi = df["AQI_recalc"].mean()

    # KPI 2 — Severe AQI days
    severe_days = df[df["AQI_recalc"] > 400].shape[0]

    # KPI 3 & 4 — Most and Cleanest City (based on high AQI incidents)
    HIGH_AQI_THRESHOLD = 200
    high_df = df[df["AQI_recalc"] > HIGH_AQI_THRESHOLD]
    city_incidents = high_df.groupby("City")["AQI_recalc"].count().sort_values(ascending=False)

    if not city_incidents.empty:
        most_polluted_city = f"{city_incidents.idxmax()} ({city_incidents.max()} incidents)"
        cleanest_city = f"{city_incidents.idxmin()} ({city_incidents.min()} incidents)"
    else:
        most_polluted_city = "No high-AQI records"
        cleanest_city = "No high-AQI records"

    # KPI 5 — Top Pollutant
    top_pollutant = df[pollutants].mean().idxmax()

    # ----- Display KPI Cards -----
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("🌫 Avg AQI", f"{avg_aqi:.1f}")
    k2.metric("🔥 Severe Days", severe_days)
    k3.metric("🏙 Most Polluted", most_polluted_city)
    k4.metric("🌿 Cleanest City", cleanest_city)
    k5.metric("🔝 Top Pollutant", top_pollutant)

    st.markdown("---")


    # ==========================================================
    # MONTHLY AQI TREND — WITH MONTH NAMES
    # ==========================================================
    st.markdown("### 📉 Monthly AQI Trend")

    # Order month names correctly
    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]

    df_month = df.groupby("Month_Name")["AQI_recalc"].mean().reindex(month_order).reset_index()

    fig_trend = px.line(
        df_month, 
        x="Month_Name", 
        y="AQI_recalc", 
        markers=True,
        title=""
    )
    fig_trend.update_layout(height=260, xaxis_title="Month", yaxis_title="AQI")
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")


    # ==========================================================
    # MINI DONUT — POLLUTANT COMPOSITION
    # ==========================================================
    st.markdown("### 🫧 Pollutant Composition (Mean Levels)")

    poll_mean = df[pollutants].mean().sort_values(ascending=False)
    fig_donut = px.pie(
        names=poll_mean.index,
        values=poll_mean.values,
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_donut.update_layout(height=260, showlegend=False)
    st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")


    # ==========================================================
    # UPDATED BAR CHART — HIGH AQI INCIDENTS
    # ==========================================================
    st.markdown(f"### 🏙 Top 10 Cities with High AQI Incidents (AQI > {HIGH_AQI_THRESHOLD})")

    if not city_incidents.empty:
        city_plot = city_incidents.reset_index().rename(columns={"AQI_recalc": "High AQI Incidents"})

        fig_city = px.bar(
            city_plot.head(10),
            x="City",
            y="High AQI Incidents",
            text="High AQI Incidents"
        )
        fig_city.update_traces(textposition='outside')
        fig_city.update_layout(height=300, xaxis_tickangle=45)
        st.plotly_chart(fig_city, use_container_width=True)
    else:
        st.info("No high AQI data available.")

    st.markdown("---")
    st.markdown("### 📂 Choose an analysis module for deeper insights:")


    # ==========================================================
    # BUTTON STYLING
    # ==========================================================
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
            font-size: 15px;
            font-weight: 500;
        }
        div.stButton > button:hover {
            background-color: #D5E4FF;
            border-color: #7CA4FF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    # ==========================================================
    # MODULE BUTTONS
    # ==========================================================
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


    # ==========================================================
    # LOAD SELECTED MODULE
    # ==========================================================
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
