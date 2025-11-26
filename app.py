import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="AQI Dashboard",
    layout="wide"
)

# ----------------------------------------------------------
# PASTEL THEME FOR RADIO BUTTONS
# ----------------------------------------------------------
st.markdown("""
    <style>

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #F4F6FA;
    }

    /* Remove the round radio buttons */
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* Style radio labels as pastel menu items */
    div[role="radiogroup"] > label {
        background-color: #ffffff;
        border: 1px solid #E2E6ED;
        padding: 12px 16px;
        margin: 6px 0;
        border-radius: 10px;
        width: 100%;
        transition: 0.2s ease;
        cursor: pointer;
        color: #344767;
        font-size: 17px;
    }

    /* Hover effect */
    div[role="radiogroup"] > label:hover {
        background-color: #E8F0FE;
        border-color: #A7C4FF;
    }

    /* Selected item */
    div[aria-checked="true"] {
        background-color: #A7C4FF !important;
        border-color: #7CA4FF !important;
        color: black !important;
        font-weight: 600 !important;
    }

    .sidebar-title {
        font-size: 26px;
        font-weight: 700;
        color: #4A4A4A;
        padding-bottom: 12px;
    }

    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# SIDEBAR NAVIGATION (FULLY INTERACTIVE)
# ----------------------------------------------------------

st.sidebar.markdown("<div class='sidebar-title'>📌 Navigation</div>", unsafe_allow_html=True)

tabs = [
    "Overview",
    "Data Cleaning",
    "Exploratory Data Analysis",
    "Data Modeling and Predictions",
    "CPCB AQI Calculator",
    "References"
]

# This radio is now clickable AND beautifully styled
page = st.sidebar.radio("Menu", tabs, index=0)

# ----------------------------------------------------------
# ROUTING TO OTHER PY FILES
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
