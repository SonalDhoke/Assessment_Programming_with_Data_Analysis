import streamlit as st

# ----------------------------------------------------------
# Page Config
# ----------------------------------------------------------
st.set_page_config(page_title="AQI Dashboard", layout="wide")

# ----------------------------------------------------------
# Sidebar Navigation
# ----------------------------------------------------------
st.sidebar.title("🗺️ Navigation")

main_menu = st.sidebar.radio(
    "Go to page:",
    [
        "Overview",
        "Dataset Information",
        "Data Cleaning",
        "Exploratory Data Analysis",
        "Data Modeling and Predictions",
        "CPCB AQI Calculator",
        "References"
    ]
)

# ----------------------------------------------------------
# Submenu (only visible for EDA)
# ----------------------------------------------------------
eda_sub = None

if main_menu == "Exploratory Data Analysis":
    eda_sub = st.sidebar.radio(
        "EDA Options:",
        [
            "Distribution Analysis",
            "Time-Series Analysis",
            "Correlation Matrix",
            "AQI Category Analysis",
            "Seasonal Patterns",
            "Comparison Tool"
        ]
    )

# ----------------------------------------------------------
# Routing Logic
# ----------------------------------------------------------

if main_menu == "Overview":
    import pages.Overview as pg
    pg.show()

elif main_menu == "Dataset Information":
    import pages.Dataset_Information as pg
    pg.show()

elif main_menu == "Data Cleaning":
    import pages.Data_Cleaning as pg
    pg.show()

elif main_menu == "Exploratory Data Analysis":

    if eda_sub == "Distribution Analysis":
        import pages.EDA_Distribution as pg
        pg.show()

    elif eda_sub == "Time-Series Analysis":
        import pages.EDA_Timeseries as pg
        pg.show()

    elif eda_sub == "Correlation Matrix":
        import pages.EDA_Correlation as pg
        pg.show()

    elif eda_sub == "AQI Category Analysis":
        import pages.EDA_AQI_Category as pg
        pg.show()

    elif eda_sub == "Seasonal Patterns":
        import pages.EDA_Seasonal as pg
        pg.show()

    elif eda_sub == "Comparison Tool":
        import pages.EDA_Comparison as pg
        pg.show()

elif main_menu == "Data Modeling and Predictions":
    import pages.Data_Modeling_and_Predictions as pg
    pg.show()

elif main_menu == "CPCB AQI Calculator":
    import pages.CPCB_AQI_Calculator as pg
    pg.show()

elif main_menu == "References":
    import pages.References as pg
    pg.show()
