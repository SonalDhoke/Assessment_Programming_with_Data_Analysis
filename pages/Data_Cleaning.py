import streamlit as st
import pandas as pd

def show():

    # -----------------------------------------
    # Load dataset ONCE using session_state
    # -----------------------------------------
    if "original_df" not in st.session_state:
        df = pd.read_csv("pages/AQI_combined_data.csv")
        st.session_state.original_df = df.copy()   # backup
        st.session_state.current_df = df.copy()    # working copy

    df = st.session_state.current_df

    st.title("🧹 Data Cleaning")

    st.write(
        """
        Below you can explore missing values, drop columns,
        and undo changes applied to the dataset.
        """
    )

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

    st.dataframe(missing_df, use_container_width=True)

    st.markdown("---")

    # -----------------------------------------
    # PART 2 — DROP COLUMN SECTION
    # -----------------------------------------
    st.subheader("🗑️ Drop Columns")

    # Tooltip / hover information icon
    st.markdown(
        """
        <span style="font-size:16px;">
        Select a column to drop 
        <span title="Recommendation: Drop columns with more than 50% missing values">ℹ️</span>
        </span>
        """,
        unsafe_allow_html=True
    )

    column_to_drop = st.selectbox(
        "Select a column to drop",
        options=df.columns,
        index=None,
        placeholder="Choose a column"
    )

    drop_clicked = st.button("Drop Column")

    if drop_clicked:
        if column_to_drop:
            st.session_state.current_df.drop(columns=[column_to_drop], inplace=True)
            st.success(f"✅ Column '{column_to_drop}' dropped successfully!")
        else:
            st.warning("⚠️ Please select a column first.")

    st.markdown("---")

    # -----------------------------------------
    # PART 3 — UNDO BUTTON
    # -----------------------------------------
    st.subheader("⏪ Undo Changes")

    if st.button("Undo All Changes"):
        st.session_state.current_df = st.session_state.original_df.copy()
        st.success("♻️ All changes undone! Dataset restored to original state.")

    # -----------------------------------------
    # Display current working dataframe
    # -----------------------------------------
    st.markdown("### 📄 Current Dataset Preview")
    st.dataframe(st.session_state.current_df, use_container_width=True)
