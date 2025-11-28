import streamlit as st
import pandas as pd
import plotly.express as px

def show():

    # Load cleaned dataset
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
    else:
        df = st.session_state.current_df

    st.header("📘 Correlation Matrix (Pollutants Only)")

    # -----------------------------------------
    # 1) Detect pollutant columns only
    # -----------------------------------------
    exclude = {
        "City", "Date", "AQI", "AQI_Recalc",
        "AQI_Bucket", "AQI_Bucket_Recalc",
        "Year", "Month", "Month_Number", "Month_Name",
        "Week_Number", "Day"
    }

    pollutant_cols = [
        col for col in df.columns
        if col not in exclude and pd.api.types.is_numeric_dtype(df[col])
    ]

    if not pollutant_cols:
        st.error("No numeric pollutant columns found for correlation.")
        return

    # -----------------------------------------
    # 2) Correlation Type Selection
    # -----------------------------------------
    corr_type = st.radio(
        "Select Correlation Method",
        ["Pearson", "Spearman", "Kendall"],
        horizontal=True
    )

    # -----------------------------------------
    # 3) Compute Correlation Matrix
    # -----------------------------------------
    corr = df[pollutant_cols].corr(method=corr_type.lower())

    # -----------------------------------------
    # 4) Plot Heatmap (NO COLOR SCALE BAR)
    # -----------------------------------------
    fig = px.imshow(
        corr,
        text_auto=True,            # shows values inside squares
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )

    fig.update_traces(colorbar=None)  # ❌ remove color scale legend

    fig.update_layout(
        title=f"{corr_type} Correlation (Pollutants Only)",
        xaxis_title="Pollutants",
        yaxis_title="Pollutants",
        margin=dict(l=30, r=30, t=60, b=30)
    )

    # Make diagonal squares slightly darker for contrast
    fig.update_xaxes(side="bottom")

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------
    # 5) Show underlying correlation table
    # -----------------------------------------
    with st.expander("Show Numeric Correlation Table"):
        st.dataframe(corr.style.background_gradient(cmap="RdBu_r"), use_container_width=True)
