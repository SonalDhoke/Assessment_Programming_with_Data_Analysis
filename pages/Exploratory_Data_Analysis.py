import streamlit as st
import plotly.express as px
import pandas as pd


def show():

    # ==========================================================
    # HEADER
    # ==========================================================
    st.markdown("<h2 style='font-size:32px;'>📊 Exploratory Data Analysis</h2>", unsafe_allow_html=True)

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
        st.warning("⚠ 'AQI_recalc' missing — using 'AQI' instead.")
        df["AQI_recalc"] = df["AQI"]

    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%B")

    pollutants = ['PM2.5','PM10','NO','NO2','NOx','NH3','CO','SO2','O3','Benzene','Toluene']

    # ==========================================================
    # KPI SECTION
    # ==========================================================
    st.markdown("## 🧭 Dashboard Overview")

    avg_aqi = df["AQI_recalc"].mean()
    severe_days = df[df["AQI_recalc"] > 400].shape[0]

    HIGH_AQI_THRESHOLD = 200
    high_df = df[df["AQI_recalc"] > HIGH_AQI_THRESHOLD]
    city_incidents = high_df.groupby("City")["AQI_recalc"].count().sort_values(ascending=False)

    most_polluted_city = f"{city_incidents.idxmax()} ({city_incidents.max()} incidents)" if not city_incidents.empty else "N/A"
    cleanest_city = f"{city_incidents.idxmin()} ({city_incidents.min()} incidents)" if not city_incidents.empty else "N/A"
    top_pollutant = df[pollutants].mean().idxmax()

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("🌫 Avg AQI", f"{avg_aqi:.1f}")
    k2.metric("🔥 Severe Days", severe_days)
    k3.metric("🏙 Most Polluted", most_polluted_city)
    k4.metric("🌿 Cleanest City", cleanest_city)
    k5.metric("🔝 Top Pollutant", top_pollutant)

    st.markdown("---")

    # ==========================================================
    # MONTHLY AQI TREND
    # ==========================================================
    st.markdown("### 📉 Monthly AQI Trend")

    month_order = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]

    df_month = df.groupby("Month_Name")["AQI_recalc"].mean().reindex(month_order).reset_index()

    fig_trend = px.line(df_month, x="Month_Name", y="AQI_recalc", markers=True)
    fig_trend.update_layout(height=260)
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")

    # ==========================================================
    # DONUT CHART — BIG + LABEL WITH %
    # ==========================================================
    st.markdown("### 🫧 Pollutant Composition")

    poll_mean = df[pollutants].mean().sort_values(ascending=False)

    fig_donut = px.pie(
        names=poll_mean.index,
        values=poll_mean.values,
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig_donut.update_traces(
        textinfo="label+percent",
        textposition="outside",
        pull=[0.05] * len(poll_mean)
    )

    fig_donut.update_layout(
        height=420,
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        uniformtext_minsize=12,
        uniformtext_mode="hide"
    )

    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("---")

    # ==========================================================
    # CITY BAR PLOT — BEAUTIFUL COLOR + DELHI VISIBLE
    # ==========================================================
    st.markdown(f"### 🏙 Top Cities with High AQI (>{HIGH_AQI_THRESHOLD})")

    if not city_incidents.empty:
        city_plot = city_incidents.reset_index().rename(
            columns={"AQI_recalc": "High AQI Incidents"}
        )

        fig_city = px.bar(
            city_plot.head(10),
            x="City",
            y="High AQI Incidents",
            text="High AQI Incidents",
            color="High AQI Incidents",
            color_continuous_scale="Tealgrn"
        )

        fig_city.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        fig_city.update_layout(
            height=420,
            xaxis_tickangle=-30,
            margin=dict(t=40, b=80, l=60, r=40),
            xaxis_title="City",
            yaxis_title="High AQI Incidents"
        )

        st.plotly_chart(fig_city, use_container_width=True)
    else:
        st.info("No high AQI data available.")

    st.markdown("---")
