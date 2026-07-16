import torch
import torch.nn as nn


class WalletLSTMAutoEncoder(nn.Module):

    def __init__(
        self,
        input_size=4,
        hidden_size=64,
        embedding_size=32,
        num_layers=2,
        dropout=0.3,
        sequence_length=20
    ):

        super().__init__()

        self.sequence_length = sequence_length

        # -----------------------
        # Encoder
        # -----------------------

        self.encoder = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout
        )

        self.embedding = nn.Linear(
            hidden_size,
            embedding_size
        )

        # -----------------------
        # Decoder
        # -----------------------

        self.decoder_input = nn.Linear(
            embedding_size,
            hidden_size
        )

        self.decoder = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout
        )

        self.output = nn.Linear(
            hidden_size,
            input_size
        )

    def forward(self, x):

        # Encoder
        _, (hidden, _) = self.encoder(x)

        embedding = self.embedding(hidden[-1])

        # Decoder
        decoder_input = self.decoder_input(embedding)

        decoder_input = decoder_input.unsqueeze(1)

        decoder_input = decoder_input.repeat(
            1,
            self.sequence_length,
            1
        )

        decoded, _ = self.decoder(decoder_input)

        reconstruction = self.output(decoded)

        return reconstruction, embedding