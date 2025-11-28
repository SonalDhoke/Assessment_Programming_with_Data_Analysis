import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, accuracy_score
import plotly.express as px

def show():

    st.title("🤖 Machine Learning – AQI Prediction")

    # Load Data
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df.copy()
    else:
        st.error("Cleaned dataset not found. Please complete data cleaning first.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    
    # Feature Engineering
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day

    # Remove rows with missing pollutant data
    df = df.dropna()

    pollutants = [
        col for col in df.columns 
        if col not in ["AQI", "AQI_Bucket", "AQI_Recalc", "AQI_Bucket_Recalc", 
                       "City", "Date", "Month_Name"] 
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    # Encode City
    enc = LabelEncoder()
    df["City_Code"] = enc.fit_transform(df["City"])

    # -----------------------------------------------------------
    # REGRESSION MODEL – Predict AQI
    # -----------------------------------------------------------
    st.subheader("📈 Predict Numerical AQI")

    X_reg = df[pollutants + ["City_Code", "Year", "Month"]]
    y_reg = df["AQI_Recalc"]

    X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)

    reg_model = RandomForestRegressor(n_estimators=150, random_state=42)
    reg_model.fit(X_train, y_train)
    y_pred_reg = reg_model.predict(X_test)

    reg_accuracy = r2_score(y_test, y_pred_reg)
    st.success(f"Regression Model R² Score: **{reg_accuracy:.3f}**")

    # User input for prediction
    st.markdown("### 🔮 Predict AQI from pollutant values")

    user_input = {}
    for p in pollutants:
        user_input[p] = st.slider(p, float(df[p].min()), float(df[p].max()), float(df[p].mean()))

    city_choice = st.selectbox("Select City", sorted(df["City"].unique()))
    month_choice = st.number_input("Month", min_value=1, max_value=12, value=6)

    city_code = enc.transform([city_choice])[0]

    input_df = pd.DataFrame([{
        **user_input,
        "City_Code": city_code,
        "Year": 2024,
        "Month": month_choice
    }])

    predicted_aqi = reg_model.predict(input_df)[0]

    st.info(f"### 🌫 Predicted AQI: **{predicted_aqi:.2f}**")


    # -----------------------------------------------------------
    # CLASSIFICATION MODEL – Predict AQI Category
    # -----------------------------------------------------------
    st.subheader("🏷 Predict AQI Category")

    df = df[df["AQI_Bucket_Recalc"].notna()]  # ensure no missing labels

    X_clf = df[pollutants + ["City_Code", "Year", "Month"]]
    y_clf = df["AQI_Bucket_Recalc"]

    X_train, X_test, y_train, y_test = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=150, random_state=42)
    clf.fit(X_train, y_train)

    y_pred_clf = clf.predict(X_test)
    clf_acc = accuracy_score(y_test, y_pred_clf)

    st.success(f"Classification Model Accuracy: **{clf_acc:.3f}**")

    predicted_bucket = clf.predict(input_df)[0]

    st.info(f"### 🏷 AQI Category Prediction: **{predicted_bucket}**")

    # -----------------------------------------------------------
    # FEATURE IMPORTANCE
    # -----------------------------------------------------------
    st.subheader("🔍 Feature Importance")

    importance_df = pd.DataFrame({
        "Feature": X_reg.columns,
        "Importance": reg_model.feature_importances_
    }).sort_values("Importance", ascending=False)

    fig_imp = px.bar(
        importance_df,
        x="Feature",
        y="Importance",
        title="Feature Importance for AQI Prediction",
        color="Importance"
    )
    st.plotly_chart(fig_imp, use_container_width=True)
