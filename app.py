import streamlit as st
import pandas as pd
import io

def show():

    # ----------------------------
    # Load Dataset (Internal)
    # ----------------------------
    df = pd.read_csv("pages/AQI_combined_data.csv")   # <-- Update path if needed
    total_rows = df.shape[0]

    # ----------------------------
    # Page Styling (Updated CSS)
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

            /* ---------------- RADIO BUTTON STYLING (NEW STREAMLIT) ---------------- */

            .stRadio > div {
                flex-direction: row !important;  /* horizontal layout */
                gap: 12px !important;
            }

            .stRadio label {
                border: 1px solid #E3EAF4 !important;
                pa
