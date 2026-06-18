import io
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ─── Colour Palette ────────────────────────────────────────────────────────────
BG = "#0f172a"
CARD = "#1e293b"
ACCENT = "#6366f1"
GREEN = "#22c55e"
AMBER = "#f59e0b"
RED = "#ef4444"
TEXT = "#f1f5f9"
MUTED = "#94a3b8"

PLOTLY_TEMPLATE = dict(
    layout=dict(
        plot_bgcolor=CARD,
        paper_bgcolor=CARD,
        font=dict(color=TEXT, family="Inter, sans-serif"),
        title_font=dict(color=TEXT),
        legend=dict(bgcolor=CARD, font=dict(color=TEXT)),
        xaxis=dict(gridcolor="#334155", linecolor="#334155", tickcolor=MUTED),
        yaxis=dict(gridcolor="#334155", linecolor="#334155", tickcolor=MUTED),
    )
)


def apply_template(fig):
    fig.update_layout(
        plot_bgcolor=CARD,
        paper_bgcolor=CARD,
        font=dict(color=TEXT, family="Inter, sans-serif"),
        title_font=dict(color=TEXT, size=16),
    )
    fig.update_xaxes(gridcolor="#334155", linecolor="#334155")
    fig.update_yaxes(gridcolor="#334155", linecolor="#334155")
    return fig


# ─── EDA Charts ────────────────────────────────────────────────────────────────
def churn_pie(df):
    counts = df["Churn"].value_counts().reset_index()
    counts.columns = ["Churn", "Count"]
    fig = px.pie(counts, names="Churn", values="Count", title="Churn Distribution",
                 color_discrete_map={"Yes": RED, "No": GREEN},
                 hole=0.45)
    return apply_template(fig)


def churn_bar(df):
    counts = df["Churn"].value_counts().reset_index()
    counts.columns = ["Churn", "Count"]
    fig = px.bar(counts, x="Churn", y="Count", title="Churn Count",
                 color="Churn", color_discrete_map={"Yes": RED, "No": GREEN})
    return apply_template(fig)


def monthly_charges_vs_churn(df):
    fig = px.box(df, x="Churn", y="MonthlyCharges", title="Monthly Charges vs Churn",
                 color="Churn", color_discrete_map={"Yes": RED, "No": GREEN})
    return apply_template(fig)


def tenure_vs_churn(df):
    fig = px.histogram(df, x="tenure", color="Churn", barmode="overlay",
                       title="Tenure Distribution by Churn",
                       color_discrete_map={"Yes": RED, "No": GREEN}, nbins=30)
    return apply_template(fig)


def contract_vs_churn(df):
    ct = df.groupby(["Contract", "Churn"]).size().reset_index(name="Count")
    fig = px.bar(ct, x="Contract", y="Count", color="Churn", barmode="group",
                 title="Contract Type vs Churn",
                 color_discrete_map={"Yes": RED, "No": GREEN})
    return apply_template(fig)


def correlation_heatmap(df):
    num_df = df.select_dtypes(include=["int64", "float64"]).copy()
    if "Churn" in df.columns:
        num_df["Churn_enc"] = (df["Churn"].str.lower() == "yes").astype(int)
    corr = num_df.corr()
    fig = px.imshow(corr, text_auto=".2f", title="Correlation Heatmap",
                    color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    return apply_template(fig)


def feature_distributions(df, col):
    fig = px.histogram(df, x=col, color="Churn", barmode="overlay",
                       title=f"Distribution: {col}",
                       color_discrete_map={"Yes": RED, "No": GREEN})
    return apply_template(fig)


# ─── Model Evaluation Charts ───────────────────────────────────────────────────
def confusion_matrix_fig(cm, labels=("No Churn", "Churn")):
    fig = px.imshow(cm, text_auto=True, x=list(labels), y=list(labels),
                    color_continuous_scale="Blues",
                    title="Confusion Matrix",
                    labels=dict(x="Predicted", y="Actual"))
    return apply_template(fig)


def roc_curve_fig(results):
    fig = go.Figure()
    colors = [ACCENT, GREEN, AMBER, RED]
    for i, (name, r) in enumerate(results.items()):
        fig.add_trace(go.Scatter(
            x=r["fpr"], y=r["tpr"],
            name=f'{name} (AUC={r["metrics"]["ROC-AUC"]:.3f})',
            line=dict(color=colors[i % len(colors)], width=2)
        ))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines",
                             line=dict(dash="dash", color=MUTED), name="Random"))
    fig.update_layout(title="ROC Curves", xaxis_title="False Positive Rate",
                      yaxis_title="True Positive Rate")
    return apply_template(fig)


def pr_curve_fig(results):
    fig = go.Figure()
    colors = [ACCENT, GREEN, AMBER, RED]
    for i, (name, r) in enumerate(results.items()):
        fig.add_trace(go.Scatter(
            x=r["recall_curve"], y=r["precision_curve"],
            name=name, line=dict(color=colors[i % len(colors)], width=2)
        ))
    fig.update_layout(title="Precision-Recall Curves",
                      xaxis_title="Recall", yaxis_title="Precision")
    return apply_template(fig)


def feature_importance_fig(imp_df):
    imp_df = imp_df.sort_values("Importance", ascending=True).tail(15)
    fig = px.bar(imp_df, x="Importance", y="Feature", orientation="h",
                 title="Feature Importance", color="Importance",
                 color_continuous_scale="Viridis")
    return apply_template(fig)


def model_comparison_table(results):
    rows = []
    for name, r in results.items():
        row = {"Model": name}
        row.update(r["metrics"])
        rows.append(row)
    return pd.DataFrame(rows)


# ─── CSV Export ────────────────────────────────────────────────────────────────
def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")
