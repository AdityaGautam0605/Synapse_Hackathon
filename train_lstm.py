import torch
import torch.nn as nn
import numpy as np
from pathlib import Path

from app.ml.lstm_model import FatigueLSTM


# ----- MOCK DATA CREATION -----
# Replace this later with real sequence extraction
# For now, we simulate 30-frame sequences

num_samples = 2000
sequence_length = 30
feature_dim = 99

X = np.random.randn(num_samples, sequence_length, feature_dim).astype(np.float32)

# Simulated binary labels
y = (np.random.rand(num_samples) > 0.7).astype(np.float32)


# ----- TENSOR CONVERSION -----
X_tensor = torch.tensor(X)
y_tensor = torch.tensor(y).view(-1, 1)


# ----- MODEL -----
model = FatigueLSTM()
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


# ----- TRAIN LOOP -----
epochs = 10

for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_tensor)
    loss = criterion(outputs, y_tensor)
    loss.backward()
    optimizer.step()

    print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")


# ----- SAVE MODEL -----
Path("app/models").mkdir(parents=True, exist_ok=True)

torch.save(model.state_dict(), "app/models/lstm_model.pt")

print("LSTM model saved successfully.")