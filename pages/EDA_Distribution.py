import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ----------------------------------------------------------
# Lightweight KDE using ONLY NumPy
# ----------------------------------------------------------
def gaussian_kde_numpy(data, num_points=200):
    """
    Gaussian KDE using NumPy only.
    Safe for Streamlit Cloud.
    """
    data = np.asarray(data)
    data = data[~np.isnan(data)]

    if len(data) < 2:
        return None, None

    xmin, xmax = data.min(), data.max()
    x_vals = np.linspace(xmin, xmax, num_points)

    # Scott's rule
    bandwidth = 1.06 * data.std() * (len(data) ** -0.2)
    bandwidth = max(bandwidth, 1e-8)

    densities = np.zeros_like(x_vals)

    for d in data:
        densities += np.exp(-0.5 * ((x_vals - d) / bandwidth) ** 2)

    densities /= (len(data) * bandwidth * np.sqrt(2 * np.pi))

    return x_vals, densities


# ----------------------------------------------------------
# Pastel CSS
# ----------------------------------------------------------
st.markdown("""
<style>
.section-box {
    background-color: #F8FAFF;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E0E7FF;
    margin-bottom: 20px;
}

.plot-container {
    border-radius: 15px;
    padding: 12px;
    background: #ffffff;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------
# MAIN FUNCTION
# ----------------------------------------------------------
def show():

    # ------------------- Load Data -----------------------
    df = None
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df
    elif "current_df" in st.session_state:
        df = st.session_state.current_df
    else:
        df = st.session_state.original_df

    if df is None:
        st.error("Dataset not available.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.header("📈 Distribution Analysis")

    # ------------------- Detect Pollutants --------------
    exclude = {
        "City", "AQI", "AQI_Bucket", "AQI_Recalc",
        "AQI_Bucket_Recalc", "Year", "Month_Name", "Week"
    }

    pollutant_cols = [
        c for c in df.columns
        if c not in exclude and pd.api.types.is_numeric_dtype(df[c])
    ]

    # ------------------- Filter Panel ---------------------
    st.markdown('<div class="section-box">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        pollutant = st.selectbox("Select Pollutant", pollutant_cols)

    with col2:
        cities = st.multiselect(
            "Filter by City (optional)",
            sorted(df["City"].dropna().unique())
        )

    with col3:
        time_group = st.selectbox(
            "Group Data By",
            ["None", "Yearly", "Monthly", "Weekly"],
            index=0
        )

    outliers = st.checkbox("Highlight Outliers", value=False)

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------- Apply City Filter -------------------
    filtered_df = df.copy()
    if cities:
        filtered_df = filtered_df[filtered_df["City"].isin(cities)]

    # --------------------- Time Grouping Logic -------------------
    if time_group == "Yearly":
        filtered_df["Year"] = filtered_df["Date"].dt.year.astype(str)
        grouped_df = filtered_df.groupby("Year")[pollutant].mean().reset_index()
        x_col = "Year"

    elif time_group == "Monthly":
        filtered_df["Month"] = filtered_df["Date"].dt.month
        filtered_df["Month_Name"] = filtered_df["Date"].dt.strftime("%B")

        month_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        grouped_df = (
            filtered_df.groupby("Month_Name")[pollutant]
            .mean()
            .reindex(month_order)
            .reset_index()
        )

        grouped_df = grouped_df.dropna().reset_index(drop=True)
        x_col = "Month_Name"

    elif time_group == "Weekly":
        filtered_df["Week"] = filtered_df["Date"].dt.isocalendar().week.astype(int)
        grouped_df = filtered_df.groupby("Week")[pollutant].mean().reset_index()
        x_col = "Week"

    else:
        grouped_df = filtered_df.copy()
        x_col = pollutant

    if grouped_df.empty:
        st.warning("No data available for selected filters.")
        return

    # --------------------- Visualization Section -------------------
    st.markdown("### 📊 Distribution Visualizations")

    col_hist, col_box = st.columns([2, 1])

    # ------------ Histogram / Bar Plot ------------
    with col_hist:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        if time_group == "None":
            fig = px.histogram(
                grouped_df,
                x=x_col,
                nbins=40,
                opacity=0.6,
                color_discrete_sequence=["#A7C4FF"]
            )
            fig.update_layout(
                title=f"Distribution of {pollutant}",
                xaxis_title=pollutant,
                yaxis_title="Frequency"
            )

            # ----------- KDE Curve -----------
            show_kde = st.checkbox("Show KDE Curve", value=True)

            if show_kde:
                data = grouped_df[x_col].dropna().values

                x_vals, kde_vals = gaussian_kde_numpy(data)

                if x_vals is not None:
                    y_scaled = kde_vals * max(fig.data[0].y) / max(kde_vals)

                    fig.add_scatter(
                        x=x_vals,
                        y=y_scaled,
                        mode='lines',
                        name="KDE Curve",
                        line=dict(color="#FF7F7F", width=3)
                    )

        else:
            fig = px.bar(
                grouped_df,
                x=x_col,
                y=pollutant,
                color_discrete_sequence=["#A7C4FF"],
                title=f"{pollutant} - {time_group} Average"
            )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------ Box Plot ------------
    with col_box:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)

        fig2 = px.box(
            grouped_df,
            x=x_col if time_group != "None" else None,
            y=pollutant,
            points="all" if outliers else False,
            color_discrete_sequence=["#FFB3C6"],
            title=f"{pollutant} Distribution ({time_group})"
        )

        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- Summary Statistics ------------------
    st.markdown("### 📌 Summary Statistics")

    stats_df = grouped_df.describe().T
    st.dataframe(stats_df, use_container_width=True)
