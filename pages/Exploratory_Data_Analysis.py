import streamlit as st

# ----------------------------------------------------------
# CUSTOM CSS — PASTEL BUTTONS
# ----------------------------------------------------------
st.markdown("""
<style>

.eda-btn {
    padding: 16px;
    margin: 8px 0;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    border: 2px solid transparent;
    text-align: center;
    transition: 0.2s;
}

.dist   { background: #FFEAEA; border-color: #FFCCCC; }
.time   { background: #FFF4D6; border-color: #FFE4A1; }
.corr   { background: #E8FFF3; border-color: #B9F5D0; }
.cat    { background: #E9F2FF; border-color: #A7C4FF; }
.season { background: #F5E8FF; border-color: #D6B6FF; }
.comp   { background: #FFF0F5; border-color: #FFC4D6; }

/* Hover */
.eda-btn:hover {
    opacity: 0.85;
    transform: scale(1.02);
}

/* Active */
.active {
    border: 3px solid #4A90E2 !important;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# MAIN PAGE LOGIC
# ----------------------------------------------------------
def show():
    st.title("📊 Exploratory Data Analysis")

    df = st.session_state.get("cleaned_df", None)
    if df is None:
        st.warning("⚠️ Please clean dataset first.")
        return

    # Store selected EDA mode
    if "eda_mode" not in st.session_state:
        st.session_state.eda_mode = "Distribution Analysis"

    st.markdown("### Choose an analysis module:")

    # ----------------------------------------------------------
    # BUTTON COLUMNS (HTML + form submit for clicking)
    # ----------------------------------------------------------
    col1, col2 = st.columns(2)

    # Mapping: label → (css_class, icon)
    eda_options = {
        "Distribution Analysis": ("dist", "📈"),
        "Time-Series Analysis": ("time", "🕒"),
        "Correlation Matrix": ("corr", "🔗"),
        "AQI Category Analysis": ("cat", "🟢"),
        "Seasonal Patterns": ("season", "🍂"),
        "Comparison Tool": ("comp", "🔍"),
    }

    # Render buttons
    with col1:
        for label in ["Distribution Analysis", "Correlation Matrix", "Seasonal Patterns"]:
            css, icon = eda_options[label]

            is_active = "active" if st.session_state.eda_mode == label else ""

            with st.form(f"form_{label}"):
                clicked = st.form_submit_button(
                    "",
                    help=f"Open {label}"
                )
                if clicked:
                    st.session_state.eda_mode = label

                st.markdown(
                    f"<div class='eda-btn {css} {is_active}'>{icon} {label}</div>",
                    unsafe_allow_html=True
                )

    with col2:
        for label in ["Time-Series Analysis", "AQI Category Analysis", "Comparison Tool"]:
            css, icon = eda_options[label]

            is_active = "active" if st.session_state.eda_mode == label else ""

            with st.form(f"form_{label}"):
                clicked = st.form_submit_button(
                    "",
                    help=f"Open {label}"
                )
                if clicked:
                    st.session_state.eda_mode = label

                st.markdown(
                    f"<div class='eda-btn {css} {is_active}'>{icon} {label}</div>",
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # ----------------------------------------------------------
    # ROUTING TO ACTUAL EDA MODULE
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
