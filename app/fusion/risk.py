import joblib
import os
import pandas as pd
from sklearn.ensemble import IsolationForest

print("=" * 60)
print("Hybrid Wallet Risk Detection")
print("=" * 60)

# --------------------------------------------------
# Load Fusion Dataset
# --------------------------------------------------

df = pd.read_csv("models/fusion_dataset.csv")

print("Wallets:", len(df))

# --------------------------------------------------
# Extract Features
# --------------------------------------------------

X = df.drop(columns=["wallet"])

print("Feature Shape:", X.shape)

# --------------------------------------------------
# Train Isolation Forest
# --------------------------------------------------

model = IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42
)

print()
print("Training Isolation Forest...")

model.fit(X)
joblib.dump(
    model,
    "models/hybrid_isolation_forest.pkl"
)

print("Training Complete!")

# --------------------------------------------------
# Predictions
# --------------------------------------------------

prediction = model.predict(X)

score = model.decision_function(X)

# --------------------------------------------------
# Risk Levels
# --------------------------------------------------

risk = []

for p in prediction:
    if p == -1:
        risk.append("High")
    else:
        risk.append("Low")

# --------------------------------------------------
# Save Results
# --------------------------------------------------

result = pd.DataFrame({
    "wallet": df["wallet"],
    "prediction": prediction,
    "anomaly_score": score,
    "risk_level": risk
})

os.makedirs("models", exist_ok=True)

result.to_csv(
    "models/hybrid_wallet_risk_scores.csv",
    index=False
)

print()
print(result.head())

print()
print("High Risk :", (result["prediction"] == -1).sum())
print("Normal    :", (result["prediction"] == 1).sum())

print()
print("Saved:")
print("models/hybrid_wallet_risk_scores.csv")

print("=" * 60)