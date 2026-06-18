# 🔮 RetentionAI — Customer Churn Intelligence Platform

A complete end-to-end machine learning web application that predicts customer churn, explains predictions using SHAP (Explainable AI), and generates actionable retention recommendations.

---

## 🚀 Features

| Feature | Details |
|---|---|
| **Dataset Upload** | Upload any customer CSV or load built-in sample data |
| **Data Validation** | Missing values, duplicates, type checks, quality score |
| **EDA Dashboard** | 7+ interactive Plotly charts |
| **Model Training** | Logistic Regression, Random Forest, Gradient Boosting |
| **Auto Model Selection** | Best model chosen by ROC-AUC |
| **Churn Prediction** | Single customer form or batch CSV upload |
| **Risk Levels** | Low / Medium / High with colour-coded indicators |
| **SHAP Explainability** | Summary plot, feature importance, waterfall, individual explanation |
| **Retention Engine** | Rule-based recommendations per customer profile |
| **Downloads** | Predictions CSV, SHAP explanation CSV, strategy report TXT |

---

## 🗂️ Project Structure

```
RetentionAI/
├── app/
│   └── streamlit_app.py      # 6-page Streamlit dashboard
├── data/
│   ├── customer_churn.csv    # Sample dataset (auto-generated)
│   └── generate_data.py      # Dataset generator script
├── models/
│   ├── churn_model.pkl       # Best trained model (created at runtime)
│   └── preprocessor.pkl      # Fitted preprocessing pipeline (created at runtime)
├── src/
│   ├── preprocess.py         # Validation, encoding, scaling pipeline
│   ├── train.py              # Model training & evaluation
│   ├── predict.py            # Single & batch prediction
│   ├── explain.py            # SHAP explainability
│   ├── recommend.py          # Retention recommendation engine
│   └── utils.py              # Plotly charts & colour palette
├── reports/                  # Output folder for exported reports
├── main.py                   # Entry point
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone / Extract the project
```bash
cd RetentionAI
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python main.py
```
Or launch Streamlit directly:
```bash
streamlit run app/streamlit_app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📊 Dashboard Pages

### 🏠 Dashboard Overview
- Upload CSV or load sample dataset
- KPI cards: Total Customers, Churn Rate, Active Customers, Model Accuracy
- Dataset preview and churn distribution charts

### 📊 Data Analysis
- Data quality report with health score
- Missing values, duplicate detection, column type inspection
- Statistical summary, 6 EDA charts, interactive feature distribution explorer

### 🤖 Model Performance
- Train Logistic Regression, Random Forest, and Gradient Boosting in one click
- Auto-select best model by ROC-AUC
- Confusion matrix, ROC curves, Precision-Recall curves, feature importance

### 🎯 Churn Prediction
- Manual entry form with 15+ customer attributes
- Batch CSV upload for bulk prediction
- Churn probability gauge, risk badge, retention recommendations

### 🔍 Explainability
- SHAP global summary plot
- SHAP bar chart (mean absolute importance)
- Individual customer waterfall plot
- Positive churn factors vs retention factors breakdown

### 💡 Retention Strategy
- Risk score display for last predicted customer
- Tailored action recommendations
- Full customer profile view
- Downloadable strategy report

---

## 🧠 Model Details

| Model | Notes |
|---|---|
| Logistic Regression | Fast baseline, linear decision boundary |
| Random Forest | Ensemble, handles non-linearity, provides feature importance |
| Gradient Boosting | Often best performance, sequential boosting |

Selection criterion: **ROC-AUC score** on 20% held-out test set.

---

## 💡 Retention Rules

| Condition | Recommendation |
|---|---|
| Monthly Charges > $75 | 15% loyalty discount |
| Tenure < 12 months | Dedicated onboarding assistance |
| Month-to-month contract | Promote annual plan |
| Support Calls > 4 | Premium dedicated support rep |
| Fiber optic service | Free upgrade / speed boost |
| No online security | Bundle security free for 3 months |
| Senior citizen | Senior care program enrollment |
| Electronic check payment | Auto-pay discount ($5/month) |
| No tech support | Free TechSupport add-on 6 months |

---

## 📦 Dataset Format

The app expects a CSV with a `Churn` column (`Yes`/`No`). It works best with Telco-style churn datasets. Required-ish columns:

`tenure`, `MonthlyCharges`, `Contract`, `InternetService`, `PaymentMethod`, `gender`, `SeniorCitizen`, `Partner`, `Dependents`, `PhoneService`, `PaperlessBilling`, `SupportCalls`

Missing columns are handled gracefully via the preprocessing pipeline.

---

## 🛠️ Tech Stack

- **Streamlit** — Web dashboard
- **Scikit-learn** — ML pipelines, models, metrics
- **SHAP** — Explainable AI
- **Plotly** — Interactive charts
- **Pandas / NumPy** — Data processing
- **Matplotlib / Seaborn** — SHAP plots
- **Joblib** — Model serialisation

---

## 📄 License

MIT — free for personal and commercial use.
