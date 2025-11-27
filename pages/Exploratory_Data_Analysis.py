import streamlit as st
import pandas as pd

# ----------------------------------------------------------
# Pastel CSS for buttons
# ----------------------------------------------------------
st.markdown("""
<style>

.eda-btn {
    padding: 18px;
    margin: 10px 0;
    text-align: center;
    border-radius: 12px;
    font-size: 20px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.25s;
    border: 1px solid #E0E4EB;
}

/* Button colors */
.dist   { background: #FFEAEA; border-color: #FFCCCC; }
.time   { background: #FFF4D6; border-color: #FFE4A1; }
.corr   { background: #E8FFF3; border-color: #B9F5D0; }
.cat    { background: #E9F2FF; border-color: #A7C4FF; }
.season { background: #F5E8FF; border-color: #D6B6FF; }
.comp   { background: #FFF0F5; border-color: #FFC4D6; }

/* Hover effects */
.eda-btn:hover {
    opacity: 0.85;
    transform: scale(1.02);
}

/* Active selection */
.active {
    border: 3px solid #4A90E2 !important;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# PAGE LOGIC
# ----------------------------------------------------------

def show():
    st.title("📊 Exploratory Data Analysis")

    # Load cleaned data
    df = st.session_state.get("cleaned_df", None)

    if df is None:
        st.warning("⚠️ Please clean the dataset first using the **Data Cleaning** page.")
        return

    # Create session variable to store selected EDA module
    if "eda_mode" not in st.session_state:
        st.session_state.eda_mode = "Distribution Analysis"

    st.markdown("### Choose an analysis module:")

    # ----------------------------------------------------------
    # BUTTON LAYOUT
    # ----------------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📈 Distribution Analysis", key="dist_btn"):
            st.session_state.eda_mode = "Distribution Analysis"
        st.markdown(
            f"<div class='eda-btn dist {'active' if st.session_state.eda_mode=='Distribution Analysis' else ''}'>📈 Distribution Analysis</div>",
            unsafe_allow_html=True
        )

        if st.button("🔗 Correlation Matrix", key="corr_btn"):
            st.session_state.eda_mode = "Correlation Matrix"
        st.markdown(
            f"<div class='eda-btn corr {'active' if st.session_state.eda_mode=='Correlation Matrix' else ''}'>🔗 Correlation Matrix</div>",
            unsafe_allow_html=True
        )

        if st.button("🍂 Seasonal Patterns", key="season_btn"):
            st.session_state.eda_mode = "Seasonal Patterns"
        st.markdown(
            f"<div class='eda-btn season {'active' if st.session_state.eda_mode=='Seasonal Patterns' else ''}'>🍂 Seasonal Patterns</div>",
            unsafe_allow_html=True
        )

    with col2:
        if st.button("🕒 Time-Series Analysis", key="time_btn"):
            st.session_state.eda_mode = "Time-Series Analysis"
        st.markdown(
            f"<div class='eda-btn time {'active' if st.session_state.eda_mode=='Time-Series Analysis' else ''}'>🕒 Time-Series Analysis</div>",
            unsafe_allow_html=True
        )

        if st.button("🟢 AQI Category Analysis", key="cat_btn"):
            st.session_state.eda_mode = "AQI Category Analysis"
        st.markdown(
            f"<div class='eda-btn cat {'active' if st.session_state.eda_mode=='AQI Category Analysis' else ''}'>🟢 AQI Category Analysis</div>",
            unsafe_allow_html=True
        )

        if st.button("🔍 Comparison Tool", key="comp_btn"):
            st.session_state.eda_mode = "Comparison Tool"
        st.markdown(
            f"<div class='eda-btn comp {'active' if st.session_state.eda_mode=='Comparison Tool' else ''}'>🔍 Comparison Tool</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ----------------------------------------------------------
    # ROUTE TO SELECTED SUBPAGE
    # ----------------------------------------------------------
    mode = st.session_state.eda_mode

    if mode == "Distribution Analysis":
        import pages.EDA_Distribution as pg
        pg.show(df)

    elif mode == "Time-Series Analysis":
        import pages.EDA_Timeseries as pg
        pg.show(df)

    elif mode == "Correlation Matrix":
        import pages.EDA_Correlation as pg
        pg.show(df)

    elif mode == "AQI Category Analysis":
        import pages.EDA_AQI_Category as pg
        pg.show(df)

    elif mode == "Seasonal Patterns":
        import pages.EDA_Seasonal as pg
        pg.show(df)

    elif mode == "Comparison Tool":
        import pages.EDA_Comparison as pg
        pg.show(df)
