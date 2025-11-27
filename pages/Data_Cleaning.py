import streamlit as st
import pandas as pd
import plotly.express as px

def show():

    # -----------------------------------------
    # Load dataset ONCE using session_state
    # -----------------------------------------
    if "original_df" not in st.session_state:
        df = pd.read_csv("pages/AQI_combined_data.csv")
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

    # Sort descending by Missing %
    missing_df = missing_df.sort_values("Missing %", ascending=False)

    # Reset index to 1, 2, 3...
    missing_df.index = range(1, len(missing_df) + 1)
    missing_df.index.name = "No."

    st.dataframe(missing_df, use_container_width=True)

    # -----------------------------------------
    # PART 1B — MISSING VALUES HEATMAP (Compact)
    # -----------------------------------------
    with st.expander("📊 Show Missing Values Heatmap"):
        st.write("Visual representation of missing values by column:")

        # Convert df to True/False mask for missing values
        heatmap_data = df.isnull()

        # Plotly heatmap
        fig = px.imshow(
            heatmap_data.T,
            color_continuous_scale=["#1f77b4", "#ff4136"],  # blue vs red
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

    # Custom label with working hover tooltip
    st.markdown(
        """
        <span style="font-size:16px;">
            Select a column to drop 
            <span style="cursor: help;" title="Recommendation: Drop columns with more than 50% missing values">
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

    # Buttons side-by-side
    col1, col2 = st.columns([1, 1])

    with col1:
        drop_clicked = st.button("Drop Column", use_container_width=True)

    with col2:
        undo_clicked = st.button("Undo", use_container_width=True)

    # Drop logic
    if drop_clicked:
        if column_to_drop:
            st.session_state.current_df.drop(columns=[column_to_drop], inplace=True)
            st.success(f"✅ Column '{column_to_drop}' dropped successfully!")
        else:
            st.warning("⚠️ Please select a column first.")

    # Undo logic
    if undo_clicked:
        st.session_state.current_df = st.session_state.original_df.copy()
        st.success("♻️ Dataset restored to original state.")

    st.markdown("---")

    # -----------------------------------------
    # Current Dataset Preview
    # -----------------------------------------
    st.subheader("📄 Current Dataset Preview")
    st.dataframe(st.session_state.current_df, use_container_width=True)
