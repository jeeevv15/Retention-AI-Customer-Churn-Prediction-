import shap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def get_explainer(model, X_train):
    try:
        explainer = shap.TreeExplainer(model)
    except Exception:
        explainer = shap.LinearExplainer(model, X_train, feature_perturbation="interventional")
    return explainer


def get_shap_values(explainer, X):
    shap_values = explainer.shap_values(X)
    # For binary classifiers, take class-1 values
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    return shap_values


def shap_summary_fig(shap_values, X, feature_names, max_display=15):
    X_df = pd.DataFrame(X, columns=feature_names)
    fig, ax = plt.subplots(figsize=(10, 6))
    shap.summary_plot(shap_values, X_df, max_display=max_display, show=False)
    plt.tight_layout()
    return fig


def shap_bar_fig(shap_values, feature_names, max_display=15):
    mean_abs = np.abs(shap_values).mean(axis=0)
    df = pd.DataFrame({"Feature": feature_names, "SHAP Importance": mean_abs})
    df = df.sort_values("SHAP Importance", ascending=True).tail(max_display)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df["Feature"], df["SHAP Importance"], color="#6366f1")
    ax.set_xlabel("Mean |SHAP Value|")
    ax.set_title("SHAP Feature Importance")
    ax.set_facecolor("#0f172a")
    fig.patch.set_facecolor("#0f172a")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.title.set_color("white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#334155")
    plt.tight_layout()
    return fig


def individual_explanation(shap_vals_single, feature_names, top_n=5):
    pairs = list(zip(feature_names, shap_vals_single))
    pairs_sorted = sorted(pairs, key=lambda x: abs(x[1]), reverse=True)[:top_n]
    pos = [(f, v) for f, v in pairs_sorted if v > 0]
    neg = [(f, v) for f, v in pairs_sorted if v <= 0]
    return pos, neg, pairs_sorted


def shap_waterfall_fig(explainer, shap_vals_single, X_single, feature_names):
    """Waterfall plot for individual customer"""
    try:
        X_df = pd.DataFrame([X_single], columns=feature_names)
        expl_obj = shap.Explanation(
            values=shap_vals_single,
            base_values=explainer.expected_value if not isinstance(explainer.expected_value, list)
                         else explainer.expected_value[1],
            data=X_single,
            feature_names=feature_names,
        )
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.plots.waterfall(expl_obj, max_display=12, show=False)
        plt.tight_layout()
        return fig
    except Exception:
        return None
