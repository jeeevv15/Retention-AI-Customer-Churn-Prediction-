import numpy as np
import pandas as pd

def generate_sample_data(n=1000, seed=42):
    np.random.seed(seed)
    df = pd.DataFrame({
        "customerID": [f"CUST-{i:04d}" for i in range(n)],
        "gender": np.random.choice(["Male", "Female"], n),
        "SeniorCitizen": np.random.choice([0, 1], n, p=[0.84, 0.16]),
        "Partner": np.random.choice(["Yes", "No"], n),
        "Dependents": np.random.choice(["Yes", "No"], n, p=[0.3, 0.7]),
        "tenure": np.random.randint(1, 72, n),
        "PhoneService": np.random.choice(["Yes", "No"], n, p=[0.9, 0.1]),
        "MultipleLines": np.random.choice(["Yes", "No", "No phone service"], n),
        "InternetService": np.random.choice(["DSL", "Fiber optic", "No"], n, p=[0.34, 0.44, 0.22]),
        "OnlineSecurity": np.random.choice(["Yes", "No", "No internet service"], n),
        "OnlineBackup": np.random.choice(["Yes", "No", "No internet service"], n),
        "DeviceProtection": np.random.choice(["Yes", "No", "No internet service"], n),
        "TechSupport": np.random.choice(["Yes", "No", "No internet service"], n),
        "StreamingTV": np.random.choice(["Yes", "No", "No internet service"], n),
        "StreamingMovies": np.random.choice(["Yes", "No", "No internet service"], n),
        "Contract": np.random.choice(["Month-to-month", "One year", "Two year"], n, p=[0.55, 0.24, 0.21]),
        "PaperlessBilling": np.random.choice(["Yes", "No"], n, p=[0.59, 0.41]),
        "PaymentMethod": np.random.choice(
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], n
        ),
        "MonthlyCharges": np.round(np.random.uniform(18, 120, n), 2),
        "TotalCharges": np.round(np.random.uniform(18, 8700, n), 2),
        "SupportCalls": np.random.randint(0, 10, n),
    })
    # Churn logic
    churn_prob = (
        0.1
        + 0.25 * (df["Contract"] == "Month-to-month").astype(float)
        + 0.15 * (df["tenure"] < 12).astype(float)
        + 0.10 * (df["MonthlyCharges"] > 80).astype(float)
        + 0.10 * (df["SupportCalls"] > 5).astype(float)
        - 0.10 * (df["Contract"] == "Two year").astype(float)
        - 0.05 * (df["tenure"] > 48).astype(float)
    ).clip(0, 1)
    df["Churn"] = np.where(np.random.rand(n) < churn_prob, "Yes", "No")
    return df

if __name__ == "__main__":
    df = generate_sample_data(1000)
    df.to_csv("data/customer_churn.csv", index=False)
    print(f"Generated {len(df)} records. Churn rate: {(df['Churn']=='Yes').mean():.1%}")
