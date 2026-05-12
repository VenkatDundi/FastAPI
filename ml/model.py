"""
Model loading and prediction logic.
Model is loaded ONCE here — never inside an endpoint function.
"""
import joblib
import numpy as np

# ── Load model at module import time (server startup) ─────────
print("Loading model...")
# ✅ Correct — builds absolute path from file location
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / "models" / "loan_model.pkl"
model = joblib.load(MODEL_PATH)
print("Model loaded successfully.")


def predict_loan_approval(
    age: int,
    annual_income: float,
    loan_amount: float,
    credit_score: int
) -> dict:
    """
    Run prediction and return structured result.
    Never receives PII — only model-relevant features.
    """
    features = np.array([[
        age, annual_income, loan_amount, credit_score
    ]])

    prediction   = model.predict(features)[0]
    probability  = model.predict_proba(features)[0]
    confidence   = round(float(max(probability)), 2)

    return {
        "approved":   bool(prediction == 1),
        "confidence": confidence,
        "decision":   "Approved" if prediction == 1 else "Rejected"
    }