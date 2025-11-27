import streamlit as st
import pandas as pd
import plotly.express as px


# ------------------------ CHIP RENDERER --------------------------
def render_chips(selected, key_prefix):
    """Displays selected columns as pills with remove buttons."""
    if not selected:
        return None

    st.write("### Selected Columns")
    cols = st.columns(len(selected))
    removed = None

    for i, col in enumerate(selected):
        with cols[i]:
            st.markdown(f"**{col}**")
            if st.button("✖", key=f"{key_prefix}_{col}", help="Remove this column"):
                removed = col

    return removed


# ---------------------------- MAIN PAGE ---------------------------
def show():

    # --------------------------------------------------------------
    # LOAD DATA ONCE
    # --------------------------------------------------------------
    if "original_df" not in st.session_state:
        df = pd.read_csv("pages/AQI_combined_data.csv")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        st.session_state.original_df = df.copy()
        st.session_state.current_df = df.copy()

    df = st.session_state.current_df

    # Always ensure clean Date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.title("🧹 Data Cleaning")

    # ==============================================================
    # PART 1 — MISSING VALUES TABLE
    # ==============================================================
    st.subheader("📉 Missing Values (Column-wise)")

    missing_df = df.isnull().sum().reset_index()
    missing_df.columns = ["Column", "Missing Count"]
    missing_df["Missing %"] = (missing_df["Missing Count"] / len(df)) * 100
    missing_df["Missing %"] = missing_df["Missing %"].round(2)
    missing_df = missing_df.sort_values("Missing %", ascending=False)
    missing_df.index = range(1, len(missing_df) + 1)
    missing_df.index.name = "No."

    st.dataframe(missing_df, use_container_width=True)

    # ==============================================================
    # PART 1B — HEATMAP
    # ==============================================================
    with st.expander("📊 Show Missing Values Heatmap"):
        heatmap_data = df.isnull()
        fig = px.imshow(
            heatmap_data.T,
            color_continuous_scale=["#1f77b4", "#ff4136"],
            aspect="auto",
            labels=dict(x="Row", y="Column", color="Missing"),
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ==============================================================
    # PART 2 — DROP COLUMN
    # ==============================================================
    st.subheader("🗑️ Drop Columns")

    st.markdown("""
        <span style="font-size:16px;">
            Select a column to drop 
            <span style="cursor: help;" title="Recommendation: Drop columns with >50% missing values">
                &#9432;
            </span>
        </span>
    """, unsafe_allow_html=True)

    column_to_drop = st.selectbox(
        "",
        options=df.columns,
        index=None,
        placeholder="Choose a column to drop"
    )

    c1, c2 = st.columns(2)
    with c1:
        drop_clicked = st.button("Drop Column", use_container_width=True)
    with c2:
        undo_clicked = st.button("Undo All Changes", use_container_width=True)

    if drop_clicked:
        if column_to_drop:
            st.session_state.current_df.drop(columns=[column_to_drop], inplace=True)
            st.success(f"🗑️ Column '{column_to_drop}' dropped successfully!")
            st.rerun()
        else:
            st.warning("⚠️ Please select a column.")

    if undo_clicked:
        st.session_state.current_df = st.session_state.original_df.copy()
        st.success("♻️ Dataset restored to original state.")
        st.rerun()

    st.markdown("---")

    # ==============================================================
    # PART 3 — IMPUTATION
    # ==============================================================
    with st.expander("🧩 Impute Missing Values", expanded=False):

        st.write("Select columns and choose a fill method:")

        # ---- Only show columns that still have NaN ----
        # missing_cols = df.columns[df.isnull().sum() > 0].tolist()
        # Columns that still have missing values (EXCLUDING AQI columns)
        excluded_cols = ["AQI", "AQI_Bucket", "AQI_Bucket_Recalc", "AQI_Recalc"]
        
        missing_cols = [
            col for col in df.columns
            if col not in excluded_cols and df[col].isnull().sum() > 0
        ]


        if not missing_cols:
            st.success("🎉 All columns have been cleaned! No missing values left.")
            col_selection = []
        else:
            col_selection = st.multiselect(
                "Select columns to impute:",
                options=missing_cols,
                placeholder="Choose columns...",
                key="impute_columns"
            )

        # Chips for removal
        removed = render_chips(col_selection, key_prefix="chip")
        if removed:
            col_selection.remove(removed)
            st.session_state.impute_columns = col_selection
            st.rerun()

        # ---- Imputation Methods ----
        imputation_options = [
            "Mean",
            "Median",
            "Mode",
            "Forward Fill",
            "Interpolate (City + Date)",
            "Interpolate (Date)",
            "Monthly Median"
        ]

        # Add chemical formula option if relevant
        nitrogen_cols = {"NO", "NO2", "NOx", "NO₂", "NOₓ"}
        if any(c in col_selection for c in nitrogen_cols):
            imputation_options.append("Fill Using Chemical Formula (NO + NO₂ = NOx)")

        method = st.selectbox("Choose imputation method:", imputation_options)

        # Frequency for some methods
        freq_needed = method in ["Mean", "Median", "Mode", "Forward Fill"]
        freq = st.selectbox("Frequency:", ["Monthly", "Yearly"]) if freq_needed else None

        # ---- Chemical Tip ----
        if any(c in col_selection for c in nitrogen_cols):
            st.info("""
                💡 **Chemical Tip:**  
                NOx = NO + NO₂  
                Missing values can be computed as:
                • NOx = NO + NO₂  
                • NO = NOx − NO₂  
                • NO₂ = NOx − NO  
            """)

        # ======================================================
        # APPLY IMPUTATION
        # ======================================================
        if st.button("Apply Imputation"):
            if not col_selection:
                st.warning("⚠️ Select at least one column.")
            else:
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

                before = df[col_selection].isnull().sum().rename("Before")

                # ---------- IMPUTATION METHODS ----------
                if method in ["Mean", "Median", "Mode"]:
                    for c in col_selection:
                        group_key = df["Date"].dt.to_period("M") if freq == "Monthly" else df["Date"].dt.year
                        if method == "Mean":
                            df[c] = df.groupby(group_key)[c].transform(lambda x: x.fillna(x.mean()))
                        elif method == "Median":
                            df[c] = df.groupby(group_key)[c].transform(lambda x: x.fillna(x.median()))
                        elif method == "Mode":
                            df[c] = df.groupby(group_key)[c].transform(
                                lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else x)
                            )

                elif method == "Forward Fill":
                    for c in col_selection:
                        group_key = df["Date"].dt.to_period("M") if freq == "Monthly" else df["Date"].dt.year
                        df[c] = df.groupby(group_key)[c].ffill()

                elif method == "Interpolate (City + Date)":
                    df = df.sort_values(["City", "Date"]).reset_index(drop=True)
                    for c in col_selection:
                        if pd.api.types.is_numeric_dtype(df[c]):
                            df[c] = df.groupby("City")[c].transform(lambda x: x.interpolate())

                elif method == "Interpolate (Date)":
                    df = df.sort_values("Date")
                    for c in col_selection:
                        df[c] = df[c].interpolate()

                elif method == "Monthly Median":
                    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                    monthly_key = df["Date"].dt.to_period("M")
                    for c in col_selection:
                        df[c] = df.groupby(monthly_key)[c].transform(lambda x: x.fillna(x.median()))

                elif method == "Fill Using Chemical Formula (NO + NO₂ = NOx)":
                    rename_map = {"NO₂": "NO2", "NOₓ": "NOx", "NOX": "NOx"}
                    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

                    if {"NO", "NO2", "NOx"}.issubset(df.columns):
                        mask = df["NOx"].isnull() & df["NO"].notnull() & df["NO2"].notnull()
                        df.loc[mask, "NOx"] = df.loc[mask, "NO"] + df.loc[mask, "NO2"]

                        mask = df["NO"].isnull() & df["NOx"].notnull() & df["NO2"].notnull()
                        df.loc[mask, "NO"] = df.loc[mask, "NOx"] - df.loc[mask, "NO2"]

                        mask = df["NO2"].isnull() & df["NOx"].notnull() & df["NO"].notnull()
                        df.loc[mask, "NO2"] = df.loc[mask, "NOx"] - df.loc[mask, "NO"]

                # ---------- RESULTS ----------
                after = df[col_selection].isnull().sum().rename("After")
                summary = pd.concat([before, after], axis=1)

                st.success("✨ Imputation applied successfully!")
                st.dataframe(summary, use_container_width=True)

                st.session_state.current_df = df

    st.markdown("---")
    # ==============================================================
    # PART — RECALCULATE AQI AFTER IMPUTATION
    # ==============================================================
    st.markdown("---")
    st.subheader("🌬️ Recalculate AQI Based on Updated Pollutant Values")
    
    st.info("""
    After filling missing pollutant values, recalculate AQI and AQI category.
    This will create two new columns:
    - **AQI_Recalc**
    - **AQI_Bucket_Recalc**
    """)
    
    if st.button("Recalculate AQI"):
        df = st.session_state.current_df
    
        # ---------------- AQI BREAKPOINTS (CPCB) ----------------
        breakpoints = {
            "PM2.5": [(0,30,0,50),(31,60,51,100),(61,90,101,200),(91,120,201,300),(121,250,301,400),(251,500,401,500)],
            "PM10": [(0,50,0,50),(51,100,51,100),(101,250,101,200),(251,350,201,300),(351,430,301,400),(431,600,401,500)],
            "NO2":  [(0,40,0,50),(41,80,51,100),(81,180,101,200),(181,280,201,300),(281,400,301,400),(401,1000,401,500)],
            "SO2":  [(0,40,0,50),(41,80,51,100),(81,380,101,200),(381,800,201,300),(801,1600,301,400),(1601,2000,401,500)],
            "CO":   [(0,1,0,50),(1.1,2,51,100),(2.1,10,101,200),(10.1,17,201,300),(17.1,34,301,400),(34.1,50,401,500)],
            "O3":   [(0,50,0,50),(51,100,51,100),(101,168,101,200),(169,208,201,300),(209,748,301,400),(749,1000,401,500)],
        }
    
        pollutants_available = [p for p in breakpoints.keys() if p in df.columns]
    
        # -------------- Function to compute sub-index --------------
        def compute_subindex(value, bp_list):
            if pd.isna(value):
                return None
            for (Clow, Chigh, Ilow, Ihigh) in bp_list:
                if Clow <= value <= Chigh:
                    return ((Ihigh - Ilow) / (Chigh - Clow)) * (value - Clow) + Ilow
            return None
    
        # -------------- Compute AQI --------------
        subindex_df = pd.DataFrame()
    
        for pollutant in pollutants_available:
            subindex_df[pollutant] = df[pollutant].apply(lambda x: compute_subindex(x, breakpoints[pollutant]))
    
        df["AQI_Recalc"] = subindex_df.max(axis=1)
    
        # -------------- Category Labels --------------
        def aqi_bucket(aqi):
            if pd.isna(aqi): return None
            if aqi <= 50: return "Good"
            if aqi <= 100: return "Satisfactory"
            if aqi <= 200: return "Moderate"
            if aqi <= 300: return "Poor"
            if aqi <= 400: return "Very Poor"
            return "Severe"
    
        df["AQI_Bucket_Recalc"] = df["AQI_Recalc"].apply(aqi_bucket)
    
        st.success("✅ AQI successfully recalculated!")
    
        st.dataframe(df[["AQI_Recalc", "AQI_Bucket_Recalc"]], use_container_width=True)
    
        # update session_state
        st.session_state.current_df = df
    

    # ==============================================================
    # PART 4 — DATE COLUMN CREATION
    # ==============================================================
    st.subheader("📆 Create Date-Based Columns (Optional)")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    date_options = st.multiselect(
        "Select fields to create:",
        ["Year", "Month Number", "Month Name", "Day", "Week Number"],
        placeholder="Choose..."
    )

    if st.button("Create Date Columns"):
        if not date_options:
            st.warning("⚠️ Select at least one.")
        else:
            if "Year" in date_options:
                df["Year"] = df["Date"].dt.year.astype("Int64")
            if "Month Number" in date_options:
                df["Month_Number"] = df["Date"].dt.month.astype("Int64")
            if "Month Name" in date_options:
                df["Month_Name"] = df["Date"].dt.strftime("%B")
            if "Day" in date_options:
                df["Day"] = df["Date"].dt.day.astype("Int64")
            if "Week Number" in date_options:
                df["Week_Number"] = df["Date"].dt.isocalendar().week.astype(int)

            st.success("🎉 Date-based columns created!")
            st.session_state.current_df = df

    # ==============================================================
    # PREVIEW
    # ==============================================================
    st.subheader("📄 Current Dataset Preview")
    st.dataframe(st.session_state.current_df, use_container_width=True)
