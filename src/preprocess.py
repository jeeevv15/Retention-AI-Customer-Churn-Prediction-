import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import joblib
import os

TARGET_COL = "Churn"
DROP_COLS = ["customerID", "TotalCharges"]


def get_column_types(df: pd.DataFrame):
    df = df.copy()
    # Drop target and ID-like cols for analysis
    feature_df = df.drop(columns=[c for c in DROP_COLS + [TARGET_COL] if c in df.columns], errors="ignore")
    num_cols = feature_df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = feature_df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    return num_cols, cat_cols


def validate_dataset(df: pd.DataFrame) -> dict:
    report = {}
    report["total_rows"] = len(df)
    report["total_cols"] = len(df.columns)
    report["missing_values"] = df.isnull().sum().to_dict()
    report["total_missing"] = int(df.isnull().sum().sum())
    report["duplicate_rows"] = int(df.duplicated().sum())
    report["dtypes"] = df.dtypes.astype(str).to_dict()
    report["missing_pct"] = (df.isnull().sum() / len(df) * 100).round(2).to_dict()
    # Data quality score
    missing_score = max(0, 100 - report["total_missing"] / (len(df) * len(df.columns)) * 100)
    dup_score = max(0, 100 - report["duplicate_rows"] / len(df) * 100)
    report["quality_score"] = round((missing_score + dup_score) / 2, 1)
    return report


def preprocess(df: pd.DataFrame, fit=True, pipeline=None, save_path="models/preprocessor.pkl"):
    df = df.copy()
    # Drop unnecessary cols
    df.drop(columns=[c for c in DROP_COLS if c in df.columns], inplace=True, errors="ignore")

    # Convert TotalCharges if exists
    if "TotalCharges" in df.columns:
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Encode target
    y = None
    if TARGET_COL in df.columns:
        y = (df[TARGET_COL].str.strip().str.lower() == "yes").astype(int)
        df.drop(columns=[TARGET_COL], inplace=True)

    num_cols, cat_cols = get_column_types(df)

    if fit:
        num_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ])
        cat_transformer = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ])
        preprocessor = ColumnTransformer([
            ("num", num_transformer, num_cols),
            ("cat", cat_transformer, cat_cols),
        ])
        X = preprocessor.fit_transform(df)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump((preprocessor, num_cols, cat_cols), save_path)
        return X, y, preprocessor, num_cols, cat_cols
    else:
        if pipeline is None:
            preprocessor, num_cols, cat_cols = joblib.load(save_path)
        else:
            preprocessor, num_cols, cat_cols = pipeline
        X = preprocessor.transform(df)
        return X, y


def get_feature_names(preprocessor, num_cols, cat_cols):
    cat_enc = preprocessor.named_transformers_["cat"]["encoder"]
    cat_feature_names = cat_enc.get_feature_names_out(cat_cols).tolist()
    return num_cols + cat_feature_names
