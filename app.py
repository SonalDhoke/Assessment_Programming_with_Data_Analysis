import streamlit as st

st.set_page_config(
    page_title="AQI Project Dashboard",
    layout="wide"
)

st.sidebar.title("Navigation")

# Side navigation
page = st.sidebar.radio(
    "Go to:",
    (
        "Overview",
        "Data Cleaning",
        "Exploratory Data Analysis",
        "Data Modeling and Predictions",
        "CPCB AQI Calculator",
        "References"
    ),
    index=0   # default page = Overview
)

# Load pages dynamically
if page == "Overview":
    import pages.Overview as pg
    pg.show()

elif page == "Data Cleaning":
    import pages.Data_Cleaning as pg
    pg.show()

elif page == "Exploratory Data Analysis":
    import pages.Exploratory_Data_Analysis as pg
    pg.show()

elif page == "Data Modeling and Predictions":
    import pages.Data_Modeling_and_Predictions as pg
    pg.show()

elif page == "CPCB AQI Calculator":
    import pages.CPCB_AQI_Calculator as pg
    pg.show()

elif page == "References":
    import pages.References as pg
    pg.show()
