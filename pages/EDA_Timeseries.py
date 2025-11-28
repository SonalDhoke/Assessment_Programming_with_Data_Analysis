import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------
# Darker Professional Colors
# ------------------------------------------
DARK_COLORS = px.colors.qualitative.Plotly

# ------------------------------------------
# Pastel CSS
# ------------------------------------------
st.markdown("""
<style>
.section-box {
    background-color: #F8FAFF;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E0E7FF;
    margin-bottom: 22px;
}

.plot-box {
    background: #ffffff;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 24px;
}
</style>
""", unsafe_allow_html=True)


def show():

    # ------------------- Load Data -----------------------
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
    elif "current_df" in st.session_state:
        df = st.session_state.current_df
    else:
        df = st.session_state.original_df

    if df is None:
        st.error("Dataset not found.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.header("📉 Time-Series Analysis (Normalized Option)")

    # ---------------- Detect pollutant columns ----------------
    exclude = {"City", "AQI", "AQI_Recalc", "AQI_Bucket", "AQI_Bucket_Recalc"}
    pollutant_cols = [
        c for c in df.columns
        if c not in exclude and pd.api.types.is_numeric_dtype(df[c])
    ]

    # ---------------- Filter Panel ----------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        pollutants = st.multiselect(
            "Select Pollutants (max 3)",
            pollutant_cols,
            max_selections=3
        )

    with col2:
        cities = st.multiselect(
            "Select Cities (max 3)",
            sorted(df["City"].unique()),
            max_selections=3
        )

    with col3:
        time_group = st.selectbox(
            "Group Data By",
            ["None", "Monthly", "Yearly", "Weekly"]
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Normalization toggle
    normalize = st.checkbox("🔄 Normalize (Min-Max: 0 → 1)", value=True)

    # ---------------- Validation ----------------
    if not pollutants:
        st.warning("Select at least one pollutant.")
        return

    if not cities:
        st.warning("Select at least one city.")
        return

    # ---------------- Apply City Filter ----------------
    df = df[df["City"].isin(cities)]

    # ---------------- Time Grouping ----------------
    if time_group == "Monthly":
        df["Month"] = df["Date"].dt.strftime("%Y-%m")
        group_var = "Month"

    elif time_group == "Yearly":
        df["Year"] = df["Date"].dt.year.astype(str)
        group_var = "Year"

    elif time_group == "Weekly":
        df["Week"] = df["Date"].dt.isocalendar().week.astype(int)
        group_var = "Week"

    else:
        group_var = "Date"

    # =====================================================
    # NORMALIZATION LOGIC
    # =====================================================
    if normalize:

        for pollutant in pollutants:
            min_val = df[pollutant].min()
            max_val = df[pollutant].max()
            df[f"norm_{pollutant}"] = (df[pollutant] - min_val) / (max_val - min_val)

        y_cols = [f"norm_{p}" for p in pollutants]
        y_label_suffix = " (Normalized)"
    else:
        y_cols = pollutants
        y_label_suffix = ""

    # =====================================================
    # SMART VISUALIZATION LOGIC
    # =====================================================

    # CASE 1: Single Pollutant + Multiple Cities → One chart
    if len(pollutants) == 1 and len(cities) > 1:

        pollutant = pollutants[0]
        y_col = y_cols[0]

        st.subheader(f"📊 {pollutant}{y_label_suffix} — Across Cities")

        fig = px.line(
            df,
            x=group_var,
            y=y_col,
            color="City",
            markers=False,
            color_discrete_sequence=DARK_COLORS,
            title=f"{pollutant}{y_label_suffix} Over Time"
        )

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title=pollutant + y_label_suffix
        )

        st.plotly_chart(fig, use_container_width=True)

    # CASE 2: Multiple Pollutants + Single City → One chart
    elif len(cities) == 1 and len(pollutants) > 1:

        city = cities[0]
        st.subheader(f"📊 {city} — Multiple Pollutants{y_label_suffix}")

        fig = px.line(
            df[df["City"] == city],
            x=group_var,
            y=y_cols,
            markers=False,
            color_discrete_sequence=DARK_COLORS,
            title=f"Pollutant Trends{y_label_suffix} — {city}"
        )

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Pollutant Level" + y_label_suffix
        )

        st.plotly_chart(fig, use_container_width=True)

    # CASE 3: Multiple Pollutants + Multiple Cities → Show all lines together (normalized makes it clean)
    else:

        st.subheader(f"📊 Combined View (Normalized: {normalize})")

        for pollutant, y_col in zip(pollutants, y_cols):

            st.markdown(f"### 🌈 {pollutant}{y_label_suffix}")

            fig = px.line(
                df,
                x=group_var,
                y=y_col,
                color="City",
                markers=False,
                color_discrete_sequence=DARK_COLORS,
                title=f"{pollutant}{y_label_suffix} — All Selected Cities"
            )

            fig.update_layout(
                xaxis_title="Time",
                yaxis_title=pollutant + y_label_suffix
            )

            st.markdown('<div class="plot-box">', unsafe_allow_html=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- Summary Table ----------------
    st.markdown("### 📌 Summary Statistics")
    summary = df.groupby("City")[pollutants].describe()
    st.dataframe(summary, use_container_width=True)
