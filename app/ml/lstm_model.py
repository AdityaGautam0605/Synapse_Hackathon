import torch
import torch.nn as nn


class FatigueLSTM(nn.Module):
    def __init__(self, input_size=99, hidden_size=64, num_layers=2):
        super(FatigueLSTM, self).__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )

        self.fc = nn.Linear(hidden_size, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, (hn, cn) = self.lstm(x)
        out = self.fc(hn[-1])
        return self.sigmoid(out)