
import streamlit as st

def show():

    # ---------------------------
    # Pastel Theme Styling
    # ---------------------------
    st.markdown("""
        <style>
            .pastel-box {
                background-color: #F7F9FC;
                padding: 18px;
                border-radius: 12px;
                border: 1px solid #E3EAF4;
                margin-bottom: 18px;
            }

            h2, h3 {
                color: #3A4A66;
            }

            .aqi-table td, .aqi-table th {
                padding: 8px 14px;
                border: 1px solid #D6D6D6;
            }
            .aqi-table {
                border-collapse: collapse;
                width: 100%;
                font-size: 16px;
                margin-top: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # ---------------------------
    # Title
    # ---------------------------
    st.title("🏠 Overview: Air Quality Index (AQI) in India")

    # ---------------------------
    # Section 1 – What is AQI?
    # ---------------------------
    st.header("1) 🌫️ What is the Air Quality Index (AQI)?")

    st.markdown("""
    <div class="pastel-box">
        The **Air Quality Index (AQI)** is a numeric and colour-coded scale that simplifies complex 
        air-pollution data into a single, easy-to-understand value ranging from **0 to 500**.  
        It helps people quickly understand **how clean or polluted the air is**, and what health 
        effects might be associated with that level of pollution.
        <br><br>
        India's AQI system is defined by the **Central Pollution Control Board (CPCB)** and used by 
        monitoring networks across IMD, IITM, SPCBs, and SAFAR.
        <br><br>
        In simple terms:
        <b>Lower AQI = Cleaner Air</b><br>
        <b>Higher AQI = More Health Risk</b>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------
    # Section 2 – Pollutants
    # ---------------------------
      # ---------------------------
    # Section 2 – Pollutants in Your Dataset
    # ---------------------------
    st.header("2) 🌬️ Pollutants in This Dataset")

    st.markdown("""
    <div class="pastel-box">
        The dataset contains **12 key atmospheric pollutants and gases** that contribute to air quality
        and human health impacts.  
        Below is a simple description of each pollutant:
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 🔹 PM2.5 — Fine Particulate Matter  
    Tiny inhalable particles (<2.5 µm) that penetrate deep into the lungs and bloodstream.

    ### 🔹 PM10 — Coarse Particulate Matter  
    Larger particles (<10 µm) that irritate the respiratory system and cause coughing/throat irritation.

    ### 🔹 NO — Nitric Oxide  
    A reactive gas mainly emitted from vehicles and high-temperature combustion; precursor to NO₂ and ozone.

    ### 🔹 NO₂ — Nitrogen Dioxide  
    A red-brown gas that irritates airways, reduces lung function, and is a major smog component.

    ### 🔹 NOx — Nitrogen Oxides (NO + NO₂)  
    A family of reactive gases formed during combustion; drives ozone formation and respiratory irritation.

    ### 🔹 NH₃ — Ammonia  
    A pungent gas released from fertilizers, livestock, and waste; causes eye, throat, and lung irritation.

    ### 🔹 CO — Carbon Monoxide  
    A colorless toxic gas from incomplete combustion; reduces oxygen delivery in the body.

    ### 🔹 SO₂ — Sulphur Dioxide  
    A sharp-smelling gas from burning coal and industrial processes; triggers asthma and respiratory distress.

    ### 🔹 O₃ — Ground Level Ozone  
    A harmful gas formed from NOx + VOCs under sunlight; irritates lungs and worsens asthma.

    ### 🔹 Benzene  
    A carcinogenic volatile organic compound (VOC) from fuel evaporation, solvents, and traffic emissions.

    ### 🔹 Toluene  
    A solvent and VOC from fuel and industrial processes; affects the nervous system and causes headaches.

    ### 🔹 Xylene  
    A VOC used in solvents and fuel emissions; causes respiratory irritation and neurological effects.
    """, unsafe_allow_html=True)

    # ---------------------------
    # Section 3 – AQI Calculation
    # ---------------------------
    st.header("3) 🧮 How AQI is Calculated (CPCB Method)")

    st.markdown("""
    <div class="pastel-box">
        The AQI is calculated using the following steps:
        <br><br>
        ➤ Step 1 — Measure pollutant concentrations for 24-hour (or 8-hour for CO & O₃).  
        <br>
        ➤ Step 2 — Convert each pollutant concentration into a **sub-index** using CPCB breakpoint tables.  
        These tables map pollutant concentration ranges to AQI ranges.  
        <br>
        ➤ Step 3 — Sub-index is computed using **linear interpolation**:  
        <i>I = (I_hi - I_lo) / (BP_hi - BP_lo) × (C - BP_lo) + I_lo</i>  
        <br>
        ➤ Step 4 — The final AQI is the **maximum** of all sub-indices (dominant pollutant).  
        <br><br>
        ✔ At least 3 pollutants must be available  
        ✔ PM₂.₅ or PM₁₀ must be one of them  
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------
    # Section 4 – AQI Buckets
    # ---------------------------
    st.header("4) 📊 AQI Categories / Buckets (CPCB Standard)")

    st.markdown("""
    Below are the six official AQI buckets defined by CPCB:
    """)

    st.markdown("""
    <table class="aqi-table">
        <tr>
            <th>AQI Range</th>
            <th>Category</th>
            <th>Colour Code</th>
            <th>Health Impact</th>
        </tr>
        <tr>
            <td>0 – 50</td>
            <td>Good</td>
            <td style="background:#55A84F;"></td>
            <td>Minimal impact</td>
        </tr>
        <tr>
            <td>51 – 100</td>
            <td>Satisfactory</td>
            <td style="background:#A3C853;"></td>
            <td>Minor discomfort to sensitive individuals</td>
        </tr>
        <tr>
            <td>101 – 200</td>
            <td>Moderate</td>
            <td style="background:#F3EC19;"></td>
            <td>Breathing discomfort to sensitive groups</td>
        </tr>
        <tr>
            <td>201 – 300</td>
            <td>Poor</td>
            <td style="background:#EC8E19;"></td>
            <td>Discomfort on prolonged exposure</td>
        </tr>
        <tr>
            <td>301 – 400</td>
            <td>Very Poor</td>
            <td style="background:#D6001C;"></td>
            <td>Respiratory illness on prolonged exposure</td>
        </tr>
        <tr>
            <td>401 – 500</td>
            <td>Severe</td>
            <td style="background:#7E0023;"></td>
            <td>Serious impact even on healthy individuals</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    # ---------------------------
    # Section 5 – Significance
    # ---------------------------
    st.header("5) ❤️ Why AQI Matters (Health & Environmental Significance)")

    st.markdown("""
    <div class="pastel-box">
        The AQI is essential for:
        <br><br>
        ✔ **Public Awareness** — Helps people assess health risks instantly.  
        ✔ **Sensitive Groups** — Guides children, elderly, and people with respiratory issues.  
        ✔ **Policy Action** — Triggers measures under GRAP, traffic restrictions, industrial controls.  
        ✔ **Urban Planning** — Shapes emission-control strategies.  
        ✔ **Environmental Protection** — Reflects how pollution affects vegetation and climate.  
        <br><br>
        In short, AQI is not just a number — it is a **life-impacting indicator** affecting 
        outdoor activity, policy decisions, and overall well-being.
    </div>
    """, unsafe_allow_html=True)

    st.success("✨ Pastel-styled overview ready! Let me know if you want icons, animations, or card layouts added.")
