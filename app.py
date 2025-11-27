import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------
st.set_page_config(
    page_title="AQI Dashboard",
    layout="wide"
)

# ----------------------------------------------------------
# PASTEL CSS THEME
# ----------------------------------------------------------
st.markdown("""
<style>

[data-testid="stSidebar"] {
    background: #F4F6FA;
    padding-top: 15px;
}

/* Sidebar Title */
.sidebar-title {
    font-size: 26px;
    font-weight: 700;
    color: #3A3A3A;
    margin-bottom: 18px;
}

/* Main Menu Item */
.menu-item {
    padding: 12px 16px;
    margin: 6px 0;
    border-radius: 10px;
    background: #FFFFFF;
    border: 1px solid #E0E4EB;
    font-size: 17px;
    color: #344767;
    cursor: pointer;
    transition: all 0.2s ease;
}

.menu-item:hover {
    background: #E9F2FF;
    border-color: #A7C4FF;
}

/* Active main item */
.menu-active {
    background: #A7C4FF !important;
    border-color: #7CA4FF !important;
    color: black !important;
    font-weight: 600 !important;
}

/* Submenu container */
.submenu-box {
    margin-left: 18px;
    margin-top: 6px;
}

/* Submenu item */
.submenu-item {
    padding: 9px 12px;
    margin: 4px 0;
    border-radius: 8px;
    background: #FFFFFF;
    border: 1px solid #D8DFEA;
    font-size: 15px;
    color: #455A64;
    cursor: pointer;
    transition: 0.2s;
}

.submenu-item:hover {
    background: #E9F2FF !important;
    border-color: #A7C4FF !important;
}

/* Active submenu */
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
# CLICK HANDLERS
# ----------------------------------------------------------
def go_to(page):
    """Navigate to a top-level page."""
    st.session_state.active_page = page
    if page != "Exploratory Data Analysis":
        st.session_state.eda_open = False


def go_to_eda(subpage):
    """Load an EDA subpage."""
    st.session_state.active_page = "Exploratory Data Analysis"
    st.session_state.eda_open = True
    st.session_state.active_eda = subpage


# ----------------------------------------------------------
# HTML RENDER HELPERS
# ----------------------------------------------------------
def menu(label, page_name):
    """Main menu item."""
    active = (st.session_state.active_page == page_name)
    css = "menu-item menu-active" if active else "menu-item"

    if st.sidebar.button(label, key=page_name, use_container_width=True):
        go_to(page_name)

    st.sidebar.markdown(f"<div class='{css}'>{label}</div>", unsafe_allow_html=True)


def submenu(label, eda_name):
    """EDA submenu item."""
    active = (st.session_state.active_eda == eda_name)
    css = "submenu-item submenu-active" if active else "submenu-item"

    if st.sidebar.button(label, key=eda_name, use_container_width=True):
        go_to_eda(eda_name)

    st.sidebar.markdown(f"<div class='{css}'>{label}</div>", unsafe_allow_html=True)


# ----------------------------------------------------------
# SIDEBAR UI
# ----------------------------------------------------------
st.sidebar.markdown("<div class='sidebar-title'>🗺️ Navigation</div>", unsafe_allow_html=True)

# Main menu buttons
menu("🏠 Overview", "Overview")
menu("ℹ️ Dataset Information", "Dataset Information")
menu("🧹 Data Cleaning", "Data Cleaning")

# EDA main menu button
if st.sidebar.button("📊 Exploratory Data Analysis", key="EDA", use_container_width=True):
    st.session_state.active_page = "Exploratory Data Analysis"
    st.session_state.eda_open = not st.session_state.eda_open

# Render EDA button visual
st.sidebar.markdown(
    f"<div class='menu-item {'menu-active' if st.session_state.active_page=='Exploratory Data Analysis' else ''}'>📊 Exploratory Data Analysis</div>",
    unsafe_allow_html=True
)

# If EDA is open → show submenu
if st.session_state.eda_open:
    st.sidebar.markdown("<div class='submenu-box'>", unsafe_allow_html=True)

    submenu("Distribution Analysis", "Distribution Analysis")
    submenu("Time-Series Analysis", "Time-Series Analysis")
    submenu("Correlation Matrix", "Correlation Matrix")
    submenu("AQI Category Analysis", "AQI Category Analysis")
    submenu("Seasonal Patterns", "Seasonal Patterns")
    submenu("Comparison Tool", "Comparison Tool")

    st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Remaining pages
menu("🤖 Data Modeling and Predictions", "Data Modeling and Predictions")
menu("🧮 CPCB AQI Calculator", "CPCB AQI Calculator")
menu("📚 References", "References")


# ----------------------------------------------------------
# PAGE ROUTING
# ----------------------------------------------------------
pg = None

page = st.session_state.active_page
eda = st.session_state.active_eda

if page == "Overview":
    import pages.Overview as pg

elif page == "Dataset Information":
    import pages.Dataset_Information as pg

elif page == "Data Cleaning":
    import pages.Data_Cleaning as pg

elif page == "Exploratory Data Analysis":
    if eda == "Distribution Analysis":
        import pages.EDA_Distribution as pg
    elif eda == "Time-Series Analysis":
        import pages.EDA_Timeseries as pg
    elif eda == "Correlation Matrix":
        import pages.EDA_Correlation as pg
    elif eda == "AQI Category Analysis":
        import pages.EDA_AQI_Category as pg
    elif eda == "Seasonal Patterns":
        import pages.EDA_Seasonal as pg
    elif eda == "Comparison Tool":
        import pages.EDA_Comparison as pg

elif page == "Data Modeling and Predictions":
    import pages.Data_Modeling_and_Predictions as pg

elif page == "CPCB AQI Calculator":
    import pages.CPCB_AQI_Calculator as pg

elif page == "References":
    import pages.References as pg

pg.show()
