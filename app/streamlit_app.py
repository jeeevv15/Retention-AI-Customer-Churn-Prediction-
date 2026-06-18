import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.preprocess import validate_dataset, preprocess, get_feature_names
from src.train import train_all_models, get_feature_importance
from src.predict import predict_single, predict_batch, get_risk_level, risk_color
from src.explain import (get_explainer, get_shap_values, shap_summary_fig,
                          shap_bar_fig, individual_explanation, shap_waterfall_fig)
from src.recommend import get_recommendations
from src.utils import (churn_pie, churn_bar, monthly_charges_vs_churn,
                        tenure_vs_churn, contract_vs_churn, correlation_heatmap,
                        feature_distributions, confusion_matrix_fig, roc_curve_fig,
                        pr_curve_fig, feature_importance_fig, model_comparison_table,
                        df_to_csv_bytes)
from src.theme import (apply_retro_theme, metric_card, section_header,
                        retro_window, speech_bubble, pixel_divider,
                        retro_alert, BG, CARD, ACCENT, GREEN, AMBER,
                        RED, TEXT, MUTED, PINK, LIME, PURPLE, BORDER, TITLEBAR)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RetentionAI",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_retro_theme()

# ── Session state ─────────────────────────────────────────────────────────────
for key in ["df", "train_results", "best_name", "preprocessor_bundle",
            "feature_names", "X_train", "X_test", "y_train", "y_test",
            "model", "last_customer", "last_prob"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
PIXEL_BAR = """
<div style="height:8px;margin:10px 0;
    background:repeating-linear-gradient(
        90deg,#c8b8f0 0,#c8b8f0 8px,#f0b8d4 8px,#f0b8d4 16px,
        #c8e88a 16px,#c8e88a 24px,#f0eaff 24px,#f0eaff 32px);
    border-top:2px solid #2d2040;border-bottom:2px solid #2d2040;">
</div>"""

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:14px 0 6px 0;">
        <div class="logo-text">🔮 RetentionAI</div>
        <div class="subtitle-text">Churn Intelligence Platform</div>
    </div>""", unsafe_allow_html=True)
    st.markdown(PIXEL_BAR, unsafe_allow_html=True)

with st.sidebar:
    page = st.radio(
        "Navigation",
        [   "🏠 Dashboard",
            "📊 Data Analysis",
            "🤖 Model Performance",
            "🎯 Churn Prediction",
            "🔍 Explainability",
            "💡 Retention Strategy",
        ],
        label_visibility="collapsed",
    )

    st.markdown(PIXEL_BAR, unsafe_allow_html=True)

    if st.session_state.df is not None:
        df_s = st.session_state.df
        churn_r = (df_s["Churn"].str.lower() == "yes").mean() if "Churn" in df_s.columns else 0
        trained_html = ('<div style="color:#5ab85a;font-weight:700;">✅ Model trained</div>'
                        if st.session_state.model else
                        '<div style="color:#e8a020;">⏳ Model not trained</div>')
        st.markdown(f"""
        <div style="background:#fff;border:2px solid #2d2040;padding:10px 12px;
             box-shadow:3px 3px 0 #2d2040;font-size:0.78rem;">
            <div style="color:#7a6a9a;font-weight:700;margin-bottom:6px;
                 text-transform:uppercase;letter-spacing:.05em;">📋 Status</div>
            <div><b>{len(df_s):,}</b> customers loaded</div>
            <div style="color:#d43050;"><b>{churn_r:.1%}</b> churn rate</div>
            {trained_html}
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:14px;color:#7a6a9a;font-size:0.7rem;text-align:center;">
        v1.0 · Streamlit + SHAP + Scikit-learn
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════
if "Dashboard" in page:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#c8b8f0,#f0b8d4);
         border:3px solid #2d2040;box-shadow:6px 6px 0 #2d2040;
         padding:24px 28px;margin-bottom:20px;">
        <div style="font-family:'Press Start 2P',monospace;font-size:1.3rem;
             color:#2d2040;text-shadow:2px 2px 0 #fff;line-height:1.6;">
            🔮 RetentionAI
        </div>
        <div style="font-size:0.95rem;color:#4a3060;font-weight:600;margin-top:6px;">
            Predict · Explain · Retain — Powered by ML & SHAP
        </div>
    </div>""", unsafe_allow_html=True)

    col_up, col_guide = st.columns([2, 1])
    with col_up:
        retro_window("💾 Upload Dataset", "📁")
        uploaded = st.file_uploader("Upload CSV", type=["csv"],
                                     label_visibility="collapsed")
        if uploaded:
            df = pd.read_csv(uploaded)
            st.session_state.df = df
            retro_alert(f"Dataset loaded — {len(df):,} rows × {len(df.columns)} columns", "success")
        if st.button("🎲 Load Sample Dataset"):
            path = os.path.join(os.path.dirname(__file__), "..", "data", "customer_churn.csv")
            df = pd.read_csv(path)
            st.session_state.df = df
            retro_alert(f"Sample dataset loaded — {len(df):,} rows × {len(df.columns)} columns", "success")

    with col_guide:
        retro_window("📖 Quick Start", "ℹ️", """
        <ol style="color:#2d2040;font-size:0.82rem;line-height:2.2;padding-left:18px;margin:0;">
            <li>Upload or load sample dataset</li>
            <li>Explore <b>Data Analysis</b></li>
            <li>Train in <b>Model Performance</b></li>
            <li>Predict in <b>Churn Prediction</b></li>
            <li>Understand with <b>Explainability</b></li>
            <li>Act on <b>Retention Strategy</b></li>
        </ol>""")

    if st.session_state.df is not None:
        df = st.session_state.df
        pixel_divider()
        section_header("📈 Dataset Overview")

        c1, c2, c3, c4 = st.columns(4)
        churn_rate = (df["Churn"].str.lower() == "yes").mean() if "Churn" in df.columns else 0
        active = int((1 - churn_rate) * len(df))
        with c1: metric_card("Total Customers", f"{len(df):,}")
        with c2: metric_card("Churn Rate", f"{churn_rate:.1%}")
        with c3: metric_card("Active Customers", f"{active:,}")
        if st.session_state.train_results:
            best = st.session_state.best_name
            acc = st.session_state.train_results[best]["metrics"]["Accuracy"]
            with c4: metric_card("Model Accuracy", f"{acc:.1%}", best)
        else:
            with c4: metric_card("Model Status", "—", "Not trained yet")

        pixel_divider()
        section_header("👁️ Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        if "Churn" in df.columns:
            col_l, col_r = st.columns(2)
            with col_l: st.plotly_chart(churn_pie(df), use_container_width=True)
            with col_r: st.plotly_chart(churn_bar(df), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# PAGE 2 — DATA ANALYSIS
# ═══════════════════════════════════════════════════════════════════
elif "Data Analysis" in page:
    st.markdown("""<div style="font-family:'Press Start 2P',monospace;font-size:1rem;
        color:#9b72d4;margin-bottom:18px;text-shadow:2px 2px 0 #c8b8f0;">
        📊 Data Analysis</div>""", unsafe_allow_html=True)

    if st.session_state.df is None:
        retro_alert("Please upload a dataset on the Dashboard first.", "warning")
        st.stop()

    df = st.session_state.df
    report = validate_dataset(df)

    section_header("🏥 Data Quality Report")
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Total Rows", f"{report['total_rows']:,}")
    with c2: metric_card("Total Columns", str(report["total_cols"]))
    with c3: metric_card("Missing Values", str(report["total_missing"]))
    with c4: metric_card("Quality Score", f"{report['quality_score']}%")

    pixel_divider()
    col_a, col_b = st.columns(2)
    with col_a:
        section_header("❓ Missing Values")
        miss_df = pd.DataFrame({
            "Column": list(report["missing_values"].keys()),
            "Missing": list(report["missing_values"].values()),
            "Missing %": list(report["missing_pct"].values()),
        }).sort_values("Missing", ascending=False)
        st.dataframe(miss_df, use_container_width=True, height=250)

    with col_b:
        section_header("📋 Column Types")
        dtype_df = pd.DataFrame({
            "Column": list(report["dtypes"].keys()),
            "Type": list(report["dtypes"].values()),
        })
        st.dataframe(dtype_df, use_container_width=True, height=250)

    if report["duplicate_rows"] > 0:
        retro_alert(f"Found {report['duplicate_rows']} duplicate rows.", "warning")
    else:
        retro_alert("No duplicate rows detected. ✨", "success")

    pixel_divider()
    section_header("📐 Statistical Summary")
    st.dataframe(df.describe().round(2), use_container_width=True)

    pixel_divider()
    section_header("📈 Exploratory Data Analysis")

    if "Churn" in df.columns:
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(churn_pie(df), use_container_width=True)
        with c2: st.plotly_chart(churn_bar(df), use_container_width=True)

        c3, c4 = st.columns(2)
        if "MonthlyCharges" in df.columns:
            with c3: st.plotly_chart(monthly_charges_vs_churn(df), use_container_width=True)
        if "tenure" in df.columns:
            with c4: st.plotly_chart(tenure_vs_churn(df), use_container_width=True)

        if "Contract" in df.columns:
            st.plotly_chart(contract_vs_churn(df), use_container_width=True)
        st.plotly_chart(correlation_heatmap(df), use_container_width=True)

        section_header("🔎 Feature Distribution Explorer")
        num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        if num_cols:
            sel = st.selectbox("Select a feature", num_cols)
            st.plotly_chart(feature_distributions(df, sel), use_container_width=True)

    st.download_button("⬇️ Download Processed Dataset",
                       df_to_csv_bytes(df), "processed_dataset.csv", "text/csv")


# ═══════════════════════════════════════════════════════════════════
# PAGE 3 — MODEL PERFORMANCE
# ═══════════════════════════════════════════════════════════════════
elif "Model Performance" in page:
    st.markdown("""<div style="font-family:'Press Start 2P',monospace;font-size:1rem;
        color:#9b72d4;margin-bottom:18px;text-shadow:2px 2px 0 #c8b8f0;">
        🤖 Model Training & Performance</div>""", unsafe_allow_html=True)

    if st.session_state.df is None:
        retro_alert("Please upload a dataset on the Dashboard first.", "warning")
        st.stop()

    df = st.session_state.df

    col_btn, col_hint = st.columns([1, 3])
    with col_btn:
        train_clicked = st.button("🚀 Train All Models")
    with col_hint:
        speech_bubble("Trains Logistic Regression, Random Forest & Gradient Boosting — best is auto-selected! 🏆", "#c8b8f0")

    if train_clicked:
        with st.spinner("Training models — please wait…"):
            try:
                X, y, preprocessor, num_cols, cat_cols = preprocess(df, fit=True)
                feature_names = get_feature_names(preprocessor, num_cols, cat_cols)
                results, best_name, X_train, X_test, y_train, y_test = train_all_models(X, y)
                model = results[best_name]["model"]
                st.session_state.update({
                    "train_results": results,
                    "best_name": best_name,
                    "preprocessor_bundle": (preprocessor, num_cols, cat_cols),
                    "feature_names": feature_names,
                    "X_train": X_train,
                    "X_test": X_test,
                    "y_train": y_train,
                    "y_test": y_test,
                    "model": model,
                })
                retro_alert(f"Training complete! Best model: {best_name}", "success")
            except Exception as e:
                retro_alert(f"Training error: {e}", "error")
                st.stop()

    if st.session_state.train_results is None:
        retro_alert("Click Train All Models above to get started.", "info")
        st.stop()

    results = st.session_state.train_results
    best_name = st.session_state.best_name
    feature_names = st.session_state.feature_names
    best_m = results[best_name]["metrics"]

    pixel_divider()
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#c8e88a,#c8b8f0);
         border:3px solid #2d2040;box-shadow:5px 5px 0 #2d2040;
         padding:16px 22px;margin-bottom:16px;">
        <div style="font-weight:800;font-size:1.1rem;color:#2d2040;">
            🏆 Best Model: {best_name}
        </div>
        <div style="color:#4a3060;font-size:0.82rem;margin-top:4px;">
            Auto-selected by highest ROC-AUC on held-out test set
        </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, (k, v) in zip([c1, c2, c3, c4, c5], best_m.items()):
        with col: metric_card(k, f"{v:.3f}")

    pixel_divider()
    section_header("📊 Model Comparison")
    st.dataframe(model_comparison_table(results), use_container_width=True)

    col_l, col_r = st.columns(2)
    with col_l:
        section_header("📉 ROC Curves")
        st.plotly_chart(roc_curve_fig(results), use_container_width=True)
    with col_r:
        section_header("📉 Precision-Recall Curves")
        st.plotly_chart(pr_curve_fig(results), use_container_width=True)

    section_header("🗂️ Confusion Matrix")
    sel_model = st.selectbox("Choose model", list(results.keys()))
    st.plotly_chart(confusion_matrix_fig(results[sel_model]["confusion_matrix"]),
                    use_container_width=True)

    section_header("🌟 Feature Importance")
    imp_df = get_feature_importance(results[best_name]["model"], feature_names)
    if not imp_df.empty:
        st.plotly_chart(feature_importance_fig(imp_df), use_container_width=True)


# ═══════════════════════════════════════════════════════════════════
# PAGE 4 — CHURN PREDICTION
# ═══════════════════════════════════════════════════════════════════
elif "Churn Prediction" in page:
    st.markdown("""<div style="font-family:'Press Start 2P',monospace;font-size:1rem;
        color:#9b72d4;margin-bottom:18px;text-shadow:2px 2px 0 #c8b8f0;">
        🎯 Churn Prediction</div>""", unsafe_allow_html=True)

    if st.session_state.model is None:
        retro_alert("Please train a model on the Model Performance page first.", "warning")
        st.stop()

    model = st.session_state.model
    bundle = st.session_state.preprocessor_bundle

    tab1, tab2 = st.tabs(["👤 Manual Entry", "📂 Batch Upload"])

    with tab1:
        section_header("Enter Customer Details")
        c1, c2, c3 = st.columns(3)
        with c1:
            tenure = st.number_input("Tenure (months)", 0, 72, 12)
            monthly_charges = st.number_input("Monthly Charges ($)", 10.0, 150.0, 65.0)
            support_calls = st.number_input("Support Calls", 0, 20, 2)
            senior_citizen = st.selectbox("Senior Citizen", [0, 1])
        with c2:
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            payment_method = st.selectbox("Payment Method", [
                "Electronic check", "Mailed check",
                "Bank transfer (automatic)", "Credit card (automatic)"])
        with c3:
            gender = st.selectbox("Gender", ["Male", "Female"])
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["Yes", "No"])
            paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
            phone_svc = st.selectbox("Phone Service", ["Yes", "No"])

        customer = {
            "tenure": tenure, "MonthlyCharges": monthly_charges,
            "SupportCalls": support_calls, "SeniorCitizen": senior_citizen,
            "Contract": contract, "InternetService": internet_service,
            "PaymentMethod": payment_method, "gender": gender,
            "Partner": partner, "Dependents": dependents,
            "PaperlessBilling": paperless, "PhoneService": phone_svc,
            "MultipleLines": "No", "OnlineSecurity": "No", "OnlineBackup": "No",
            "DeviceProtection": "No", "TechSupport": "No",
            "StreamingTV": "No", "StreamingMovies": "No",
            "TotalCharges": monthly_charges * tenure,
        }

        if st.button("🔮 Predict Churn"):
            with st.spinner("Running prediction…"):
                pred, prob, risk = predict_single(customer, model, bundle)

            color = risk_color(risk)
            churn_label = "⚠️ WILL CHURN" if pred == 1 else "✅ WILL NOT CHURN"
            pixel_divider()

            col_res, col_gauge = st.columns(2)
            with col_res:
                st.markdown(f"""
                <div style="background:#fff;border:3px solid #2d2040;
                     box-shadow:6px 6px 0 #2d2040;overflow:hidden;">
                    <div style="background:linear-gradient(90deg,{color}44,{color}11);
                         border-bottom:2.5px solid #2d2040;padding:8px 14px;
                         display:flex;align-items:center;justify-content:space-between;">
                        <span style="font-weight:800;color:#2d2040;font-size:0.85rem;">
                            🖥️ Prediction Result
                        </span>
                        <div style="display:flex;gap:4px;">
                            <span style="width:14px;height:14px;border:2px solid #2d2040;
                                display:inline-flex;align-items:center;justify-content:center;
                                background:#f0eaff;font-size:9px;">_</span>
                            <span style="width:14px;height:14px;border:2px solid #2d2040;
                                display:inline-flex;align-items:center;justify-content:center;
                                background:#f0eaff;font-size:9px;">□</span>
                            <span style="width:14px;height:14px;border:2px solid #2d2040;
                                display:inline-flex;align-items:center;justify-content:center;
                                background:#f0eaff;font-size:9px;">✕</span>
                        </div>
                    </div>
                    <div style="padding:24px;text-align:center;">
                        <div style="font-family:'VT323',monospace;font-size:2rem;
                             color:{color};font-weight:700;">{churn_label}</div>
                        <div style="font-family:'VT323',monospace;font-size:4.5rem;
                             color:{color};line-height:1;">{prob:.1%}</div>
                        <div style="color:#7a6a9a;font-size:0.78rem;margin-bottom:12px;">
                            Churn Probability
                        </div>
                        <span class="risk-badge"
                            style="background:{color}22;color:{color};border:2.5px solid {color};">
                            {risk}
                        </span>
                        <div style="margin-top:18px;background:#f0eaff;
                             border:2px solid #2d2040;height:20px;">
                            <div style="
                                background:repeating-linear-gradient(
                                    90deg,{color} 0,{color} 14px,{color}66 14px,{color}66 18px);
                                width:{prob*100:.0f}%;height:100%;">
                            </div>
                        </div>
                        <div style="font-size:0.7rem;color:#7a6a9a;margin-top:4px;">
                            Risk bar — {prob*100:.0f}%
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            with col_gauge:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob * 100,
                    title={"text": "Churn Risk Score",
                           "font": {"color": "#2d2040", "family": "Space Grotesk"}},
                    number={"suffix": "%", "font": {"color": "#2d2040"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#7a6a9a"},
                        "bar": {"color": color},
                        "bgcolor": "#faf5ff",
                        "bordercolor": "#2d2040",
                        "borderwidth": 2,
                        "steps": [
                            {"range": [0, 35],  "color": "#d8f8d8"},
                            {"range": [35, 65], "color": "#fff8d8"},
                            {"range": [65, 100],"color": "#ffd8e0"},
                        ],
                    },
                ))
                fig.update_layout(
                    paper_bgcolor="#ffffff",
                    font={"color": "#2d2040", "family": "Space Grotesk"},
                    height=300,
                    margin=dict(t=50, b=20, l=20, r=20),
                )
                st.plotly_chart(fig, use_container_width=True)

            recs = get_recommendations(customer, prob)
            section_header("💡 Retention Recommendations")
            for i, r in enumerate(recs, 1):
                st.markdown(f"""
                <div class="rec-card">
                    <span style="background:#c8b8f0;border:2px solid #2d2040;
                         padding:2px 7px;font-weight:800;margin-right:8px;
                         box-shadow:2px 2px 0 #2d2040;font-size:0.75rem;">{i:02d}</span>
                    {r}
                </div>""", unsafe_allow_html=True)

            st.session_state["last_customer"] = customer
            st.session_state["last_prob"] = prob

    with tab2:
        section_header("📂 Batch Prediction via CSV")
        batch_file = st.file_uploader("Upload customer CSV", type=["csv"], key="batch")
        if batch_file:
            batch_df = pd.read_csv(batch_file)
            st.dataframe(batch_df.head(), use_container_width=True)
            if st.button("🔮 Run Batch Prediction"):
                with st.spinner("Running batch predictions…"):
                    try:
                        preds, probs, risks = predict_batch(batch_df, model, bundle)
                        batch_df["Predicted_Churn"] = ["Yes" if p else "No" for p in preds]
                        batch_df["Churn_Probability"] = np.round(probs, 4)
                        batch_df["Risk_Level"] = risks
                        retro_alert(f"Done! Predictions for {len(batch_df):,} customers.", "success")
                        st.dataframe(
                            batch_df[["Predicted_Churn","Churn_Probability","Risk_Level"]].head(20),
                            use_container_width=True)
                        st.download_button("⬇️ Download Predictions",
                                           df_to_csv_bytes(batch_df),
                                           "churn_predictions.csv", "text/csv")
                    except Exception as e:
                        retro_alert(f"Prediction error: {e}", "error")


# ═══════════════════════════════════════════════════════════════════
# PAGE 5 — EXPLAINABILITY
# ═══════════════════════════════════════════════════════════════════
elif "Explainability" in page:
    st.markdown("""<div style="font-family:'Press Start 2P',monospace;font-size:1rem;
        color:#9b72d4;margin-bottom:18px;text-shadow:2px 2px 0 #c8b8f0;">
        🔍 Explainable AI — SHAP</div>""", unsafe_allow_html=True)

    if st.session_state.model is None:
        retro_alert("Please train a model on the Model Performance page first.", "warning")
        st.stop()

    model = st.session_state.model
    X_train = st.session_state.X_train
    X_test  = st.session_state.X_test
    feature_names = st.session_state.feature_names

    speech_bubble("SHAP values show which features push predictions toward or away from churn! 🧠", "#c8e88a")

    with st.spinner("Computing SHAP values — this may take a moment…"):
        try:
            explainer = get_explainer(model, X_train)
            shap_vals = get_shap_values(explainer, X_test[:200])
        except Exception as e:
            retro_alert(f"SHAP error: {e}", "error")
            st.stop()

    tab1, tab2, tab3 = st.tabs(["📊 Global Summary", "📈 Feature Importance", "👤 Individual"])

    with tab1:
        section_header("SHAP Summary Plot")
        fig = shap_summary_fig(shap_vals, X_test[:200], feature_names)
        st.pyplot(fig, use_container_width=True)
        plt.clf()

    with tab2:
        section_header("SHAP Feature Importance (Mean |SHAP|)")
        fig2 = shap_bar_fig(shap_vals, feature_names)
        st.pyplot(fig2, use_container_width=True)
        plt.clf()

    with tab3:
        section_header("Individual Customer Explanation")
        idx = st.slider("Select test customer index", 0, min(199, len(X_test)-1), 0)
        single_shap = shap_vals[idx]
        single_x    = X_test[idx]
        pos, neg, _ = individual_explanation(single_shap, feature_names, top_n=8)

        col_pos, col_neg = st.columns(2)
        with col_pos:
            st.markdown("""
            <div style="background:linear-gradient(90deg,#ffd8e0,#fff0f4);
                 border:2.5px solid #d43050;box-shadow:4px 4px 0 #2d2040;
                 padding:10px 14px;font-weight:700;color:#d43050;margin-bottom:8px;">
                🔺 Churn Risk Factors
            </div>""", unsafe_allow_html=True)
            if pos:
                for f, v in pos:
                    st.markdown(
                        f'<div class="explain-pos">⬆ <b>{f}</b>'
                        f'<span style="float:right;color:#d43050">+{v:.3f}</span></div>',
                        unsafe_allow_html=True)
            else:
                retro_alert("No positive SHAP values for this customer.", "info")

        with col_neg:
            st.markdown("""
            <div style="background:linear-gradient(90deg,#d8f8d8,#f0fff4);
                 border:2.5px solid #5ab85a;box-shadow:4px 4px 0 #2d2040;
                 padding:10px 14px;font-weight:700;color:#5ab85a;margin-bottom:8px;">
                🔻 Retention Factors
            </div>""", unsafe_allow_html=True)
            if neg:
                for f, v in neg:
                    st.markdown(
                        f'<div class="explain-neg">⬇ <b>{f}</b>'
                        f'<span style="float:right;color:#5ab85a">{v:.3f}</span></div>',
                        unsafe_allow_html=True)
            else:
                retro_alert("No negative SHAP values for this customer.", "info")

        wf_fig = shap_waterfall_fig(explainer, single_shap, single_x, feature_names)
        if wf_fig:
            st.pyplot(wf_fig, use_container_width=True)
            plt.clf()

        shap_df = pd.DataFrame({"Feature": feature_names, "SHAP_Value": single_shap})
        st.download_button("⬇️ Download SHAP Explanation",
                           df_to_csv_bytes(shap_df), "shap_explanation.csv", "text/csv")


# ═══════════════════════════════════════════════════════════════════
# PAGE 6 — RETENTION STRATEGY
# ═══════════════════════════════════════════════════════════════════
elif "Retention Strategy" in page:
    st.markdown("""<div style="font-family:'Press Start 2P',monospace;font-size:1rem;
        color:#9b72d4;margin-bottom:18px;text-shadow:2px 2px 0 #c8b8f0;">
        💡 Retention Strategy Engine</div>""", unsafe_allow_html=True)

    if st.session_state.model is None:
        retro_alert("Please train a model first.", "warning")
        st.stop()

    customer = st.session_state.get("last_customer")
    prob     = st.session_state.get("last_prob")

    if customer is None:
        speech_bubble("Go to Churn Prediction, run a prediction, then come back here! 👈", PINK)
        st.stop()

    risk  = get_risk_level(prob)
    color = risk_color(risk)
    recs  = get_recommendations(customer, prob)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div style="background:#fff;border:3px solid {color};
             box-shadow:6px 6px 0 #2d2040;overflow:hidden;">
            <div style="background:linear-gradient(90deg,{color}55,{color}11);
                 border-bottom:2.5px solid #2d2040;padding:8px 14px;
                 font-weight:800;color:#2d2040;font-size:0.82rem;">
                ⚠️ Risk Assessment
            </div>
            <div style="padding:22px;text-align:center;">
                <div style="color:#7a6a9a;font-size:0.72rem;font-weight:700;
                     text-transform:uppercase;letter-spacing:.1em;">
                    Churn Probability
                </div>
                <div style="font-family:'VT323',monospace;font-size:4rem;
                     color:{color};line-height:1.1;margin:8px 0;">{prob:.1%}</div>
                <span class="risk-badge"
                    style="background:{color}22;color:{color};border:2.5px solid {color};">
                    {risk}
                </span>
                <div style="margin-top:14px;background:#f0eaff;
                     border:2px solid #2d2040;height:16px;">
                    <div style="background:repeating-linear-gradient(
                        90deg,{color} 0,{color} 12px,{color}44 12px,{color}44 16px);
                        width:{prob*100:.0f}%;height:100%;">
                    </div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        section_header("🎯 Recommended Retention Actions")
        for i, r in enumerate(recs, 1):
            st.markdown(f"""
            <div class="rec-card">
                <span style="background:#c8b8f0;border:2px solid #2d2040;
                     padding:2px 8px;font-weight:800;margin-right:8px;
                     box-shadow:2px 2px 0 #2d2040;font-size:0.75rem;">{i:02d}</span>
                {r}
            </div>""", unsafe_allow_html=True)

    pixel_divider()
    section_header("📋 Customer Profile")
    profile_df = pd.DataFrame([customer]).T.reset_index()
    profile_df.columns = ["Attribute", "Value"]
    st.dataframe(profile_df, use_container_width=True, height=400)

    lines = ["RetentionAI — Retention Strategy Report", "="*44,
             f"Churn Probability : {prob:.1%}",
             f"Risk Level        : {risk}", "",
             "Recommended Actions:"]
    for i, r in enumerate(recs, 1):
        lines.append(f"  {i}. {r}")
    lines += ["", "Customer Profile:"]
    for k, v in customer.items():
        lines.append(f"  {k}: {v}")
    st.download_button("⬇️ Download Strategy Report",
                       "\n".join(lines).encode(),
                       "retention_strategy.txt", "text/plain")