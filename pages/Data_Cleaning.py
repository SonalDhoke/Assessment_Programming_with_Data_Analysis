import streamlit as st
import pandas as pd

def show():

    # ----------------------------
    # Load Dataset (Internal)
    # ----------------------------
    df = pd.read_excel("AQI_combined_data.csv")   # <-- Update name if needed
    total_rows = df.shape[0]

    # ----------------------------
    # Page Styling
    # ----------------------------
    st.markdown("""
        <style>

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

        </style>
    """, unsafe_allow_html=True)

    # ----------------------------
    # Title
    # ----------------------------
    st.markdown("<div class='section-header'>📘 Dataset Overview</div>", unsafe_allow_html=True)

    # ----------------------------
    # Dataset Description
    # ----------------------------
    st.markdown("""
    <div class="pastel-box">
        This page provides an initial overview of the dataset used for AQI analysis.
        You can preview rows, inspect dataset structure, and review basic statistics.
        Cleaning, missing values, and transformations will be handled in the next page.
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------
    # Row Selection Section
    # ----------------------------
    st.markdown("<div class='sub-header'>🔍 View Dataset Rows</div>", unsafe_allow_html=True)

    view_option = st.radio(
        "Select how to display rows:",
        ["Show first rows", "Show last rows"],
        horizontal=True
    )

    num_rows = st.number_input(
        f"Enter number of rows to display (max {total_rows}):",
        min_value=1,
        max_value=total_rows,
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
    # Data Types
    # ----------------------------
    st.markdown("<div class='sub-header'>🔠 Column Data Types</div>", unsafe_allow_html=True)

    dtype_df = pd.DataFrame(df.dtypes, columns=["Data Type"]).reset_index().rename(columns={"index": "Column"})
    st.dataframe(dtype_df, use_container_width=True)

    # ----------------------------
    # df.info()
    # ----------------------------
    st.markdown("<div class='sub-header'>🧠 Dataset Info (df.info)</div>", unsafe_allow_html=True)

    buffer = []
    df.info(buf=buffer.append)
    info_str = "".join(buffer)

    st.markdown(f"<div class='pastel-box info-text'>{info_str}</div>", unsafe_allow_html=True)

    # ----------------------------
    # df.describe()
    # ----------------------------
    st.markdown("<div class='sub-header'>📊 Statistical Summary (describe)</div>", unsafe_allow_html=True)
    st.dataframe(df.describe(), use_container_width=True)
