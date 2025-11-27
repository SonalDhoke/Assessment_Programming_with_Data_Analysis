import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --------------------- CPCB BREAKPOINTS (for thresholds) ---------------------
CPCB_BREAKPOINTS = {
    "PM2.5": [(0, 30), (31, 60), (61, 90), (91, 120), (121, 250), (251, 500)],
    "PM10":  [(0, 50), (51, 100), (101, 250), (251, 350), (351, 430), (431, 600)],
    "NO2":   [(0, 40), (41, 80), (81, 180), (181, 280), (281, 400), (401, 1000)],
    "SO2":   [(0, 40), (41, 80), (81, 380), (381, 800), (801, 1600), (1601, 2000)],
    "CO":    [(0, 1), (1.1, 2), (2.1, 10), (10.1, 17), (17.1, 34), (34.1, 50)],
    "O3":    [(0, 50), (51, 100), (101, 168), (169, 208), (209, 748), (749, 1000)],
}

CPCB_CATEGORIES = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]


# ------------------------ PASTEL COLOR HELPER ------------------------
def get_pastel_color(name: str) -> str:
    """Return a soft pastel color for a given pollutant name."""
    preset = {
        "PM2.5": "#A7C7E7",   # pastel blue
        "PM10":  "#F7D1BA",   # pastel peach
        "NO2":   "#E7BFE7",   # pastel purple
        "SO2":   "#F5E1A4",   # pastel yellow
        "CO":    "#B8E0D2",   # pastel mint
        "O3":    "#FFCBDD",   # pastel pink,
        "NOx":   "#D6CDEA",
    }
    if name in preset:
        return preset[name]

    # Generate a pastel color from the name (hash → HSL → hex)
    # Simple deterministic hash
    h = abs(hash(name)) % 360
    s = 0.35  # low saturation for pastel
    l = 0.80  # high lightness for pastel

    # Convert HSL to RGB
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if h < 60:
        r1, g1, b1 = c, x, 0
    elif h < 120:
        r1, g1, b1 = x, c, 0
    elif h < 180:
        r1, g1, b1 = 0, c, x
    elif h < 240:
        r1, g1, b1 = 0, x, c
    elif h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x

    r = int((r1 + m) * 255)
    g = int((g1 + m) * 255)
    b = int((b1 + m) * 255)

    return f"#{r:02x}{g:02x}{b:02x}"


# ------------------------ MAIN PAGE FUNCTION ------------------------
def show():
    st.title("📊 Pollutant Distribution Analysis")
    st.caption("Interactive, pastel-themed distribution explorer for all pollutants present after cleaning.")

    # -----------------------------------------------------------------
    # 1. GET CLEANED DATA
    # -----------------------------------------------------------------
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df.copy()
    elif "current_df" in st.session_state:
        df = st.session_state.current_df.copy()
    else:
        # Fallback – load the base file (same as cleaning page)
        df = pd.read_csv("pages/AQI_combined_data.csv")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    if df.empty:
        st.warning("The dataset appears to be empty. Please complete data cleaning first.")
        return

    # -----------------------------------------------------------------
    # 2. DETECT POLLUTANT COLUMNS (NUMERIC, EXCLUDING META / AQI)
    # -----------------------------------------------------------------
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    exclude_cols = [
        "AQI", "AQI_Bucket", "AQI_Recalc", "AQI_Bucket_Recalc",
        "Year", "Month_Number", "Day", "Week_Number",
        "Latitude", "Longitude"
    ]
    # Also exclude any obvious id / index columns if present
    exclude_cols += ["id", "ID", "Index"]

    pollutant_cols = [c for c in numeric_cols if c not in exclude_cols]

    if not pollutant_cols:
        st.warning("No numeric pollutant columns found after cleaning.")
        return

    # -----------------------------------------------------------------
    # 3. SIDEBAR / CONTROL PANEL
    # -----------------------------------------------------------------
    st.sidebar.header("⚙️ Distribution Controls")

    pollutant = st.sidebar.selectbox("Select pollutant", pollutant_cols)

    bins = st.sidebar.slider("Number of bins", min_value=5, max_value=80, value=30, step=1)

    show_kde = st.sidebar.checkbox("Show smooth density curve (KDE-like)", value=True)
    remove_outliers = st.sidebar.checkbox("Remove outliers (IQR method)", value=False)
    show_thresholds = st.sidebar.checkbox(
        "Show CPCB concentration breakpoints (if available)",
        value=True
    )

    box_violin_mode = st.sidebar.radio(
        "Box / Violin plot",
        ["Boxplot", "Violin", "Both"],
        index=0
    )

    color = get_pastel_color(pollutant)

    # -----------------------------------------------------------------
    # 4. PREPARE DATA (OPTIONAL OUTLIER REMOVAL)
    # -----------------------------------------------------------------
    series = df[pollutant].dropna()

    original_count = len(series)

    if remove_outliers and not series.empty:
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        series = series[(series >= lower) & (series <= upper)]

    filtered_count = len(series)

    if series.empty:
        st.warning(f"No valid data points available for **{pollutant}** after filtering.")
        return

    # -----------------------------------------------------------------
    # 5. SUMMARY CARDS
    # -----------------------------------------------------------------
    st.subheader(f"📈 Distribution for: `{pollutant}`")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Mean", f"{series.mean():.2f}")
    with c2:
        st.metric("Median", f"{series.median():.2f}")
    with c3:
        st.metric("Std. Deviation", f"{series.std():.2f}")

    c4, c5, c6 = st.columns(3)
    with c4:
        st.metric("Min", f"{series.min():.2f}")
    with c5:
        st.metric("Max", f"{series.max():.2f}")
    with c6:
        info_text = f"{filtered_count} / {original_count}"
        st.metric("Used points", info_text)

    st.markdown("---")

    # -----------------------------------------------------------------
    # 6. HISTOGRAM + OPTIONAL DENSITY CURVE
    # -----------------------------------------------------------------
    st.markdown("### 📊 Histogram")

    fig = go.Figure()

    # Histogram
    fig.add_trace(
        go.Histogram(
            x=series,
            nbinsx=bins,
            name=pollutant,
            marker=dict(color=color, line=dict(width=0)),
            opacity=0.75
        )
    )

    # KDE-like density curve (using normalized histogram as proxy)
    if show_kde and len(series) > 1:
        counts, bin_edges = np.histogram(series, bins=bins, density=True)
        bin_centers = 0.5 * (bin_edges[0:-1] + bin_edges[1:])
        fig.add_trace(
            go.Scatter(
                x=bin_centers,
                y=counts,
                mode="lines",
                name="Density",
                line=dict(width=3, color=color)
            )
        )

    # CPCB breakpoints (if pollutant is in dictionary)
    if show_thresholds and pollutant in CPCB_BREAKPOINTS:
        bp_list = CPCB_BREAKPOINTS[pollutant]
        pastel_band_colors = [
            "rgba(167,199,231,0.15)",  # Good
            "rgba(184,224,210,0.15)",  # Satisfactory
            "rgba(245,225,164,0.15)",  # Moderate
            "rgba(247,209,186,0.15)",  # Poor
            "rgba(231,191,231,0.15)",  # Very Poor
            "rgba(255,203,221,0.15)",  # Severe
        ]

        for (i, (low, high)) in enumerate(bp_list):
            band_color = pastel_band_colors[i] if i < len(pastel_band_colors) else "rgba(0,0,0,0.05)"
            fig.add_vrect(
                x0=low,
                x1=high,
                fillcolor=band_color,
                line_width=0,
                opacity=1,
                annotation_text=CPCB_CATEGORIES[i],
                annotation_position="top left",
                annotation_font_size=10,
                annotation_font_color="#555555"
            )

    fig.update_layout(
        bargap=0.05,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#f9fafb",
        xaxis_title=f"{pollutant} concentration",
        yaxis_title="Count",
        legend_title="Legend",
        margin=dict(l=40, r=20, t=40, b=40),
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------------------------------
    # 7. BOX / VIOLIN PLOTS
    # -----------------------------------------------------------------
    st.markdown("### 🎻 Box / Violin Plot")

    # Prepare dataframe for plotly (just one column but easier to extend later)
    plot_df = pd.DataFrame({pollutant: series})

    if box_violin_mode in ["Boxplot", "Both"]:
        fig_box = go.Figure()
        fig_box.add_trace(
            go.Box(
                y=plot_df[pollutant],
                name=pollutant,
                boxpoints="outliers",
                marker=dict(color=color),
            )
        )
        fig_box.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#f9fafb",
            yaxis_title=pollutant,
            margin=dict(l=40, r=20, t=40, b=40),
        )
        st.plotly_chart(fig_box, use_container_width=True)

    if box_violin_mode in ["Violin", "Both"]:
        fig_violin = go.Figure()
        fig_violin.add_trace(
            go.Violin(
                y=plot_df[pollutant],
                name=pollutant,
                box_visible=True,
                meanline_visible=True,
                line=dict(color="#666666", width=1),
                fillcolor=color,
                opacity=0.7,
            )
        )
        fig_violin.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#f9fafb",
            yaxis_title=pollutant,
            margin=dict(l=40, r=20, t=40, b=40),
        )
        st.plotly_chart(fig_violin, use_container_width=True)

    # -----------------------------------------------------------------
    # 8. SMALL NOTE
    # -----------------------------------------------------------------
    st.info(
        "This section uses **all numeric pollutant columns available after cleaning**. "
        "Controls on the left let you change bins, remove outliers, show density curves, "
        "and overlay CPCB concentration ranges where applicable."
    )
