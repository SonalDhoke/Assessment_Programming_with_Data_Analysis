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
        df["Date"] = pd.to_datetime(df["Date"])
        st.session_state.original_df = df.copy()   # Backup
        st.session_state.current_df = df.copy()    # Working copy

    df = st.session_state.current_df

    st.title("🧹 Data Cleaning")

    # -----------------------------------------
    # PART 1 — MISSING VALUES TABLE
    # -----------------------------------------
    st.subheader("📉 Missing Values (Column-wise)")

    missing_df = (
        df.isnull().sum()
        .reset_index()
        .rename(columns={"index": "Column", 0: "Missing Count"})
    )

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
    # PART 2 — DROP COLUMN SECTION
    # -----------------------------------------
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

    column_to_drop = st.selectbox(
        label="",
        options=df.columns,
        index=None,
        placeholder="Choose a column"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        drop_clicked = st.button("Drop Column", use_container_width=True)

    with col2:
        undo_clicked = st.button("Undo", use_container_width=True)

    if drop_clicked:
        if column_to_drop:
            st.session_state.current_df.drop(columns=[column_to_drop], inplace=True)
            st.success(f"✅ Column '{column_to_drop}' dropped successfully!")
        else:
            st.warning("⚠️ Please select a column first.")

    if undo_clicked:
        st.session_state.current_df = st.session_state.original_df.copy()
        st.success("♻️ Dataset restored to original state.")

    st.markdown("---")

    # -----------------------------------------
    # PART 4 — IMPUTATION SECTION
    # -----------------------------------------
    with st.expander("🧩 Impute Missing Values", expanded=False):

        st.write("Select columns and choose a fill method:")

        # -------- CHEMICAL GROUPS ---------
        chemical_groups = {
            "Nitrogen Oxides (NO, NO₂, NOx)": ["NO", "NO2", "NOx", "NO₂", "NOₓ"],
        }

        chem_choice = st.selectbox(
            "Select chemical group (optional):",
            ["None"] + list(chemical_groups.keys()),
            index=0
        )

        # -------- MULTISELECT --------
        col_selection = st.multiselect(
            "Select columns to impute:",
            options=df.columns,
            placeholder="Choose columns...",
            key="col_select"
        )

        # Auto-select chemical columns
        if chem_choice != "None":
            for col in chemical_groups[chem_choice]:
                if col in df.columns and col not in col_selection:
                    col_selection.append(col)
            st.session_state.col_select = col_selection

        # -------- CHIPS DISPLAY (visual only) --------
        chip_html = """
        <style>
        .chip-container { margin-top: 5px; }
        .chip {
            display:inline-block;
            padding:6px 12px;
            margin:4px;
            background-color:#ddecff;
            border-radius:12px;
            font-size:14px;
        }
        .chip .closebtn {
            margin-left:8px;
            color:#b30000;
            cursor:pointer;
            font-weight:bold;
        }
        </style>
        <div class="chip-container">
        """

        for c in col_selection:
            chip_html += f"""
            <span class="chip">{c} 
                <span class="closebtn" title="Remove from dropdown">✖</span>
            </span>
            """

        chip_html += "</div>"

        components.html(chip_html, height=120)

        # -------- METHOD --------
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

        # -------- FREQUENCY IF NEEDED --------
        freq_needed = method in ["Mean", "Median", "Mode", "Forward Fill"]
        freq = st.selectbox("Frequency:", ["Monthly", "Yearly"]) if freq_needed else None

        # -------- CHEMICAL TIP --------
        if any(c in col_selection for c in ["NO", "NO2", "NOx", "NO₂", "NOₓ"]):
            st.info(
                "💡 **Chemical Tip:**\n"
                "NOx ≈ NO + NO₂. Missing values can be estimated using:\n"
                "- **NOx = NO + NO₂**\n"
                "- **NO = NOx - NO₂**\n"
                "- **NO₂ = NOx - NO**\n"
                "⚠ Ensure units are consistent before using this relationship."
            )

        # -------- APPLY IMPUTATION --------
        if st.button("Apply Imputation"):
            if not col_selection:
                st.warning("⚠ Please select at least one column.")
            else:
                before_missing = df[col_selection].isnull().sum().sum()

                # ===== IMPUTATION LOGIC =====

                if method == "Mean":
                    for c in col_selection:
                        gr = df["Date"].dt.to_period("M") if freq == "Monthly" else df["Date"].dt.year
                        df[c] = df.groupby(gr)[c].transform(lambda x: x.fillna(x.mean()))

                elif method == "Median":
                    for c in col_selection:
                        gr = df["Date"].dt.to_period("M") if freq == "Monthly" else df["Date"].dt.year
                        df[c] = df.groupby(gr)[c].transform(lambda x: x.fillna(x.median()))

                elif method == "Mode":
                    for c in col_selection:
                        gr = df["Date"].dt.to_period("M") if freq == "Monthly" else df["Date"].dt.year
                        df[c] = df.groupby(gr)[c].transform(lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else x))

                elif method == "Forward Fill":
                    for c in col_selection:
                        gr = df["Date"].dt.to_period("M") if freq == "Monthly" else df["Date"].dt.year
                        df[c] = df.groupby(gr)[c].ffill()

                elif method == "Interpolate (City + Date)":
                    df.set_index("Date", inplace=True)
                    for c in col_selection:
                        df[c] = df.groupby("City")[c].apply(lambda x: x.interpolate())
                    df.reset_index(inplace=True)

                elif method == "Interpolate (Date)":
                    df.set_index("Date", inplace=True)
                    df[col_selection] = df[col_selection].interpolate()
                    df.reset_index(inplace=True)

                elif method == "Monthly Median":
                    for c in col_selection:
                        df[c] = df.groupby(df["Date"].dt.to_period("M"))[c].transform(lambda x: x.fillna(x.median()))

                st.session_state.current_df = df

                after_missing = df[col_selection].isnull().sum().sum()

                st.success(
                    f"✨ Imputation applied successfully!\n"
                    f"Missing before: **{before_missing}** → after: **{after_missing}**"
                )

    # -----------------------------------------
    # Current Dataset Preview
    # -----------------------------------------
    st.subheader("📄 Current Dataset Preview")
    st.dataframe(st.session_state.current_df, use_container_width=True)
