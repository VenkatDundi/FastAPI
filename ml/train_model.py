"""
Run this script once to train and save the model.
No need for real data — we generate synthetic training data.
"""
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ── Generate synthetic loan data ─────────────────────────────
np.random.seed(42)
n_samples = 1000

age              = np.random.randint(19, 79, n_samples)
annual_income    = np.random.uniform(20000, 200000, n_samples)
loan_amount      = np.random.uniform(5000, 300000, n_samples)
credit_score     = np.random.randint(300, 850, n_samples)

# Simple approval rule — high income + good credit score = approved
approved = (
    (credit_score > 650) &
    (annual_income > loan_amount * 0.3)
).astype(int)

X = np.column_stack([
    age, annual_income, loan_amount, credit_score
])
y = approved

# ── Train the model ───────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Model trained. Accuracy: {accuracy:.2%}")

# ── Save the model ────────────────────────────────────────────
# ✅ Correct — saves to models/ folder
from pathlib import Path

# Create models/ folder if it does not exist
models_dir = Path(__file__).parent.parent / "models"
models_dir.mkdir(exist_ok=True)

model_path = models_dir / "loan_model.pkl"
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")