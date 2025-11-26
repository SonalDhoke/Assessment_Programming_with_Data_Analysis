import streamlit as st
import pandas as pd
import io

def show():

    # ----------------------------
    # Load Dataset (Internal)
    # ----------------------------
    try:
        df = pd.read_csv("pages/AQI_combined_data.csv")   # <-- Update path if needed
    except FileNotFoundError:
        st.error("❌ Could not find file: `pages/AQI_combined_data.csv`. "
                 "Please check the path or upload the file.")
        return

    total_rows = df.shape[0]

    # ----------------------------
    # Page Styling (SAFE, STABLE CSS)
    # ----------------------------
    st.markdown("""
        <style>

            /* ---------------- HEADERS ---------------- */
            .section-header {
                font-size: 28px !important;
                font-weight: 700 !important;
                color: #344767 !important;
                margin-top: 25px !important;
                margin-bottom: 10px !important;
            }

            .sub-header {
                font-size: 22px !important;
                font-weight: 600 !important;
                color: #4A6480 !important;
                margin-top: 20px !important;
                margin-bottom: 10px !important;
            }

            /* ---------------- BOX STYLING ---------------- */
            .pastel-box {
                background-color: #F7F9FC;
                padding: 18px;
                border-radius: 12px;
                border: 1px solid #E3EAF4;
                margin-bottom: 20px;
                font-size: 16px;
                line-height: 1.55;
                color: #3A4A66;
            }

            .info-text {
                font-family: monospace;
                font-size: 15px;
                white-space: pre-wrap;
            }

            /* ---------------- RADIO BUTTON STYLING ----------------
               Use data-testid and role, which are more stable in recent Streamlit
            -------------------------------------------------------- */

            [data-testid="stRadio"] > div {
                display: flex;
                flex-direction: row;      /* horizontal layout */
                gap: 10px;
                flex-wrap: wrap;
            }

            [data-testid="stRadio"] div[role="radio"] {
                border: 1px solid #E3EAF4;
                padding: 8px 14px;
                border-radius: 10px;
                background-color: #FFFFFF;
                transition: 0.2s ease;
                font-size: 16px;
                color: #3A4A66;
            }

            [data-testid="stRadio"] div[role="radio"]:hover {
                background-color: #f0f4fa;
                border-color: #cfd8e3;
            }

            [data-testid="stRadio"] div[role="radio"][aria-checked="true"] {
                background-color: #d8e8ff !important;
                border-color: #a7c4ff !important;
                color: #2a3a55 !important;
                font-weight: 600 !important;
            }

        </style>
    """, unsafe_allow_html=True)

    # ----------------------------
    # Title
    # ----------------------------
    st.markdown("<div class='section-header'>📘 Dataset Information</div>", unsafe_allow_html=True)

    # ----------------------------
    # Dataset Description
    # ----------------------------
    st.markdown("""
    <div class="pastel-box">
        This page provides a high-level overview of the dataset used for AQI analysis.
        You can explore the top/bottom rows, dataset structure, column data types, and
        basic descriptive statistics.  
        <br><br>
        Detailed cleaning and preprocessing will be performed in the Data Cleaning page.
    </div>
    """, unsafe_allow_html=True)

    # ===============================================================
    # 🔍 VIEW ROWS SECTION
    # ===============================================================
    st.markdown("<div class='sub-header'>🔍 View Dataset Rows</div>", unsafe_allow_html=True)

    view_option = st.radio(
        "Select how to display rows:",
        ["Show first rows", "Show last rows"],
        horizontal=True
    )

    num_rows = st.number_input(
        f"Enter number of rows to display (max {total_rows}):",
        min_value=1,
        max_value=int(total_rows),
        value=5
    )

    if view_option == "Show first rows":
        st.dataframe(df.head(num_rows), use_container_width=True)
    else:
        st.dataframe(df.tail(num_rows), use_container_width=True)

    # ----------------------------
    # Dataset Structure
    # ----------------------------
    st.markdown("<div class='sub-header'>📄 Dataset Structure</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='pastel-box'>
        🔹 <b>Total Rows:</b> {df.shape[0]} <br>
        🔹 <b>Total Columns:</b> {df.shape[1]} <br>
        🔹 <b>Column Names:</b> {', '.join(df.columns)} 
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------
    # Data Types Table
    # ----------------------------
    st.markdown("<div class='sub-header'>🔠 Column Data Types</div>", unsafe_allow_html=True)

    dtype_df = (
        pd.DataFrame(df.dtypes, columns=["Data Type"])
        .reset_index()
        .rename(columns={"index": "Column"})
    )
    st.dataframe(dtype_df, use_container_width=True)

    # ----------------------------
    # df.info() Block
    # ----------------------------
    st.markdown("<div class='sub-header'>🧠 Dataset Info (df.info)</div>", unsafe_allow_html=True)

    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()

    st.markdown(f"<div class='pastel-box info-text'>{info_str}</div>", unsafe_allow_html=True)

    # ===============================================================
    # 📊 Statistical Summary
    # ===============================================================
    st.markdown("<div class='sub-header'>📊 Statistical Summary</div>", unsafe_allow_html=True)

    # Use plain describe to avoid any Styler rendering issues
    desc = df.describe(include="all", datetime_is_numeric=True)
    st.dataframe(desc, use_container_width=True)
