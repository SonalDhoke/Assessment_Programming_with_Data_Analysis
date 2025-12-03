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
    🔗 https://cpcb.nic.in/displaypdf.php?id=bmF0aW9uYWwtYWlyLXF1YWxpdHktaW5kZXgvRklOQUwtUkVQT1JUX0FRSV8ucGRm
    
    Contains official AQI breakpoints, calculation methodology, 
    health categories, and pollutant standards.

    **2. CPCB – Real-Time Air Quality Dashboard**  
    🔗 https://app.cpcbccr.com/AQI_India/  
    Live AQI & pollution levels from continuous monitoring systems.

    **3. CPCB – Air Quality Standards for India**  
    🔗 https://cpcb.nic.in/upload/NAAQS_2019.pdf
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

    # -------------------- Scientific Articles --------------------
    st.subheader("📖 Scientific Articles & Research")

    st.markdown("""
    **1. Assessment and forecasting of particulate matter emissions and structural health monitoring of buildings**  
    🔗 https://www.nature.com/articles/s41598-025-00814-9  

    **2. PM2.5 Health Impact Studies (Lancet)**  
    🔗 https://www.thelancet.com/journals/lanplh/article/PIIS2542-5196(21)00350-8/fulltext 

    **3. Atmospheric Chemistry of NO, NO₂, NOx**  
    🔗 https://www.sciencedirect.com/science/article/abs/pii/S1352231022006276  
    """)

    st.markdown("---")
     # -------------------- Data Modeling --------------------
    st.subheader("🤖 Data Modeling and Predictions")

    st.markdown("""
    **1. Air Quality Index Predictions Using Supervised ML Classifiers**  
    🔗 https://eprint.innovativepublication.org/id/eprint/1787/1/IJISRT25JUL758%20%281%29.pdf  
    

    **2. Air Quality Prediction System using LightGBM**  
    🔗 https://www.irjet.net/archives/V7/i7/IRJET-V7I7678.pdf 
    
    """)

    st.markdown("---")

    st.success("References updated successfully!")
