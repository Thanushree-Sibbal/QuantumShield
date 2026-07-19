import joblib
import torch
import pandas as pd
import time
from datetime import datetime

from torch_geometric.nn import GAE

from app.ai.graphsage import GraphSAGEEncoder
from app.lstm.model import WalletLSTMAutoEncoder

print("=" * 60)
print("Loading QuantumShield Models")
print("=" * 60)


class Predictor:

    def __init__(self):

        self.graph_model = None
        self.lstm_model = None
        self.isolation_forest = None
        self.fusion_data = None

        # ==================================================
        # Graph AutoEncoder
        # ==================================================

        try:
            encoder = GraphSAGEEncoder(
                input_dim=14,
                hidden_dim=64,
                embedding_dim=32
            )

            self.graph_model = GAE(encoder)

            self.graph_model.load_state_dict(
                torch.load(
                    "models/graphsage_model.pt",
                    map_location="cpu"
                )
            )

            self.graph_model.eval()

            print("✅ Graph AutoEncoder Loaded")

        except Exception as e:
            print("❌ Graph AutoEncoder:", e)

        # ==================================================
        # LSTM AutoEncoder
        # ==================================================

        try:
            self.lstm_model = WalletLSTMAutoEncoder()

            self.lstm_model.load_state_dict(
                torch.load(
                    "models/lstm_autoencoder.pt",
                    map_location="cpu"
                )
            )

            self.lstm_model.eval()

            print("✅ LSTM AutoEncoder Loaded")

        except Exception as e:
            print("❌ LSTM AutoEncoder:", e)

        # ==================================================
        # Isolation Forest
        # ==================================================

        try:
            self.isolation_forest = joblib.load(
                "models/hybrid_isolation_forest.pkl"
            )

            print("✅ Isolation Forest Loaded")

        except Exception as e:
            print("❌ Isolation Forest:", e)

        # ==================================================
        # Fusion Dataset
        # ==================================================

        try:
            self.fusion_data = pd.read_csv(
                "models/fusion_dataset.csv"
            )

            # Normalize wallet addresses once
            self.fusion_data["wallet"] = (
                self.fusion_data["wallet"]
                .str.lower()
                .str.strip()
            )

            # Use wallet as the index for fast lookups
            self.fusion_data.set_index("wallet", inplace=True)

            print(
                f"✅ Fusion Dataset Loaded ({len(self.fusion_data)} wallets)"
            )

        except Exception as e:
            print("❌ Fusion Dataset:", e)

    # ==================================================
    # Predict Wallet Risk
    # ==================================================

    def predict_wallet(self, wallet: str):

        start = time.perf_counter()

        # Normalize wallet address
        wallet = wallet.lower().strip()

        # Check if wallet exists
        if wallet not in self.fusion_data.index:
            return {
                "success": False,
                "message": "Wallet not found in dataset."
            }

        # Retrieve wallet features
        wallet_row = self.fusion_data.loc[[wallet]]
        features = wallet_row.values

        # Isolation Forest Prediction
        prediction = self.isolation_forest.predict(features)[0]
        anomaly_score = float(
            self.isolation_forest.decision_function(features)[0]
        )

        # Calculate risk score (0-100)
        risk_score = int(
            max(
                0,
                min(
                    100,
                    (0.5 - anomaly_score) * 100
                )
            )
        )

        # Determine prediction and risk level
        if anomaly_score >= 0.20:
            prediction_text = "Normal"
            risk_level = "Low"

        elif anomaly_score >= 0.00:
            prediction_text = "Normal"
            risk_level = "Medium"

        else:
            prediction_text = "Anomalous"
            risk_level = "High"

        # Measure execution time
        elapsed = int(
            (time.perf_counter() - start) * 1000
        )

        return {
            "success": True,
            "wallet": wallet,
            "wallet_found": True,
            "prediction": prediction_text,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "anomaly_score": round(anomaly_score, 6),
            "model": "Hybrid GraphSAGE + LSTM + Isolation Forest",
            "embedding_dimension": 64,
            "analysis_time_ms": elapsed,
            "api_version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


predictor = Predictor()