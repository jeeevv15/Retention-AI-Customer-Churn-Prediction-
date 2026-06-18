import numpy as np
import pandas as pd
import joblib
from src.preprocess import preprocess


PREPROCESSOR_PATH = "models/preprocessor.pkl"
MODEL_PATH = "models/churn_model.pkl"


def predict_single(customer_dict: dict, model=None, preprocessor_bundle=None):
    df = pd.DataFrame([customer_dict])
    X, _ = preprocess(df, fit=False, pipeline=preprocessor_bundle, save_path=PREPROCESSOR_PATH)
    if model is None:
        model = joblib.load(MODEL_PATH)
    prob = model.predict_proba(X)[0][1]
    pred = int(prob >= 0.5)
    risk = get_risk_level(prob)
    return pred, prob, risk


def predict_batch(df: pd.DataFrame, model=None, preprocessor_bundle=None):
    X, y = preprocess(df, fit=False, pipeline=preprocessor_bundle, save_path=PREPROCESSOR_PATH)
    if model is None:
        model = joblib.load(MODEL_PATH)
    probs = model.predict_proba(X)[:, 1]
    preds = (probs >= 0.5).astype(int)
    risks = [get_risk_level(p) for p in probs]
    return preds, probs, risks


def get_risk_level(prob: float) -> str:
    if prob < 0.35:
        return "Low Risk"
    elif prob < 0.65:
        return "Medium Risk"
    else:
        return "High Risk"


def risk_color(risk: str) -> str:
    return {"Low Risk": "#22c55e", "Medium Risk": "#f59e0b", "High Risk": "#ef4444"}.get(risk, "#6b7280")
