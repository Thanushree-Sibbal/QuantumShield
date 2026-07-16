import joblib
import torch

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

        # ---------------------------------
        # GraphSAGE
        # ---------------------------------

        try:

            self.graph_model = GraphSAGEEncoder(
                input_dim=14,
                hidden_dim=64,
                embedding_dim=32
            )

            self.graph_model.load_state_dict(
                torch.load(
                    "models/graphsage_model.pt",
                    map_location="cpu"
                )
            )

            self.graph_model.eval()

            print("✅ GraphSAGE Loaded")

        except Exception as e:

            print("❌ GraphSAGE:", e)

        # ---------------------------------
        # LSTM
        # ---------------------------------

        try:

            self.lstm_model = WalletLSTMAutoEncoder()

            self.lstm_model.load_state_dict(
                torch.load(
                    "models/lstm_autoencoder.pt",
                    map_location="cpu"
                )
            )

            self.lstm_model.eval()

            print("✅ LSTM Loaded")

        except Exception as e:

            print("❌ LSTM:", e)

        # ---------------------------------
        # Isolation Forest
        # ---------------------------------

        try:

            self.isolation_forest = joblib.load(
                "models/hybrid_isolation_forest.pkl"
            )

            print("✅ Isolation Forest Loaded")

        except Exception as e:

            print("❌ Isolation Forest:", e)


predictor = Predictor()