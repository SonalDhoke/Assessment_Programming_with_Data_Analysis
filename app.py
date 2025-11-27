import streamlit as st

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="AQI Dashboard",
    layout="wide"
)

# ----------------------------------------------------------
# CSS STYLING (pastel theme + nested submenu styling)
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

/* MAIN MENU BUTTON STYLING */
.menu-btn {
    background-color: white;
    border: 1px solid #E2E6ED;
    padding: 12px 16px;
    margin-bottom: 6px;
    width: 100%;
    border-radius: 10px;
    font-size: 17px;
    color: #344767;
    cursor: pointer;
    transition: 0.2s;
}

.menu-btn:hover {
    background-color: #E9F2FF;
    border-color: #A7C4FF;
}

/* ACTIVE MAIN MENU ITEM */
.menu-active {
    background-color: #A7C4FF !important;
    border-color: #7CA4FF !important;
    color: black !important;
    font-weight: 600 !important;
}

/* SUBMENU CONTAINER */
.submenu-box {
    padding-left: 22px;
    padding-top: 4px;
}

/* SUBMENU ITEM */
.submenu-btn {
    background-color: #FFFFFF;
    border: 1px solid #D8DFEA;
    padding: 8px 14px;
    margin: 4px 0;
    width: 100%;
    border-radius: 8px;
    font-size: 15px;
    color: #455A64;
    cursor: pointer;
    transition: 0.2s;
}

.submenu-btn:hover {
    background-color: #E9F2FF !important;
    border-color: #A7C4FF !important;
}

/* ACTIVE SUBMENU ITEM */
.submenu-active {
    background-color: #CDE0FF !important;
    border-color: #7CA4FF !important;
    color: black !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# SIDEBAR STATE
# ----------------------------------------------------------
if "active_page" not in st.session_state:
    st.session_state.active_page = "Overview"

if "eda_submenu_open" not in st.session_state:
    st.session_state.eda_submenu_open = False

if "active_eda" not in st.session_state:
    st.session_state.active_eda = "Distribution Analysis"


# ----------------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------------

def main_menu_button(label, key, icon):
    """Creates a main menu button inside sidebar."""
    is_active = (st.session_state.active_page == label)
    css_class = "menu-btn " + ("menu-active" if is_active else "")

    clicked = st.sidebar.button(f"{icon} {label}", key=key, use_container_width=True)
    if clicked:
        st.session_state.active_page = label
        return True
    return False


def submenu_button(label, key):
    """Creates submenu buttons under EDA."""
    is_active = (st.session_state.active_eda == label)
    css_class = "submenu-btn " + ("submenu-active" if is_active else "")

    clicked = st.sidebar.button(label, key=key, use_container_width=True)
    if clicked:
        st.session_state.active_eda = label
        return True
    return False


# ----------------------------------------------------------
# SIDEBAR MENU (WITH INLINE SUBMENU)
# ----------------------------------------------------------

st.sidebar.markdown("<div class='sidebar-title'>🗺️ Navigation</div>", unsafe_allow_html=True)

# ----------- Overview -----------
if main_menu_button("Overview", "menu_overview", "🏠"):
    st.session_state.eda_submenu_open = False

# ----------- Dataset Info -----------
if main_menu_button("Dataset Information", "menu_dataset", "ℹ️"):
    st.session_state.eda_submenu_open = False

# ----------- Data Cleaning -----------
if main_menu_button("Data Cleaning", "menu_clean", "🧹"):
    st.session_state.eda_submenu_open = False

# ----------- Exploratory Data Analysis (TOGGLES SUBMENU) -----------
clicked_eda = main_menu_button("Exploratory Data Analysis", "menu_eda", "📊")

if clicked_eda:
    st.session_state.eda_submenu_open = not st.session_state.eda_submenu_open

# ----------- SUBMENU APPEARS HERE — EXACTLY UNDER EDA -----------
eda_choice = None

if st.session_state.eda_submenu_open:

    st.sidebar.markdown("<div class='submenu-box'>", unsafe_allow_html=True)

    if submenu_button("Distribution Analysis", "sub_dist"):
        pass
    if submenu_button("Time-Series Analysis", "sub_ts"):
        pass
    if submenu_button("Correlation Matrix", "sub_corr"):
        pass
    if submenu_button("AQI Category Analysis", "sub_cat"):
        pass
    if submenu_button("Seasonal Patterns", "sub_season"):
        pass
    if submenu_button("Comparison Tool", "sub_comp"):
        pass

    st.sidebar.markdown("</div>", unsafe_allow_html=True)


# ----------- Data Modeling -----------
if main_menu_button("Data Modeling and Predictions", "menu_model", "🤖"):
    st.session_state.eda_submenu_open = False

# ----------- Calculator -----------
if main_menu_button("CPCB AQI Calculator", "menu_calc", "🧮"):
    st.session_state.eda_submenu_open = False

# ----------- References -----------
if main_menu_button("References", "menu_ref", "📚"):
    st.session_state.eda_submenu_open = False


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
