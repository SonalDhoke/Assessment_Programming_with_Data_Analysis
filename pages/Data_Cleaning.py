import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

def show():

    # -----------------------------------------
    # Load dataset ONCE using session_state
    # -----------------------------------------
    if "original_df" not in st.session_state:
        df = pd.read_csv("pages/AQI_combined_data.csv")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        st.session_state.original_df = df.copy()
        st.session_state.current_df = df.copy()

    df = st.session_state.current_df

    st.title("🧹 Data Cleaning")

    # -----------------------------------------
    # PART 1 — Missing Values Table
    # -----------------------------------------
    st.subheader("📉 Missing Values (Column-wise)")

    missing_df = df.isnull().sum().reset_index()
    missing_df.columns = ["Column", "Missing Count"]
    missing_df["Missing %"] = (missing_df["Missing Count"] / len(df)) * 100
    missing_df["Missing %"] = missing_df["Missing %"].round(2)
    missing_df = missing_df.sort_values("Missing %", ascending=False)
    missing_df.index = range(1, len(missing_df) + 1)
    missing_df.index.name = "No."

    st.dataframe(missing_df, use_container_width=True)

    # -----------------------------------------
    # PART 1B — Heatmap
    # -----------------------------------------
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

    # -----------------------------------------
    # PART 2 — Drop Column
    # -----------------------------------------
    st.subheader("🗑️ Drop Columns")

    st.markdown("""
        <span style="font-size:16px;">
            Select a column to drop 
            <span style="cursor: help;" title="Recommendation: Drop columns with > 50% missing values">
                &#9432;
            </span>
        </span>
    """, unsafe_allow_html=True)

    column_to_drop = st.selectbox("", options=df.columns, index=None, placeholder="Choose a column")

    col1, col2 = st.columns(2)

    with col1:
        drop_clicked = st.button("Drop Column", use_container_width=True)

    with col2:
        undo_clicked = st.button("Undo All Changes", use_container_width=True)

    if drop_clicked:
        if column_to_drop:
            st.session_state.current_df.drop(columns=[column_to_drop], inplace=True)
            st.success(f"🗑️ Column '{column_to_drop}' dropped successfully!")
        else:
            st.warning("⚠️ Select a column first.")

    if undo_clicked:
        st.session_state.current_df = st.session_state.original_df.copy()
        st.success("♻️ Dataset restored to original state.")

    st.markdown("---")

    # -----------------------------------------
    # PART 3 — Imputation Section
    # -----------------------------------------
    with st.expander("🧩 Impute Missing Values", expanded=False):

        st.write("Select columns and choose a fill method:")

        # ----- Chemical Group Auto-Selection -----
        chemical_groups = {
            "Nitrogen Oxides (NO, NO₂, NOx)": ["NO", "NO2", "NOx", "NO₂", "NOₓ"],
        }

        chem_choice = st.selectbox(
            "Select chemical group (optional):",
            ["None"] + list(chemical_groups.keys()),
            index=0
        )

        # ----- Column Multiselect -----
        col_selection = st.multiselect(
            "Select columns to impute:",
            options=df.columns,
            placeholder="Choose columns...",
            key="impute_columns"
        )

        # Auto-add chemical columns
        if chem_choice != "None":
            for c in chemical_groups[chem_choice]:
                if c in df.columns and c not in col_selection:
                    col_selection.append(c)
            st.session_state.impute_columns = col_selection

        # ----- Chip Display -----
        chip_html = """
        <style>
        .chip-container { margin-top: 8px; }
        .chip {
            display:inline-block;
            padding:6px 12px;
            margin:4px;
            background-color:#ddecff;
            border-radius:12px;
            font-size:14px;
        }
        </style>
        <div class='chip-container'>
        """

        for c in col_selection:
            chip_html += f"<span class='chip'>{c}</span>"

        chip_html += "</div>"
        components.html(chip_html, height=120)

        # ----- Method Selection -----
        method = st.selectbox(
            "Choose imputation method:",
            [
                "Mean",
                "Median",
                "Mode",
                "Forward Fill",
                "Interpolate (City + Date)",
                "Interpolate (Date)",
                "Monthly Median",
            ]
        )

        freq_needed = method in ["Mean", "Median", "Mode", "Forward Fill"]
        freq = st.selectbox("Frequency:", ["Monthly", "Yearly"]) if freq_needed else None

        # ----- Chemical Tips -----
        if any(c in col_selection for c in ["NO", "NO2", "NOx", "NO₂", "NOₓ"]):
            st.info("""
                💡 **Chemical Tip:**  
                NOx ≈ NO + NO₂  
                You can fill missing values using:
                - NOx = NO + NO₂  
                - NO = NOx − NO₂  
                - NO₂ = NOx − NO  
                ⚠ Ensure units are consistent.
            """)

        # ----- Apply Imputation -----
        if st.button("Apply Imputation"):
            if not col_selection:
                st.warning("⚠️ Select at least one column.")
            else:

                # GUARANTEE Date stays datetime
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

                # BEFORE COUNTS
                before = df[col_selection].isnull().sum().rename("Before")

                # ========== IMPUTATION METHODS ==========
                if method in ["Mean", "Median", "Mode"]:
                    for c in col_selection:
                        if freq == "Monthly":
                            grp = df["Date"].dt.to_period("M")
                        else:
                            grp = df["Date"].dt.year

                        if method == "Mean":
                            df[c] = df.groupby(grp)[c].transform(lambda x: x.fillna(x.mean()))

                        elif method == "Median":
                            df[c] = df.groupby(grp)[c].transform(lambda x: x.fillna(x.median()))

                        elif method == "Mode":
                            df[c] = df.groupby(grp)[c].transform(lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else x))

                elif method == "Forward Fill":
                    for c in col_selection:
                        if freq == "Monthly":
                            grp = df["Date"].dt.to_period("M")
                        else:
                            grp = df["Date"].dt.year
                        df[c] = df.groupby(grp)[c].ffill()

                elif method == "Interpolate (City + Date)":
                    for c in col_selection:
                        df = df.sort_values(["City", "Date"])
                        df[c] = df.groupby("City")[c].apply(lambda x: x.interpolate())

                elif method == "Interpolate (Date)":
                    df = df.sort_values("Date")
                    for c in col_selection:
                        df[c] = df[c].interpolate()

                elif method == "Monthly Median":
                    for c in col_selection:
                        df[c] = df.groupby(df["Date"].dt.to_period("M"))[c].transform(lambda x: x.fillna(x.median()))

                # AFTER COUNTS
                after = df[col_selection].isnull().sum().rename("After")

                result_df = pd.concat([before, after], axis=1)

                st.session_state.current_df = df

                st.success("✨ Imputation applied successfully!")
                st.dataframe(result_df, use_container_width=True)

    # -----------------------------------------
    # Current Dataset Preview
    # -----------------------------------------
    st.subheader("📄 Current Dataset Preview")
    st.dataframe(st.session_state.current_df, use_container_width=True)
