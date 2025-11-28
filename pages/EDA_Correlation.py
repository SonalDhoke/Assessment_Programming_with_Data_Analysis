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
    # City Filter
    # -----------------------------------------
    st.subheader("🏙️ Select City")

    cities = st.multiselect(
        "Choose one or more cities:",
        sorted(df["City"].dropna().unique()),
        max_selections=3
    )

    if cities:
        df = df[df["City"].isin(cities)]

    # -----------------------------------------
    # Pollutant Detection
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

    if len(pollutant_cols) < 2:
        st.error("Not enough pollutant columns to compute correlation.")
        return

    # -----------------------------------------
    # Correlation Type Selection (Pearson / Spearman)
    # -----------------------------------------
    corr_type = st.selectbox(
        "Correlation Method",
        ["Pearson", "Spearman"]
    )

    # -----------------------------------------
    # Compute Correlation Matrix
    # -----------------------------------------
    corr = df[pollutant_cols].corr(method=corr_type.lower())

    # -----------------------------------------
    # Heatmap (NO COLOR SCALE BAR)
    # -----------------------------------------
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )

    fig.update_traces(colorbar=None)

    fig.update_layout(
        title=f"{corr_type} Correlation Matrix (Pollutants Only)",
        xaxis_title="Pollutants",
        yaxis_title="Pollutants",
        margin=dict(l=30, r=30, t=50, b=30)
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------
    # Numeric Table
    # -----------------------------------------
    with st.expander("📄 Show Correlation Values"):
        st.dataframe(
            corr.style.background_gradient(cmap="RdBu_r"),
            use_container_width=True
        )
