"""
RetentionAI — Entry Point
Run: python main.py
"""
import os
import sys
import subprocess


def main():
    print("=" * 55)
    print("  🔮 RetentionAI — Customer Churn Intelligence Platform")
    print("=" * 55)

    # Generate sample data if missing
    data_path = os.path.join("data", "customer_churn.csv")
    if not os.path.exists(data_path):
        print("\n📦 Generating sample dataset…")
        from data.generate_data import generate_sample_data
        df = generate_sample_data(1000)
        os.makedirs("data", exist_ok=True)
        df.to_csv(data_path, index=False)
        print(f"   ✅ Saved to {data_path}  ({len(df):,} rows)")

    os.makedirs("models", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    print("\n🚀 Launching Streamlit dashboard…")
    print("   Open your browser at  http://localhost:8501\n")

    app_path = os.path.join("app", "streamlit_app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], check=True)


if __name__ == "__main__":
    main()
