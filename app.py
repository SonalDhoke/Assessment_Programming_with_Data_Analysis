import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="AQI Dashboard",
    layout="wide"
)

# ----------------------------------------------------------
# PASTEL CSS THEME FOR SIDEBAR
# ----------------------------------------------------------
st.markdown("""
<style>

[data-testid="stSidebar"] {
    background-color: #F4F6FA;
    padding-top: 20px;
}

/* Sidebar Title */
.sidebar-title {
    font-size: 26px;
    font-weight: 700;
    color: #333333;
    margin-bottom: 20px;
}

/* Sidebar Menu Items */
.sidebar-radio label {
    background-color: #ffffff !important;
    border: 1px solid #E2E6ED !important;
    padding: 12px 16px !important;
    margin: 6px 0 !important;
    border-radius: 10px !important;
    width: 100% !important;
    cursor: pointer !important;
    color: #344767 !important;
    font-size: 17px !important;
    transition: 0.2s ease !important;
}

/* Hover Effects */
.sidebar-radio label:hover {
    background-color: #E9F2FF !important;
    border-color: #A7C4FF !important;
}

/* Active Option */
.sidebar-radio [data-testid="stRadio"] > div[aria-checked="true"] {
    background-color: #A7C4FF !important;
    border-color: #7CA4FF !important;
    color: black !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# SIDEBAR NAVIGATION (MAIN MENU ONLY)
# ----------------------------------------------------------

st.sidebar.markdown("<div class='sidebar-title'>🗺️ Navigation</div>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    [
        "🏠 Overview",
        "ℹ️ Dataset Information",
        "🧹 Data Cleaning",
        "📊 Exploratory Data Analysis",
        "🤖 Data Modeling and Predictions",
        "🧮 CPCB AQI Calculator",
        "📚 References"
    ],
    key="main_nav",
    help="Select a page"
)

# Clean label for routing
page_clean = page.split(" ", 1)[1]

# ----------------------------------------------------------
# PAGE ROUTING
# ----------------------------------------------------------

if page_clean == "Overview":
    import pages.Overview as pg
    pg.show()

elif page_clean == "Dataset Information":
    import pages.Dataset_Information as pg
    pg.show()

elif page_clean == "Data Cleaning":
    import pages.Data_Cleaning as pg
    pg.show()

elif page_clean == "Exploratory Data Analysis":
    import pages.Exploratory_Data_Analysis as pg
    pg.show()

elif page_clean == "Data Modeling and Predictions":
    import pages.Data_Modeling_and_Predictions as pg
    pg.show()

elif page_clean == "CPCB AQI Calculator":
    import pages.CPCB_AQI_Calculator as pg
    pg.show()

elif page_clean == "References":
    import pages.References as pg
    pg.show()
