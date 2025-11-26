import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="AQI Dashboard",
    layout="wide"
)

# ----------------------------------------------------------
# PASTEL THEME + HIGHLIGHTED SIDEBAR (SINGLE NAV)
# ----------------------------------------------------------
st.markdown("""
    <style>

    /* Soft pastel background for sidebar */
    [data-testid="stSidebar"] {
        background-color: #F4F6FA;
    }

    .sidebar-title {
        font-size: 26px;
        font-weight: 700;
        padding-bottom: 12px;
        color: #4A4A4A;
    }

    /* Hide built-in radio labels so only custom menu shows */
    div[role="radiogroup"] label {
        display: none !important;
    }

    /* Menu item style */
    .menu-item {
        padding: 12px 16px;
        margin: 6px 0;
        border-radius: 10px;
        font-size: 17px;
        background-color: #ffffff;
        border: 1px solid #E2E6ED;
        color: #344767;
        transition: 0.2s ease;
    }

    /* Hover effect */
    .menu-item:hover {
        background-color: #E8F0FE;
        border-color: #A7C4FF;
    }

    /* Selected menu item (pastel highlight) */
    .menu-active {
        background-color: #A7C4FF !important;
        color: black !important;
        font-weight: 600;
        border: 1px solid #7CA4FF !important;
    }

    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------

tabs = [
    "Overview",
    "Data Cleaning",
    "Exploratory Data Analysis",
    "Data Modeling and Predictions",
    "CPCB AQI Calculator",
    "References"
]

# Underlying radio system (hidden visually)
page = st.sidebar.radio("Menu", tabs, index=0)

# Title
st.sidebar.markdown("<div class='sidebar-title'>📌 Navigation</div>", unsafe_allow_html=True)

# Custom visual menu
for tab in tabs:
    if tab == page:
        st.sidebar.markdown(f"<div class='menu-item menu-active'>{tab}</div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown(f"<div class='menu-item'>{tab}</div>", unsafe_allow_html=True)

# ----------------------------------------------------------
# ROUTING
# ----------------------------------------------------------

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
