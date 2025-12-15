import streamlit as st
import pandas as pd
import plotly.express as px


def show():

    st.title("🤖 AQI Prediction using LightGBM")

    # =====================================================
    # LOAD DATA
    # =====================================================
    if "cleaned_df" not in st.session_state:
        st.error("Cleaned dataset not found. Complete data cleaning first.")
        return

    df = st.session_state.cleaned_df.copy()

    # =====================================================
    # LOAD REGRESSION MODEL (FROM app.py)
    # =====================================================
    reg_model = st.session_state.reg_model

    # 🔥 Get feature order DIRECTLY from model
    feature_cols = reg_model.feature_name_

    # =====================================================
    # BASIC FEATURE ENGINEERING (NO FITTING)
    # =====================================================
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.month

    df["Season"] = df["Month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Summer", 4: "Summer", 5: "Summer",
        6: "Monsoon", 7: "Monsoon", 8: "Monsoon",
        9: "Post-Monsoon", 10: "Post-Monsoon", 11: "Post-Monsoon"
    })

    # =====================================================
    # RECREATE ENCODING (CONSISTENT ENOUGH)
    # =====================================================
    from sklearn.preprocessing import LabelEncoder

    city_encoder = LabelEncoder()
    season_encoder = LabelEncoder()

    df["City_Code"] = city_encoder.fit_transform(df["City"])
    df["Season_Code"] = season_encoder.fit_transform(df["Season"])

    # =====================================================
    # POLLUTANT INPUTS
    # =====================================================
    exclude_cols = [
        "AQI", "AQI_Recalc", "AQI_Bucket", "AQI_Bucket_Recalc",
        "City", "Date", "Season", "Month_Name",
        "Week", "Week_No", "Week_Number",
        "City_Code", "Season_Code", "Month"
    ]

    pollutants = [
        col for col in df.columns
        if col not in exclude_cols
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    # =====================================================
    # USER INPUT
    # =====================================================
    st.subheader("🔮 Predict AQI")

    user_input = {}
    cols = st.columns(3)

    for i, p in enumerate(pollutants):
        with cols[i % 3]:
            user_input[p] = st.number_input(
                p,
                float(df[p].min()),
                float(df[p].max()),
                float(df[p].mean())
            )

    city = st.selectbox("City", sorted(df["City"].unique()))
    month = st.number_input("Month", 1, 12, 6)

    season = df[df["City"] == city]["Season"].mode().iloc[0]

    city_code = city_encoder.transform([city])[0]
    season_code = season_encoder.transform([season])[0]

    # =====================================================
    # BUILD INPUT DF (MATCH MODEL FEATURES)
    # =====================================================
    input_df = pd.DataFrame([{
        **user_input,
        "City_Code": city_code,
        "Month": month,
        "Season_Code": season_code
    }])

    input_df = input_df.reindex(columns=feature_cols).fillna(0)

    # =====================================================
    # PREDICTION
    # =====================================================
    if st.button("Predict AQI"):
        pred_aqi = reg_model.predict(input_df)[0]
        st.info(f"🌫 **Predicted AQI:** {pred_aqi:.2f}")

    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================
    st.subheader("🔍 Feature Importance")

    importance_df = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": reg_model.feature_importances_
    }).sort_values("Importance", ascending=False)

    fig = px.bar(
        importance_df,
        x="Feature",
        y="Importance",
        title="LightGBM Feature Importance"
    )

    st.plotly_chart(fig, use_container_width=True)
