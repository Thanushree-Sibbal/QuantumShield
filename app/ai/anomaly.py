import pandas as pd
from sklearn.ensemble import IsolationForest

print("=" * 60)
print("Loading Wallet Embeddings")
print("=" * 60)

# -------------------------------------------------
# Load embeddings
# -------------------------------------------------

df = pd.read_csv("models/wallet_embeddings.csv")

wallets = df["wallet"]

X = df.drop(columns=["wallet"])

print("Wallets :", len(wallets))
print("Features:", X.shape[1])

# -------------------------------------------------
# Train Isolation Forest
# -------------------------------------------------

print()
print("Training Isolation Forest...")
print()

iso = IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42,
    n_jobs=-1
)

iso.fit(X)

print("Training Complete!")

print("=" * 60)
# -------------------------------------------------
# Generate anomaly scores
# -------------------------------------------------

print("Generating anomaly scores...")
predictions = iso.predict(X)
scores = iso.decision_function(X)

result = pd.DataFrame({
    "wallet": wallets,
    "prediction": predictions,
    "anomaly_score": scores
})

# ------------------------------------------
# Assign Risk Levels
# ------------------------------------------

def risk_level(row):

    if row["prediction"] == -1:

        if row["anomaly_score"] < -0.05:
            return "High"

        return "Medium"

    return "Low"

result["risk_level"] = result.apply(
    risk_level,
    axis=1
)

print()

print(result.head())

print()

print("High Risk :", (result["risk_level"] == "High").sum())

print("Medium Risk :", (result["risk_level"] == "Medium").sum())

print("Low Risk :", (result["risk_level"] == "Low").sum())

print("=" * 60)

# ------------------------------------------
# Save results
# ------------------------------------------

result.to_csv(
    "models/wallet_risk_scores.csv",
    index=False
)

print("Saved: models/wallet_risk_scores.csv")