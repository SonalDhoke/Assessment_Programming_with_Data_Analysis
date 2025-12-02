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

    # ---------------------------------------------------------
    # LOAD CLEANED DATA
    # ---------------------------------------------------------
    if "cleaned_df" in st.session_state:
        df = st.session_state.cleaned_df.copy()
    else:
        st.error("Cleaned dataset not found. Please complete data cleaning first.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ---------------------------------------------------------
    # FEATURE ENGINEERING
    # ---------------------------------------------------------
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day

    # Add Season
    df["Season"] = df["Month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Summer", 4: "Summer", 5: "Summer",
        6: "Monsoon", 7: "Monsoon", 8: "Monsoon",
        9: "Post-Monsoon", 10: "Post-Monsoon", 11: "Post-Monsoon"
    })

    # Encode Season
    season_encoder = LabelEncoder()
    df["Season_Code"] = season_encoder.fit_transform(df["Season"])

    # Encode City
    city_encoder = LabelEncoder()
    df["City_Code"] = city_encoder.fit_transform(df["City"])

    # ---------------------------------------------------------
    # POLLUTANT FEATURE LIST
    # ---------------------------------------------------------
    pollutants = [
        col for col in df.columns 
        if col not in [
            "AQI", "AQI_Recalc", "AQI_Bucket", "AQI_Bucket_recalc",
            "City", "City_Code", "Date", "Month_Name",
            "Year", "Month", "Day", "Season", "Season_Code"
        ]
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    df = df.dropna(subset=pollutants + ["AQI_Recalc"])

    # ---------------------------------------------------------
    # REGRESSION MODEL – Predict AQI
    # ---------------------------------------------------------
    st.subheader("📈 Predict Numerical AQI (Regression)")

    X_reg = df[pollutants + ["City_Code", "Month", "Season_Code"]]
    y_reg = df["AQI_Recalc"]

    X_train, X_test, y_train, y_test = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=42
    )

    reg_model = RandomForestRegressor(n_estimators=200, random_state=42)
    reg_model.fit(X_train, y_train)

    y_pred_reg = reg_model.predict(X_test)
    reg_r2 = r2_score(y_test, y_pred_reg)

    st.success(f"Regression Model R² Score: **{reg_r2:.3f}**")

    # Save training column order
    reg_feature_order = X_reg.columns.tolist()

    # -------------------------------------
    # USER INPUT FOR REGRESSION PREDICTION
    # -------------------------------------
    st.markdown("### 🔮 Predict AQI from pollutant values")

    user_input = {}

    cols = st.columns(3)
    for idx, p in enumerate(pollutants):
        with cols[idx % 3]:
            user_input[p] = st.number_input(
                p, float(df[p].min()), float(df[p].max()), float(df[p].mean())
            )

    city_choice = st.selectbox("Select City", sorted(df["City"].unique()))
    month_choice = st.number_input("Month", min_value=1, max_value=12, value=6)

    season_choice = df[df["City"] == city_choice]["Season"].mode().iloc[0]
    season_code = season_encoder.transform([season_choice])[0]

    city_code = city_encoder.transform([city_choice])[0]

    input_df = pd.DataFrame([{
        **user_input,
        "City_Code": city_code,
        "Month": month_choice,
        "Season_Code": season_code
    }])

    # 🔧 FIX: Ensure same columns in same order
    input_df = input_df.reindex(columns=reg_feature_order)
    input_df = input_df.fillna(0)

    predicted_aqi = reg_model.predict(input_df)[0]
    st.info(f"### 🌫 Predicted AQI: **{predicted_aqi:.2f}**")

    # ---------------------------------------------------------
    # CLASSIFICATION MODEL – Predict AQI Category
    # ---------------------------------------------------------
    st.subheader("🏷 Predict AQI Category (Classification)")
    
    # Ensure column exists
    if "AQI_Bucket_Recalc" not in df.columns:
        st.error("Column 'AQI_Bucket_Recalc' not found in dataset.")
        return
    
    # Remove rows where bucket is missing
    df_clf = df.dropna(subset=["AQI_Bucket_Recalc"])
    
    X_clf = df_clf[pollutants + ["City_Code", "Month", "Season_Code"]]
    y_clf = df_clf["AQI_Bucket_Recalc"]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_clf, y_clf, test_size=0.2, random_state=42
    )
    
    # Train classifier
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred_clf = clf.predict(X_test)
    clf_acc = accuracy_score(y_test, y_pred_clf)
    
    st.success(f"Classification Model Accuracy: **{clf_acc:.3f}**")
    
    # ---- Prediction for User Input ----
    clf_feature_order = X_clf.columns.tolist()
    
    # Match columns exactly in same order
    input_df_clf = input_df.reindex(columns=clf_feature_order).fillna(0)
    
    pred_bucket = clf.predict(input_df_clf)[0]
    
    st.info(f"### 🏷 AQI Category Prediction: **{pred_bucket}**")

    # ---------------------------------------------------------
    # FEATURE IMPORTANCE PLOT
    # ---------------------------------------------------------
    st.subheader("🔍 Feature Importance (Regression Model)")

    importance_df = pd.DataFrame({
        "Feature": reg_feature_order,
        "Importance": reg_model.feature_importances_
    }).sort_values("Importance", ascending=False)

    fig_imp = px.bar(
        importance_df,
        x="Feature",
        y="Importance",
        title="Feature Importance for AQI Prediction"
    )
    st.plotly_chart(fig_imp, use_container_width=True)
