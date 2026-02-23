import torch
import numpy as np
from app.ml.model_registry import registry


def predict_sequence(sequence: list) -> float:
    """
    sequence: list of shape (30, 99)
    Returns temporal fatigue risk (0–1).
    """

    model = registry.lstm_model

    arr = np.array(sequence, dtype=np.float32)

    if arr.shape != (30, 99):
        raise ValueError("Sequence must be shape (30, 99)")

    arr = arr.reshape(1, 30, 99)

    tensor = torch.tensor(arr)

    with torch.no_grad():
        output = model(tensor)

    return float(output.item())