import streamlit as st

# ----------------------------------------------------------
# CSS — Pastel Button Cards (Clickable DIVs)
# ----------------------------------------------------------
st.markdown("""
<style>

.eda-card {
    padding: 18px;
    margin: 10px 0;
    border-radius: 12px;
    font-size: 20px;
    font-weight: 600;
    cursor: pointer;
    border: 2px solid transparent;
    text-align: left;
    transition: 0.2s ease;
}

.dist   { background: #FFEAEA; border-color: #FFCCCC; }
.time   { background: #FFF4D6; border-color: #FFE4A1; }
.corr   { background: #E8FFF3; border-color: #B9F5D0; }
.cat    { background: #E9F2FF; border-color: #A7C4FF; }
.season { background: #F5E8FF; border-color: #D6B6FF; }
.comp   { background: #FFF0F5; border-color: #FFC4D6; }

.eda-card:hover {
    transform: translateY(-3px);
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.active-card {
    border: 3px solid #4A90E2 !important;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# PAGE LOGIC
# ----------------------------------------------------------
def show():
    st.title("📊 Exploratory Data Analysis")

    df = st.session_state.get("cleaned_df", None)
    if df is None:
        st.warning("⚠️ Please clean dataset first.")
        return

    if "eda_mode" not in st.session_state:
        st.session_state.eda_mode = "Distribution Analysis"

    st.markdown("### Choose an analysis module:")

    # EDA options
    options = {
        "Distribution Analysis": ("📈", "dist"),
        "Time-Series Analysis": ("🕒", "time"),
        "Correlation Matrix": ("🔗", "corr"),
        "AQI Category Analysis": ("🟢", "cat"),
        "Seasonal Patterns": ("🍂", "season"),
        "Comparison Tool": ("🔍", "comp"),
    }

    col1, col2 = st.columns(2)

    # Render cards (clickable)
    def render_card(label, icon, css_class):
        active = "active-card" if st.session_state.eda_mode == label else ""
        card_html = f"""
            <div class="eda-card {css_class} {active}" onclick="window.location.href='?eda={label}'">
                {icon} {label}
            </div>
        """
        return card_html

    import urllib.parse

    # Clicking is handled through query_params (safe)
    qp = st.query_params
    if "eda" in qp:
        st.session_state.eda_mode = urllib.parse.unquote(qp["eda"])

    # 6 cards split into 2 columns
    with col1:
        st.markdown(render_card("Distribution Analysis", "📈", "dist"), unsafe_allow_html=True)
        st.markdown(render_card("Correlation Matrix", "🔗", "corr"), unsafe_allow_html=True)
        st.markdown(render_card("Seasonal Patterns", "🍂", "season"), unsafe_allow_html=True)

    with col2:
        st.markdown(render_card("Time-Series Analysis", "🕒", "time"), unsafe_allow_html=True)
        st.markdown(render_card("AQI Category Analysis", "🟢", "cat"), unsafe_allow_html=True)
        st.markdown(render_card("Comparison Tool", "🔍", "comp"), unsafe_allow_html=True)

    st.markdown("---")

    # ----------------------------------------------------------
    # ROUTING TO SUBMODULE
    # ----------------------------------------------------------
    mode = st.session_state.eda_mode

    if mode == "Distribution Analysis":
        import pages.EDA_Distribution as pg
        pg.show()

    elif mode == "Time-Series Analysis":
        import pages.EDA_Timeseries as pg
        pg.show()

    elif mode == "Correlation Matrix":
        import pages.EDA_Correlation as pg
        pg.show()

    elif mode == "AQI Category Analysis":
        import pages.EDA_AQI_Category as pg
        pg.show()

    elif mode == "Seasonal Patterns":
        import pages.EDA_Seasonal as pg
        pg.show()

    elif mode == "Comparison Tool":
        import pages.EDA_Comparison as pg
        pg.show()
