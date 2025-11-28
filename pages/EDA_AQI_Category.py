import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------------------------
# CSS Styling
# ----------------------------------------------------------
st.markdown("""
<style>
.section-box {
    background-color: #F8FAFF;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #E0E7FF;
    margin-bottom: 25px;
}

.plot-box {
    background: #FFFFFF;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------------
def show():

    # Load dataset
    df = None
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
    elif "current_df" in st.session_state:
        df = st.session_state.current_df
    elif "original_df" in st.session_state:
        df = st.session_state.original_df

    if df is None:
        st.error("Dataset not available.")
        return

    st.header("🌫️ AQI Category Comparison (Before vs After Cleaning)")

    # ----------------------------------------------------------
    # FILTER PANEL
    # ----------------------------------------------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    cities = st.multiselect(
        "Select Cities (optional)",
        sorted(df["City"].dropna().unique())
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_df = df.copy()
    if cities:
        filtered_df = filtered_df[filtered_df["City"].isin(cities)]

    if filtered_df.empty:
        st.warning("No data available for selected cities.")
        return

    # ----------------------------------------------------------
    # MAPPING FOR GOOD COLORS
    # ----------------------------------------------------------
    aqi_colors = {
        "Good": "#4CAF50",
        "Satisfactory": "#8BC34A",
        "Moderate": "#FFEB3B",
        "Poor": "#FF9800",
        "Very Poor": "#F44336",
        "Severe": "#B71C1C"
    }

    # ----------------------------------------------------------
    # FIX — Convert value_counts output to consistent columns
    # ----------------------------------------------------------
    def prepare_vc(series, name):
        """
        Ensures the output always has:
        name | count
        """
        vc = series.value_counts().reset_index()
        vc.columns = [name, "count"]
        return vc

    # BEFORE
    vc_before = prepare_vc(filtered_df["AQI_Bucket"], "AQI_Bucket")

    # AFTER
    vc_after = prepare_vc(filtered_df["AQI_Bucket_Recalc"], "AQI_Bucket_Recalc")

    # ----------------------------------------------------------
    # SIDE-BY-SIDE PLOTS
    # ----------------------------------------------------------
    col_before, col_after = st.columns(2)

    # ------------------ BEFORE CLEANING --------------------
    with col_before:
        st.markdown("### 🟡 Before Cleaning (AQI_Bucket)")
        st.markdown('<div class="plot-box">', unsafe_allow_html=True)

        fig1 = px.bar(
            vc_before,
            x="AQI_Bucket",
            y="count",
            text="count",
            color="AQI_Bucket",
            color_discrete_map=aqi_colors
        )
        fig1.update_traces(textposition="outside")
        fig1.update_layout(
            xaxis_title="AQI Category",
            yaxis_title="Count",
            height=450
        )

        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ AFTER CLEANING --------------------
    with col_after:
        st.markdown("### 🟢 After Cleaning (AQI_Bucket_Recalc)")
        st.markdown('<div class="plot-box">', unsafe_allow_html=True)

        fig2 = px.bar(
            vc_after,
            x="AQI_Bucket_Recalc",
            y="count",
            text="count",
            color="AQI_Bucket_Recalc",
            color_discrete_map=aqi_colors
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(
            xaxis_title="AQI Category",
            yaxis_title="Count",
            height=450
        )

        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------------------------------------
    # RAW DATA EXPANDER
    # ----------------------------------------------------------
    with st.expander("📄 View Underlying Data"):
        st.dataframe(filtered_df, use_container_width=True)
