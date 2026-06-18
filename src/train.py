import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, roc_curve, precision_recall_curve
)
import joblib
import os

MODEL_PATH = "models/churn_model.pkl"


def get_models():
    return {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
    }


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    metrics = {
        "Accuracy": round(accuracy_score(y_test, y_pred), 4),
        "Precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
        "Recall": round(recall_score(y_test, y_pred, zero_division=0), 4),
        "F1 Score": round(f1_score(y_test, y_pred, zero_division=0), 4),
        "ROC-AUC": round(roc_auc_score(y_test, y_prob), 4),
    }
    cm = confusion_matrix(y_test, y_pred)
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    prec, rec, _ = precision_recall_curve(y_test, y_prob)
    return metrics, cm, fpr, tpr, prec, rec, y_pred, y_prob


def train_all_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    models = get_models()
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        metrics, cm, fpr, tpr, prec, rec, y_pred, y_prob = evaluate_model(model, X_test, y_test)
        results[name] = {
            "model": model,
            "metrics": metrics,
            "confusion_matrix": cm,
            "fpr": fpr,
            "tpr": tpr,
            "precision_curve": prec,
            "recall_curve": rec,
            "y_pred": y_pred,
            "y_prob": y_prob,
            "y_test": y_test,
        }

    # Pick best by ROC-AUC
    best_name = max(results, key=lambda k: results[k]["metrics"]["ROC-AUC"])
    best_model = results[best_name]["model"]

    os.makedirs("models", exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)

    return results, best_name, X_train, X_test, y_train, y_test


def load_model(path=MODEL_PATH):
    return joblib.load(path)


def get_feature_importance(model, feature_names):
    if hasattr(model, "feature_importances_"):
        imp = model.feature_importances_
    elif hasattr(model, "coef_"):
        imp = np.abs(model.coef_[0])
    else:
        return pd.DataFrame()
    df = pd.DataFrame({"Feature": feature_names, "Importance": imp})
    return df.sort_values("Importance", ascending=False).head(20)
