import streamlit as st

def show():
    st.title("📊 Exploratory Data Analysis")

    # Use cleaned data if available
    df = st.session_state.get("cleaned_df")
    if df is None:
        st.warning("⚠️ Please clean the dataset first on the **Data Cleaning** page.")
        return

    # ----------------------------------------------------------
    # Simple pastel styling for ALL buttons on this page
    # ----------------------------------------------------------
    st.markdown(
        """
        <style>
        div.stButton > button {
            width: 100%;
            border-radius: 12px;
            border: 1px solid #A7C4FF;
            background-color: #E9F2FF;
            color: #344767;
            padding: 0.6rem 1rem;
            font-size: 16px;
            font-weight: 500;
        }
        div.stButton > button:hover {
            background-color: #D5E4FF;
            border-color: #7CA4FF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Remember which module is selected
    if "eda_mode" not in st.session_state:
        st.session_state.eda_mode = "Distribution Analysis"

    st.subheader("Choose an analysis module:")

    col1, col2 = st.columns(2)

    # LEFT COLUMN BUTTONS
    with col1:
        if st.button("📈 Distribution Analysis"):
            st.session_state.eda_mode = "Distribution Analysis"

        if st.button("🔗 Correlation Matrix"):
            st.session_state.eda_mode = "Correlation Matrix"

        if st.button("🍂 Seasonal Patterns"):
            st.session_state.eda_mode = "Seasonal Patterns"

    # RIGHT COLUMN BUTTONS
    with col2:
        if st.button("🕒 Time-Series Analysis"):
            st.session_state.eda_mode = "Time-Series Analysis"

        if st.button("🟢 AQI Category Analysis"):
            st.session_state.eda_mode = "AQI Category Analysis"

        if st.button("🔍 Comparison Tool"):
            st.session_state.eda_mode = "Comparison Tool"

    st.markdown(f"**Selected module:** `{st.session_state.eda_mode}`")
    st.markdown("---")

    # ----------------------------------------------------------
    # ROUTE TO THE SELECTED EDA SUBPAGE
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
