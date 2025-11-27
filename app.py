import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="AQI Dashboard",
    layout="wide"
)

# ----------------------------------------------------------
# CSS: PASTEL DASHBOARD SIDEBAR + NESTED SUBMENU
# ----------------------------------------------------------
st.markdown("""
<style>

[data-testid="stSidebar"] {
    background: #F4F6FA;
    padding-top: 20px;
}

/* Sidebar Title */
.sidebar-title {
    font-size: 26px;
    font-weight: 700;
    color: #4A4A4A;
    margin-bottom: 15px;
}

/* MAIN MENU ITEM */
.menu-item {
    padding: 12px 16px;
    margin: 6px 0;
    border-radius: 10px;
    background: white;
    border: 1px solid #E2E6ED;
    font-size: 17px;
    color: #344767;
    cursor: pointer;
    transition: 0.2s;
}

/* MAIN MENU HOVER */
.menu-item:hover {
    background: #E9F2FF;
    border-color: #A7C4FF;
}

/* ACTIVE MAIN PAGE */
.menu-active {
    background: #A7C4FF !important;
    border-color: #7CA4FF !important;
    color: black !important;
    font-weight: 600;
}

/* SUBMENU WRAPPER */
.submenu-wrapper {
    margin-left: 20px;
    margin-top: 5px;
}

/* SUBMENU ITEM */
.submenu-item {
    padding: 8px 14px;
    margin: 4px 0;
    border-radius: 8px;
    background: #FFFFFF;
    border: 1px solid #D8DFEA;
    font-size: 15px;
    color: #455A64;
    cursor: pointer;
    transition: 0.2s;
}

/* SUBMENU HOVER */
.submenu-item:hover {
    background: #E9F2FF !important;
    border-color: #A7C4FF !important;
}

/* ACTIVE SUBMENU */
.submenu-active {
    background: #CDE0FF !important;
    border-color: #7CA4FF !important;
    color: black !important;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------
if "active_page" not in st.session_state:
    st.session_state.active_page = "Overview"

if "eda_open" not in st.session_state:
    st.session_state.eda_open = False

if "active_eda" not in st.session_state:
    st.session_state.active_eda = "Distribution Analysis"


# ----------------------------------------------------------
# FUNCTION: MAIN MENU CLICK
# ----------------------------------------------------------
def click_main_page(page):
    st.session_state.active_page = page
    if page != "Exploratory Data Analysis":
        st.session_state.eda_open = False


# ----------------------------------------------------------
# FUNCTION: SUBMENU CLICK
# ----------------------------------------------------------
def click_submenu(item):
    st.session_state.active_page = "Exploratory Data Analysis"
    st.session_state.active_eda = item


# ----------------------------------------------------------
# SIDEBAR UI (HTML)
# ----------------------------------------------------------
st.sidebar.markdown("<div class='sidebar-title'>🗺️ Navigation</div>", unsafe_allow_html=True)

# Helper to draw a clickable div
def clickable(label, active, key):
    css = "menu-item"
    if active:
        css += " menu-active"
    if st.sidebar.button(label, key=key):
        return True
    st.sidebar.markdown(f"<div class='{css}'>{label}</div>", unsafe_allow_html=True)
    return False


# ---------------- MAIN MENU ITEMS ----------------

if clickable("🏠 Overview", st.session_state.active_page == "Overview", "p_overview"):
    click_main_page("Overview")

if clickable("ℹ️ Dataset Information", st.session_state.active_page == "Dataset Information", "p_dataset"):
    click_main_page("Dataset Information")

if clickable("🧹 Data Cleaning", st.session_state.active_page == "Data Cleaning", "p_clean"):
    click_main_page("Data Cleaning")

# ----------- EXPANDABLE EDA MENU -----------
if clickable("📊 Exploratory Data Analysis", st.session_state.active_page == "Exploratory Data Analysis", "p_eda"):
    st.session_state.active_page = "Exploratory Data Analysis"
    st.session_state.eda_open = not st.session_state.eda_open

# ----------- SHOW NESTED SUBMENU HERE -----------
if st.session_state.eda_open:

    st.sidebar.markdown("<div class='submenu-wrapper'>", unsafe_allow_html=True)

    def submenu(label, key):
        active = (st.session_state.active_eda == label)
        css = "submenu-item submenu-active" if active else "submenu-item"
        if st.sidebar.button(label, key=key):
            click_submenu(label)
        st.sidebar.markdown(f"<div class='{css}'>{label}</div>", unsafe_allow_html=True)

    submenu("Distribution Analysis", "sub1")
    submenu("Time-Series Analysis", "sub2")
    submenu("Correlation Matrix", "sub3")
    submenu("AQI Category Analysis", "sub4")
    submenu("Seasonal Patterns", "sub5")
    submenu("Comparison Tool", "sub6")

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------
# Remaining main menu items
# ---------------------------------------------

if clickable("🤖 Data Modeling and Predictions", st.session_state.active_page == "Data Modeling and Predictions", "p_model"):
    click_main_page("Data Modeling and Predictions")

if clickable("🧮 CPCB AQI Calculator", st.session_state.active_page == "CPCB AQI Calculator", "p_calc"):
    click_main_page("CPCB AQI Calculator")

if clickable("📚 References", st.session_state.active_page == "References", "p_ref"):
    click_main_page("References")


# ----------------------------------------------------------
# PAGE ROUTING
# ----------------------------------------------------------
page = st.session_state.active_page
eda_page = st.session_state.active_eda

if page == "Overview":
    import pages.Overview as pg
    pg.show()

elif page == "Dataset Information":
    import pages.Dataset_Information as pg
    pg.show()

elif page == "Data Cleaning":
    import pages.Data_Cleaning as pg
    pg.show()

elif page == "Exploratory Data Analysis":

    if eda_page == "Distribution Analysis":
        import pages.EDA_Distribution as pg
        pg.show()

    elif eda_page == "Time-Series Analysis":
        import pages.EDA_Timeseries as pg
        pg.show()

    elif eda_page == "Correlation Matrix":
        import pages.EDA_Correlation as pg
        pg.show()

    elif eda_page == "AQI Category Analysis":
        import pages.EDA_AQI_Category as pg
        pg.show()

    elif eda_page == "Seasonal Patterns":
        import pages.EDA_Seasonal as pg
        pg.show()

    elif eda_page == "Comparison Tool":
        import pages.EDA_Comparison as pg
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
