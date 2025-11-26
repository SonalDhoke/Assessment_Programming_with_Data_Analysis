import streamlit as st
import pandas as pd

def show():

    # ---------------------------
    # Pastel Styling
    # ---------------------------
    st.markdown("""
        <style>

            .section-header {
                font-size: 28px !important;
                font-weight: 700 !important;
                color: #344767 !important;
                margin-top: 30px !important;
                margin-bottom: 10px !important;
            }

            .sub-header {
                font-size: 22px !important;
                font-weight: 600 !important;
                color: #4A6480 !important;
                margin-top: 25px !important;
                margin-bottom: 8px !important;
            }

            .pastel-box {
                background-color: #F7F9FC;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #E3EAF4;
                margin-bottom: 20px;
            }

            .aqi-table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 15px;
                background-color: white;
                border-radius: 8px;
                overflow: hidden;
            }

            .aqi-table th {
                background-color: #E4ECFA;
                padding: 10px;
                font-weight: 700;
                color: #3A4A66;
                border: 1px solid #D6D9DF;
                text-align: center;
            }

            .aqi-table td {
                padding: 10px;
                border: 1px solid #D6D9DF;
                text-align: center;
                font-size: 15px;
            }

        </style>
    """, unsafe_allow_html=True)

    # ---------------------------
    # MAIN TITLE
    # ---------------------------
    st.markdown("<div class='section-header'>📌 Air Quality Index (AQI) – Overview</div>", unsafe_allow_html=True)

    # ---------------------------
    # WHAT IS AQI
    # ---------------------------
    st.markdown("<div class='sub-header'>🌫️ What is AQI?</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="pastel-box">
            The **Air Quality Index (AQI)** is a simplified, colour-coded number that represents 
            how clean or polluted the air currently is.  
            AQI ranges from <b>0 to 500</b> and helps people quickly understand:
            <ul>
                <li>🔹 How healthy or unhealthy the air is</li>
                <li>🔹 What health impacts may occur</li>
                <li>🔹 Whether sensitive groups should limit outdoor activities</li>
                <li>🔹 When pollution-control actions must be taken</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # ---------------------------
    # POLLUTANT TABLE
    # ---------------------------
    st.markdown("<div class='sub-header'>🌬️ Pollutants in This Dataset</div>", unsafe_allow_html=True)

    pollutant_data = {
        "Pollutant": [
            "PM2.5", "PM10", "NO", "NO₂", "NOx", 
            "NH₃", "CO", "SO₂", "O₃", "Benzene", "Toluene", "Xylene"
        ],
        "Full Name": [
            "Fine Particulate Matter",
            "Coarse Particulate Matter",
            "Nitric Oxide",
            "Nitrogen Dioxide",
            "Nitrogen Oxides",
            "Ammonia",
            "Carbon Monoxide",
            "Sulphur Dioxide",
            "Ground-Level Ozone",
            "Benzene",
            "Toluene",
            "Xylene"
        ],
        "Description": [
            "Penetrates deep into lungs; causes cardiovascular & respiratory issues.",
            "Irritates respiratory tract; causes coughing & throat discomfort.",
            "Emitted from vehicles/combustion; precursor to NO₂ & ozone.",
            "Toxic gas that reduces lung function & forms smog.",
            "Combination of NO & NO₂; drives ozone formation.",
            "Released from fertilizers & waste; irritates eyes and lungs.",
            "Toxic gas reducing oxygen supply; dangerous at high levels.",
            "From burning fuels; causes asthma & airway inflammation.",
            "Formed in sunlight from NOx + VOCs; damages lung tissue.",
            "Carcinogenic VOC from fuel/solvents; harmful to nervous system.",
            "VOC from fuels/industry; causes headaches & irritation.",
            "VOC solvent; affects breathing & neurological functions."
        ]
    }

    df_pollutants = pd.DataFrame(pollutant_data)
    st.dataframe(df_pollutants, use_container_width=True)

    # ---------------------------
    # AQI CALCULATION
    # ---------------------------
    st.markdown("<div class='sub-header'>🧮 How AQI is Calculated</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="pastel-box">
            AQI is calculated in the following steps:
            <ul>
                <li>📍 24-hour or 8-hour average concentration values are taken for pollutants</li>
                <li>📍 Each pollutant is converted into a <b>Sub-Index</b> using CPCB breakpoint tables</li>
                <li>📍 Sub-index is obtained using <b>linear interpolation</b></li>
                <li>📍 The final AQI = <b>maximum</b> of all pollutant sub-indices</li>
                <li>📍 The pollutant with the highest sub-index = <b>Dominant Pollutant</b></li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # ---------------------------
    # AQI BUCKET TABLE
    # ---------------------------
    st.markdown("<div class='sub-header'>📊 AQI Categories (CPCB)</div>", unsafe_allow_html=True)

    st.markdown("""
    <table class="aqi-table">
        <tr>
            <th>AQI Range</th>
            <th>Category</th>
            <th>Colour</th>
            <th>Health Impact</th>
        </tr>
        <tr>
            <td>0–50</td>
            <td>Good</td>
            <td style="background:#55A84F;"></td>
            <td>Minimal impact</td>
        </tr>
        <tr>
            <td>51–100</td>
            <td>Satisfactory</td>
            <td style="background:#A3C853;"></td>
            <td>Minor discomfort to sensitive individuals</td>
        </tr>
        <tr>
            <td>101–200</td>
            <td>Moderate</td>
            <td style="background:#F3EC19;"></td>
            <td>Breathing discomfort to sensitive groups</td>
        </tr>
        <tr>
            <td>201–300</td>
            <td>Poor</td>
            <td style="background:#EC8E19;"></td>
            <td>Discomfort on prolonged exposure</td>
        </tr>
        <tr>
            <td>301–400</td>
            <td>Very Poor</td>
            <td style="background:#D6001C;"></td>
            <td>Respiratory illness on prolonged exposure</td>
        </tr>
        <tr>
            <td>401–500</td>
            <td>Severe</td>
            <td style="background:#7E0023;"></td>
            <td>Serious impact even on healthy individuals</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    # ---------------------------
    # SIGNIFICANCE
    # ---------------------------
    st.markdown("<div class='sub-header'>❤️ Why AQI Matters</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="pastel-box">
            <ul>
                <li>🔸 Helps people understand the air they breathe</li>
                <li>🔸 Guides health advisories for children, elderly, asthma patients</li>
                <li>🔸 Supports policy actions like GRAP, traffic control, and emission reduction</li>
                <li>🔸 Tracks pollution trends for research and planning</li>
                <li>🔸 Provides environmental visibility for decision-making</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
