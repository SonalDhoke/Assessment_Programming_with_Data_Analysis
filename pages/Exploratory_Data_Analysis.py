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
    # MONTHLY TREND
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
    # DONUT CHART
    # ==========================================================
    st.markdown("### 🫧 Pollutant Composition")

    poll_mean = df[pollutants].mean().sort_values(ascending=False)
    fig_donut = px.pie(names=poll_mean.index, values=poll_mean.values, hole=0.5,
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_donut.update_layout(height=260, showlegend=False)
    st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

    # ==========================================================
    # CITY BAR
    # ==========================================================
    st.markdown(f"### 🏙 Top Cities with High AQI (>{HIGH_AQI_THRESHOLD})")

    if not city_incidents.empty:
        city_plot = city_incidents.reset_index().rename(columns={"AQI_recalc": "High AQI Incidents"})
        fig_city = px.bar(city_plot.head(10), x="City", y="High AQI Incidents", text="High AQI Incidents")
        fig_city.update_traces(textposition='outside')
        fig_city.update_layout(height=300, xaxis_tickangle=45)
        st.plotly_chart(fig_city, use_container_width=True)

    st.markdown("---")
    st.markdown("## 📂 Choose an Analysis Module")

    # ==========================================================
    # 3×2 PASTEL GRID STYLING
    # ==========================================================
    st.markdown("""
    <style>
    .module-card {
        background: linear-gradient(135deg, #EEF4FF, #F8FBFF);
        border: 1px solid #C9DAFF;
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        font-size: 16px;
        font-weight: 600;
        color: #344767;
        cursor: pointer;
        transition: all 0.25s ease-in-out;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }

    .module-card:hover {
        transform: translateY(-3px);
        background: linear-gradient(135deg, #DDE9FF, #EEF4FF);
        border-color: #7CA4FF;
        box-shadow: 0px 8px 20px rgba(124,164,255,0.25);
    }

    .selected-card {
        background: linear-gradient(135deg, #C7DBFF, #E6F0FF);
        border: 2px solid #5C8DFF;
        box-shadow: 0px 10px 28px rgba(92,141,255,0.35);
    }
    </style>
    """, unsafe_allow_html=True)

    if "eda_mode" not in st.session_state:
        st.session_state.eda_mode = "Distribution Analysis"

    modules = [
        ("📈 Distribution Analysis", "Distribution Analysis"),
        ("🕒 Time-Series Analysis", "Time-Series Analysis"),
        ("🔗 Correlation Matrix", "Correlation Matrix"),
        ("🟢 AQI Category Analysis", "AQI Category Analysis"),
        ("🍂 Seasonal Patterns", "Seasonal Patterns"),
        ("🔍 Comparison Tool", "Comparison Tool"),
    ]

    row1 = st.columns(3)
    row2 = st.columns(3)

    for i, (label, value) in enumerate(modules):
        col = row1[i] if i < 3 else row2[i - 3]
        is_selected = st.session_state.eda_mode == value
        card_class = "module-card selected-card" if is_selected else "module-card"

        with col:
            st.markdown(f"<div class='{card_class}'>{label}</div>", unsafe_allow_html=True)
            if st.button(label, key=value):
                st.session_state.eda_mode = value

    st.markdown(f"### ✅ Selected Module: `{st.session_state.eda_mode}`")
    st.markdown("---")

    # ==========================================================
    # LOAD MODULE
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
