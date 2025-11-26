import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="AQI Dashboard",
    layout="wide"
)

# ----------------------------------------------------------
# PASTEL THEME + UNIQUE HOVER COLORS + ICONS
# ----------------------------------------------------------
st.markdown("""
    <style>

    [data-testid="stSidebar"] {
        background-color: #F4F6FA;
    }

    .sidebar-title {
        font-size: 26px;
        font-weight: 700;
        color: #4A4A4A;
        padding-bottom: 12px;
    }

    /* Hide radio circle icons */
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* Base tab style */
    div[role="radiogroup"] > label {
        background-color: #ffffff;
        border: 1px solid #E2E6ED;
        padding: 12px 16px;
        margin: 6px 0;
        border-radius: 10px;
        width: 100%;
        cursor: pointer;
        color: #344767;
        font-size: 17px;
        transition: 0.2s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Active tab */
    div[aria-checked="true"] {
        background-color: #A7C4FF !important;
        border-color: #7CA4FF !important;
        color: black !important;
        font-weight: 600 !important;
    }

    /* Hover pastel colors for each tab */
    div[role="radiogroup"] > label:nth-child(1):hover {
        background-color: #FFE8E8 !important;
        border-color: #FFCCCC !important;
    }
    div[role="radiogroup"] > label:nth-child(2):hover {
        background-color: #FFF4D6 !important;
        border-color: #FFE4A1 !important;
    }
    div[role="radiogroup"] > label:nth-child(3):hover {
        background-color: #E8FFF3 !important;
        border-color: #B9F5D0 !important;
    }
    div[role="radiogroup"] > label:nth-child(4):hover {
        background-color: #E9F2FF !important;
        border-color: #A7C4FF !important;
    }
    div[role="radiogroup"] > label:nth-child(5):hover {
        background-color: #F5E8FF !important;
        border-color: #D6B6FF !important;
    }
    div[role="radiogroup"] > label:nth-child(6):hover {
        background-color: #FFF0F5 !important;
        border-color: #FFC4D6 !important;
    }
    div[role="radiogroup"] > label:nth-child(7):hover {
        background-color: #dadfe0 !important;
        border-color: #b7bdbe !important;
    }

    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# SIDEBAR NAVIGATION WITH ICONS
# ----------------------------------------------------------

# Your only sidebar title (WILL NOT duplicate now)
st.sidebar.markdown("<div class='sidebar-title'>🗺️ Navigation</div>", unsafe_allow_html=True)

tabs = [
    "🏠 Overview",
    "ℹ️ Dataset Information",
    "🧹 Data Cleaning",
    "📊 Exploratory Data Analysis",
    "🤖 Data Modeling and Predictions",
    "🧮 CPCB AQI Calculator",
    "📚 References"
]

# FIX: Use label=" " to prevent the empty label from appearing as a header
page = st.sidebar.radio(" ", tabs, index=0)

# Clean mapping without emojis for routing
page_clean = page.split(" ", 1)[1]

# ----------------------------------------------------------
# ROUTING
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
