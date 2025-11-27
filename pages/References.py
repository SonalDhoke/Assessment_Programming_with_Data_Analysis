import streamlit as st

def show():

    st.title("📚 References & Data Sources")

    st.markdown("""
    Below are the official and authoritative sources related to air quality,
    weather data, CPCB standards, AQI breakpoints, pollutant health impacts,
    and research guidelines used throughout this AQI analysis project.
    """)

    st.markdown("---")

    # -------------------- CPCB --------------------
    st.subheader("🇮🇳 Central Pollution Control Board (CPCB)")

    st.markdown("""
    **1. CPCB – National Air Quality Index (AQI) Framework**  
    🔗 https://cpcb.nic.in/National-Air-Quality-Index/  
    Contains official AQI breakpoints, calculation methodology, 
    health categories, and pollutant standards.

    **2. CPCB – National Air Quality Monitoring Programme (NAMP)**  
    🔗 https://cpcb.nic.in/namp/  
    Provides monitored pollutant data collected from stations across India.

    **3. CPCB – Real-Time Air Quality Dashboard**  
    🔗 https://app.cpcbccr.com/AQI_India/  
    Live AQI & pollution levels from continuous monitoring systems.

    **4. CPCB – Air Quality Standards for India**  
    🔗 https://cpcb.nic.in/uploads/National_Air_Quality_Standards.pdf  
    Defines permissible pollutant limits and health impacts.
    """)

    st.markdown("---")

    # -------------------- IMD/MET (Mausam) --------------------
    st.subheader("🌦 Indian Meteorological Department (IMD / Mausam)")

    st.markdown("""
    **1. Mausam – IMD Weather Portal**  
    🔗 https://mausam.imd.gov.in/  
    Official weather observations, forecasts, and climate summaries.

    **2. IMD - Climate Data Service Portal**  
    🔗 https://imdpune.gov.in/  
    Long-term climate records, rainfall, temperature datasets.

    **3. IMD - Air Quality Forecasting & SAFAR**  
    🔗 https://safar.tropmet.res.in/  
    Multi-pollutant forecasts, health bulletins, AQI maps.
    """)

    st.markdown("---")

    # -------------------- MoEFCC --------------------
    st.subheader("🏛 Ministry of Environment, Forest and Climate Change (MoEFCC)")

    st.markdown("""
    **1. MoEFCC Official Website**  
    🔗 https://moef.gov.in/  
    Policies, environmental regulations, national clean air initiatives.

    **2. National Clean Air Programme (NCAP)**  
    🔗 https://ncap.niti.gov.in/  
    Government initiative to reduce particulate pollution by 20–30%.
    """)

    st.markdown("---")

    # -------------------- WHO --------------------
    st.subheader("🌍 World Health Organization (WHO) – Global Standards")

    st.markdown("""
    **1. WHO Global Air Quality Guidelines (2021)**  
    🔗 https://www.who.int/publications/i/item/9789240034228  
    Latest global exposure limits for PM2.5, PM10, NO₂, O₃, SO₂.

    **2. WHO Air Pollution Dashboard**  
    🔗 https://www.who.int/data/gho/data/themes/air-pollution  
    Global pollutant exposure, mortality statistics, risk assessments.
    """)

    st.markdown("---")

    # -------------------- NASA & Satellite Data --------------------
    st.subheader("🛰️ NASA / ESA – Satellite-Based Air Quality Sources")

    st.markdown("""
    **1. NASA Earth Data – Air Quality**  
    🔗 https://earthdata.nasa.gov/learn/toolkits/air-quality  
    Satellite datasets for aerosols, NO₂, SO₂, CO, ozone.

    **2. Sentinel-5P (ESA) – Atmosphere Monitoring**  
    🔗 https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-5p  
    Real-time mapping of trace gases (NO₂, SO₂, CO, O₃).
    """)

    st.markdown("---")

    # -------------------- Scientific Articles --------------------
    st.subheader("📖 Scientific Articles & Research")

    st.markdown("""
    **1. Air Quality Index Methodologies (Research Paper)**  
    🔗 https://www.sciencedirect.com/science/article/pii/S0160412020321208  

    **2. PM2.5 Health Impact Studies (Lancet)**  
    🔗 https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)32558-2/fulltext  

    **3. Atmospheric Chemistry of NO, NO₂, NOx**  
    🔗 https://acp.copernicus.org/articles/  
    """)

    st.markdown("---")

    st.success("References updated successfully!")
