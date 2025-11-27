import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="CPCB AQI Calculator", layout="centered")

st.title("🇮🇳 CPCB AQI Calculator")
st.write("Enter pollutant concentrations to compute India AQI (CPCB).")

# ---------------------------
# CPCB BREAKPOINTS
# ---------------------------
breakpoints = {
    "PM2.5": [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, 500, 401, 500),
    ],
    "PM10": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 250, 101, 200),
        (251, 350, 201, 300),
        (351, 430, 301, 400),
        (431, 600, 401, 500),
    ],
    "NO2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 180, 101, 200),
        (181, 280, 201, 300),
        (281, 400, 301, 400),
        (401, 1000, 401, 500),
    ],
    "SO2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 380, 101, 200),
        (381, 800, 201, 300),
        (801, 1600, 301, 400),
        (1601, 2000, 401, 500),
    ],
    "CO": [
        (0, 1, 0, 50),
        (1.1, 2, 51, 100),
        (2.1, 10, 101, 200),
        (10.1, 17, 201, 300),
        (17.1, 34, 301, 400),
        (34.1, 50, 401, 500),
    ],
    "O3": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 168, 101, 200),
        (169, 208, 201, 300),
        (209, 748, 301, 400),
        (749, 1000, 401, 500),
    ]
}

# ---------------------------
# AQI CATEGORY
# ---------------------------
def get_aqi_category(aqi):
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Satisfactory"
    if aqi <= 200: return "Moderate"
    if aqi <= 300: return "Poor"
    if aqi <= 400: return "Very Poor"
    return "Severe"

# ---------------------------
# AQI CALC LOGIC
# ---------------------------
def calculate_sub_index(pollutant, concentration):
    for bp_low, bp_high, si_low, si_high in breakpoints[pollutant]:
        if bp_low <= concentration <= bp_high:
            si = ((si_high - si_low) / (bp_high - bp_low)) * (concentration - bp_low) + si_low
            return round(si)
    return None

# ---------------------------
# INPUT UI
# ---------------------------
st.subheader("Enter Concentrations")

pollutants = {}
for p in breakpoints.keys():
    pollutants[p] = st.number_input(f"{p} (µg/m³)", min_value=0.0, step=0.1)

if st.button("Calculate AQI"):
    results = {}
    for p, val in pollutants.items():
        if val > 0:
            results[p] = calculate_sub_index(p, val)

    if len(results) == 0:
        st.warning("Please enter at least one pollutant value.")
    else:
        df = pd.DataFrame({
            "Pollutant": list(results.keys()),
            "Sub-Index": list(results.values())
        })

        st.subheader("Sub-Index Results")
        st.dataframe(df)

        overall_aqi = max(results.values())
        category = get_aqi_category(overall_aqi)

        st.subheader("Overall AQI")
        st.metric("AQI Value", overall_aqi, help="Highest sub-index is considered overall AQI")
        st.success(f"Air Quality Category: **{category}**")

        st.write("---")
        st.write("CPCB National AQI Method used. Breakpoints aligned with official guidelines.")
