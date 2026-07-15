import torch
import torch.nn as nn


class WalletLSTM(nn.Module):

    def __init__(
        self,
        input_size=4,
        hidden_size=64,
        num_layers=2,
        embedding_size=32,
        dropout=0.3
    ):

        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout
        )

        self.dropout = nn.Dropout(dropout)

        self.fc = nn.Linear(
            hidden_size,
            embedding_size
        )

    def forward(self, x):

        output, (hidden, cell) = self.lstm(x)

        x = hidden[-1]

        x = self.dropout(x)

        embedding = self.fc(x)

        return embedding