import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="AQI Dashboard",
    layout="wide"
)

# ----------------------------------------------------------
# CUSTOM SIDEBAR UI (HIGHLIGHTED TABS)
# ----------------------------------------------------------
st.markdown("""
    <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #f7f7f7;
        }

        /* Title styling */
        .sidebar-title {
            font-size: 26px;
            font-weight: 700;
            color: #333;
            padding-bottom: 10px;
        }

        /* Sidebar tab container */
        .sidebar-item {
            padding: 10px 16px;
            margin: 6px 0;
            border-radius: 8px;
            font-size: 16px;
            color: #333;
            border: 1px solid transparent;
            transition: 0.2s ease-in-out;
        }

        /* Hover effect */
        .sidebar-item:hover {
            background-color: #e6f2ff;
            border-color: #99ccff;
        }

        /* Active tab */
        .sidebar-active {
            background-color: #3399ff !important;
            color: white !important;
            border: 1px solid #0073e6 !important;
            font-weight: 600;
        }

        /* Hide default radio buttons */
        div[role=radiogroup] > label > div:first-child {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# SIDEBAR NAVIGATION
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

# Radio button selection
page = st.sidebar.radio("Select page:", tabs)

# Highlighted items
for tab in tabs:
    if tab == page:
        st.sidebar.markdown(f"<div class='sidebar-item sidebar-active'>{tab}</div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown(f"<div class='sidebar-item'>{tab}</div>", unsafe_allow_html=True)

# ----------------------------------------------------------
# PAGE ROUTING — IMPORT CORRESPONDING FILE
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
