import streamlit as st

# ----------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------
st.set_page_config(
    page_title="AQI Dashboard",
    layout="wide"
)

# ----------------------------------------------------------------
# CSS — PASTEL THEME WITH CLEAN DASHBOARD SIDEBAR
# ----------------------------------------------------------------
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
    color: #3A3A3A;
    margin-bottom: 18px;
}

/* Main menu block */
.menu-block {
    padding: 12px 16px;
    margin: 6px 0;
    border-radius: 10px;
    background: white;
    border: 1px solid #E0E4EB;
    font-size: 17px;
    color: #344767;
    cursor: pointer;
    transition: all 0.2s ease;
}

.menu-block:hover {
    background: #E9F2FF;
    border-color: #A7C4FF;
}

.menu-active {
    background: #A7C4FF !important;
    border-color: #7CA4FF !important;
    color: black !important;
    font-weight: 600 !important;
}

/* Submenu Container */
.submenu-box {
    margin-left: 20px;
    margin-top: 6px;
}

/* Submenu item */
.submenu-block {
    padding: 9px 12px;
    margin: 4px 0;
    border-radius: 8px;
    background: #FFFFFF;
    border: 1px solid #D8DFEA;
    font-size: 15px;
    color: #455A64;
    cursor: pointer;
}

.submenu-block:hover {
    background: #E9F2FF !important;
    border-color: #A7C4FF !important;
}

.submenu-active {
    background: #CDE0FF !important;
    border-color: #7CA4FF !important;
    color: black !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------
if "active_page" not in st.session_state:
    st.session_state.active_page = "Overview"

if "eda_open" not in st.session_state:
    st.session_state.eda_open = False

if "active_eda" not in st.session_state:
    st.session_state.active_eda = "Distribution Analysis"


# ----------------------------------------------------------------
# CLICK HANDLERS (NO STREAMLIT BUTTONS!)
# ----------------------------------------------------------------
def go_to(page):
    st.session_state.active_page = page
    if page != "Exploratory Data Analysis":
        st.session_state.eda_open = False

def go_to_eda(subpage):
    st.session_state.active_page = "Exploratory Data Analysis"
    st.session_state.eda_open = True
    st.session_state.active_eda = subpage


# ----------------------------------------------------------------
# HTML MENU RENDERER (NO BUTTONS)
# ----------------------------------------------------------------
def menu_item(label, page_name):
    active = st.session_state.active_page == page_name
    css = "menu-block menu-active" if active else "menu-block"

    if st.sidebar.markdown(
        f"<div class='{css}'>{label}</div>",
        unsafe_allow_html=True
    ):
        pass

    if st.sidebar.container().button(label, key=f"click_{page_name}", help="", type="secondary"):
        go_to(page_name)


def submenu_item(label, eda_name):
    active = st.session_state.active_eda == eda_name
    css = "submenu-block submenu-active" if active else "submenu-block"

    if st.sidebar.markdown(f"<div class='{css}'>{label}</div>", unsafe_allow_html=True):
        pass

    if st.sidebar.container().button(label, key=f"eda_{eda_name}", type="secondary", help=""):
        go_to_eda(eda_name)


# ----------------------------------------------------------------
# SIDEBAR UI
# ----------------------------------------------------------------
st.sidebar.markdown("<div class='sidebar-title'>🗺️ Navigation</div>", unsafe_allow_html=True)

menu_item("🏠 Overview", "Overview")
menu_item("ℹ️ Dataset Information", "Dataset Information")
menu_item("🧹 Data Cleaning", "Data Cleaning")

# EDA toggler
eda_active = st.session_state.active_page == "Exploratory Data Analysis"
eda_css = "menu-block menu-active" if eda_active else "menu-block"

if st.sidebar.markdown(f"<div class='{eda_css}'>📊 Exploratory Data Analysis</div>", unsafe_allow_html=True):
    pass

if st.sidebar.button("📊", key="toggle_eda", help="Expand EDA submenu"):
    st.session_state.eda_open = not st.session_state.eda_open
    st.session_state.active_page = "Exploratory Data Analysis"

# Submenu items
if st.session_state.eda_open:

    st.sidebar.markdown("<div class='submenu-box'>", unsafe_allow_html=True)

    submenu_item("Distribution Analysis", "Distribution Analysis")
    submenu_item("Time-Series Analysis", "Time-Series Analysis")
    submenu_item("Correlation Matrix", "Correlation Matrix")
    submenu_item("AQI Category Analysis", "AQI Category Analysis")
    submenu_item("Seasonal Patterns", "Seasonal Patterns")
    submenu_item("Comparison Tool", "Comparison Tool")

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

menu_item("🤖 Data Modeling and Predictions", "Data Modeling and Predictions")
menu_item("🧮 CPCB AQI Calculator", "CPCB AQI Calculator")
menu_item("📚 References", "References")


# ----------------------------------------------------------------
# PAGE ROUTING
# ----------------------------------------------------------------
page = st.session_state.active_page
eda_page = st.session_state.active_eda

if page == "Overview":
    import pages.Overview as pg

elif page == "Dataset Information":
    import pages.Dataset_Information as pg

elif page == "Data Cleaning":
    import pages.Data_Cleaning as pg

elif page == "Exploratory Data Analysis":
    if eda_page == "Distribution Analysis":
        import pages.EDA_Distribution as pg
    elif eda_page == "Time-Series Analysis":
        import pages.EDA_Timeseries as pg
    elif eda_page == "Correlation Matrix":
        import pages.EDA_Correlation as pg
    elif eda_page == "AQI Category Analysis":
        import pages.EDA_AQI_Category as pg
    elif eda_page == "Seasonal Patterns":
        import pages.EDA_Seasonal as pg
    elif eda_page == "Comparison Tool":
        import pages.EDA_Comparison as pg

elif page == "Data Modeling and Predictions":
    import pages.Data_Modeling_and_Predictions as pg

elif page == "CPCB AQI Calculator":
    import pages.CPCB_AQI_Calculator as pg

elif page == "References":
    import pages.References as pg

pg.show()
