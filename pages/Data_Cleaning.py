import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# ------------------------ CHIP RENDERER --------------------------
def render_chips(selected, key_prefix):
    """Displays selected columns as pills + removable buttons."""
    st.write("### Selected Columns")

    if not selected:
        st.info("No columns selected.")
        return None

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

    # --------------------------------------------------------------
    # ALWAYS KEEP DATE CLEAN
    # --------------------------------------------------------------
    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        if isinstance(df.index, pd.DatetimeIndex):
            df.reset_index(inplace=True, drop=True)
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.title("🧹 Data Cleaning")

    # ==============================================================
    # PART 1 — Missing Values Table
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
    # PART 1B — Heatmap
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
    # PART 2 — Drop Column
    # ==============================================================
    st.subheader("🗑️ Drop Columns")

    st.markdown(
        """
        <span style="font-size:16px;">
            Select a column to drop 
            <span style="cursor: help;" title="Recommendation: Drop columns with > 50% missing values">
                &#9432;
            </span>
        </span>
        """,
        unsafe_allow_html=True
    )

    column_to_drop = st.selectbox("", options=df.columns, index=None, placeholder="Choose a column")

    c1, c2 = st.columns(2)
    with c1:
        drop_clicked = st.button("Drop Column", use_container_width=True)
    with c2:
        undo_clicked = st.button("Undo All Changes", use_container_width=True)

    if drop_clicked:
        if column_to_drop:
            st.session_state.current_df.drop(columns=[column_to_drop], inplace=True)
            st.success(f"🗑️ Column '{column_to_drop}' dropped successfully!")
            st.experimental_rerun()
        else:
            st.warning("⚠️ Select a column.")

    if undo_clicked:
        st.session_state.current_df = st.session_state.original_df.copy()
        st.success("♻️ Dataset restored to original state.")
        st.experimental_rerun()

    st.markdown("---")

    # ==============================================================
    # PART 3 — IMPUTATION
    # ==============================================================
    with st.expander("🧩 Impute Missing Values", expanded=False):

        st.write("Select columns and choose a fill method:")

        col_selection = st.multiselect(
            "Select columns to impute:",
            options=df.columns,
            placeholder="Choose columns...",
            key="impute_columns"
        )

        removed = render_chips(col_selection, key_prefix="chip")
        if removed:
            col_selection.remove(removed)
            st.session_state.impute_columns = col_selection
            st.experimental_rerun()

        imputation_options = [
            "Mean",
            "Median",
            "Mode",
            "Forward Fill",
            "Interpolate (City + Date)",
            "Interpolate (Date)",
            "Monthly Median"
        ]

        nitrogen_cols = {"NO", "NO2", "NOx", "NO₂", "NOₓ"}

        if any(c in nitrogen_cols for c in col_selection):
            imputation_options.append("Fill Using Chemical Formula (NO + NO₂ = NOx)")

        method = st.selectbox("Choose imputation method:", imputation_options)

        freq_needed = method in ["Mean", "Median", "Mode", "Forward Fill"]
        freq = st.selectbox("Frequency:", ["Monthly", "Yearly"]) if freq_needed else None

        if any(c in col_selection for c in nitrogen_cols):
            st.info("""
                💡 **Chemical Tip:**  
                NOx ≈ NO + NO₂  
                Missing values can be estimated using:
                • NOx = NO + NO₂  
                • NO = NOx − NO₂  
                • NO₂ = NOx − NO  
            """)

        if st.button("Apply Imputation"):
            if not col_selection:
                st.warning("⚠️ Select at least one column.")
            else:

                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

                before = df[col_selection].isnull().sum().rename("Before")

                # ---------------- APPLY IMPUTATION ----------------
                if method in ["Mean", "Median", "Mode"]:
                    for c in col_selection:
                        grp = df["Date"].dt.to_period("M") if freq == "Monthly" else df["Date"].dt.year
                        if method == "Mean":
                            df[c] = df.groupby(grp)[c].transform(lambda x: x.fillna(x.mean()))
                        elif method == "Median":
                            df[c] = df.groupby(grp)[c].transform(lambda x: x.fillna(x.median()))
                        elif method == "Mode":
                            df[c] = df.groupby(grp)[c].transform(lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else x))

                elif method == "Forward Fill":
                    for c in col_selection:
                        grp = df["Date"].dt.to_period("M") if freq == "Monthly" else df["Date"].dt.year
                        df[c] = df.groupby(grp)[c].ffill()

                elif method == "Interpolate (City + Date)":
                    df = df.sort_values(["City", "Date"])
                    for c in col_selection:
                        df[c] = df.groupby("City")[c].apply(lambda x: x.interpolate())

                elif method == "Interpolate (Date)":
                    df = df.sort_values("Date")
                    for c in col_selection:
                        df[c] = df[c].interpolate()

                elif method == "Monthly Median":

                    # 🚑 FIX: Ensure Date is truly datetime before using dt accessor
                    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                
                    # 🚑 FIX: Drop rows where Date became NaT (only temporarily during imputation)
                    if df["Date"].isnull().any():
                        st.warning("⚠️ Some rows had invalid dates and were skipped during monthly imputation.")
                        df = df[df["Date"].notnull()]
                
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

                after = df[col_selection].isnull().sum().rename("After")
                summary = pd.concat([before, after], axis=1)

                st.success("✨ Imputation applied successfully!")
                st.dataframe(summary, use_container_width=True)

                st.session_state.current_df = df
                st.experimental_rerun()

    st.markdown("---")

    # ==============================================================
    # PART 4 — DATE-BASED COLUMN CREATION
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
                months = [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ]
                df["Month_Name"] = pd.Categorical(df["Month_Name"], categories=months, ordered=True)

            if "Day" in date_options:
                df["Day"] = df["Date"].dt.day.astype("Int64")

            if "Week Number" in date_options:
                df["Week_Number"] = df["Date"].dt.isocalendar().week.astype(int)

            st.success("🎉 Date-based columns created!")
            st.session_state.current_df = df
            st.experimental_rerun()

    # ==============================================================
    # CURRENT DATASET PREVIEW
    # ==============================================================
    st.subheader("📄 Current Dataset Preview")
    st.dataframe(st.session_state.current_df, use_container_width=True)
