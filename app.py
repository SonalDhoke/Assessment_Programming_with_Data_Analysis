import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="AQI Dashboard",
    layout="wide"
)

# ----------------------------------------------------------
# CSS PASTEL DASHBOARD SIDEBAR
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
    margin-bottom: 18px;
}

/* MAIN MENU ITEM */
.menu-item {
    padding: 14px 16px;
    margin: 8px 0;
    border-radius: 12px;
    background: white;
    border: 1px solid #E2E6ED;
    font-size: 17px;
    color: #344767;
    cursor: pointer;
    transition: 0.2s;
}

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
.submenu-box {
    margin-left: 25px;
    margin-top: 4px;
}

/* SUBMENU ITEM */
.submenu-item {
    padding: 10px 14px;
    margin: 4px 0;
    border-radius: 10px;
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
# CLICK HANDLING USING QUERY PARAMS (WORKS PERFECTLY)
# ----------------------------------------------------------
query_params = st.query_params

if "page" in query_params:
    st.session_state.active_page = query_params["page"][0]

if "eda" in query_params:
    st.session_state.active_eda = query_params["eda"][0]
    st.session_state.eda_open = True


def link(label, page=None, eda=None, submenu=False, active=False):
    """Render a clickable HTML div with query params."""

    css = "submenu-item" if submenu else "menu-item"
    if active:
        css += " submenu-active" if submenu else "menu-active"

    # Build link
    params = {}
    if page:
        params["page"] = page
    if eda:
        params["eda"] = eda
        params["page"] = "Exploratory Data Analysis"

    url = st.experimental_get_query_params()

    # Convert params into URL string
    qp = "&".join([f"{k}={v}" for k, v in params.items()])
    href = f"?{qp}" if qp else "?"

    html = f"<a href='{href}' style='text-decoration:none;'><div class='{css}'>{label}</div></a>"
    st.sidebar.markdown(html, unsafe_allow_html=True)


# ----------------------------------------------------------
# SIDEBAR UI
# ----------------------------------------------------------
st.sidebar.markdown("<div class='sidebar-title'>🗺️ Navigation</div>", unsafe_allow_html=True)

# Main Pages
link("🏠 Overview", page="Overview", active=st.session_state.active_page == "Overview")
link("ℹ️ Dataset Information", page="Dataset Information", active=st.session_state.active_page == "Dataset Information")
link("🧹 Data Cleaning", page="Data Cleaning", active=st.session_state.active_page == "Data Cleaning")

# EDA (toggles submenu)
active_eda_main = st.session_state.active_page == "Exploratory Data Analysis"
link("📊 Exploratory Data Analysis", page="Exploratory Data Analysis", active=active_eda_main)

# Show submenu when inside EDA
if active_eda_main:

    st.sidebar.markdown("<div class='submenu-box'>", unsafe_allow_html=True)

    link("Distribution Analysis", eda="Distribution Analysis", submenu=True,
         active=st.session_state.active_eda == "Distribution Analysis")

    link("Time-Series Analysis", eda="Time-Series Analysis", submenu=True,
         active=st.session_state.active_eda == "Time-Series Analysis")

    link("Correlation Matrix", eda="Correlation Matrix", submenu=True,
         active=st.session_state.active_eda == "Correlation Matrix")

    link("AQI Category Analysis", eda="AQI Category Analysis", submenu=True,
         active=st.session_state.active_eda == "AQI Category Analysis")

    link("Seasonal Patterns", eda="Seasonal Patterns", submenu=True,
         active=st.session_state.active_eda == "Seasonal Patterns")

    link("Comparison Tool", eda="Comparison Tool", submenu=True,
         active=st.session_state.active_eda == "Comparison Tool")

    st.sidebar.markdown("</div>", unsafe_allow_html=True)


# Remaining Pages
link("🤖 Data Modeling and Predictions", page="Data Modeling and Predictions",
     active=st.session_state.active_page == "Data Modeling and Predictions")

link("🧮 CPCB AQI Calculator", page="CPCB AQI Calculator",
     active=st.session_state.active_page == "CPCB AQI Calculator")

link("📚 References", page="References",
     active=st.session_state.active_page == "References")


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
