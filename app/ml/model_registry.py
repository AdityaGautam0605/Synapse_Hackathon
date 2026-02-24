import joblib
import torch
from pathlib import Path

from app.ml.lstm_model import FatigueLSTM

MODEL_DIR = Path("app/models")


class ModelRegistry:
    def __init__(self):
        self.xgb_model = None
        self.scaler = None
        self.feature_names = None
        self.lstm_model = None

    def load_models(self):
        
        self.xgb_model = joblib.load(MODEL_DIR / "xgb_model.pkl")
        self.scaler = joblib.load(MODEL_DIR / "xgb_scaler.pkl")
        self.feature_names = joblib.load(MODEL_DIR / "xgb_features.pkl")

       
        self.lstm_model = FatigueLSTM()
        self.lstm_model.load_state_dict(
            torch.load(MODEL_DIR / "lstm_model.pt", map_location="cpu")
        )
        self.lstm_model.eval()


registry = ModelRegistry()