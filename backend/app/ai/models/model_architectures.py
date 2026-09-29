"""
Model Architectures for Agricultural Price Forecasting:
1. Linear Regression (Baseline)
2. Random Forest Regressor (Ensemble ML)
3. PyTorch LSTM Neural Network (Sequential DL)
"""

import torch
import torch.nn as nn
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def get_baseline_model():
    """Baseline Linear Regression Model"""
    return LinearRegression()

def get_random_forest_model():
    """
    Random Forest Regressor:
    - 100 Decision Trees
    - max_depth=20 to prevent overfitting
    - min_samples_split=5
    - Parallel execution (n_jobs=-1)
    """
    return RandomForestRegressor(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        verbose=1
    )

class LSTMPricePredictor(nn.Module):
    """
    PyTorch Deep Learning LSTM Architecture for Agricultural Price Forecasting:
    - Input Layer: Feature dimension D
    - LSTM Layer 1: 64 hidden units with sequence return
    - LSTM Layer 2: 32 hidden units
    - Dropout Layer: p=0.2 (regularization)
    - Fully Connected Layer 1: 32 -> 16 + ReLU activation
    - Output Projection Layer: 16 -> 1 (Predicted Modal Price)
    """
    def __init__(self, input_dim, hidden_dim1=64, hidden_dim2=32, dropout=0.2):
        super(LSTMPricePredictor, self).__init__()
        self.lstm1 = nn.LSTM(input_dim, hidden_dim1, batch_first=True)
        self.lstm2 = nn.LSTM(hidden_dim1, hidden_dim2, batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(hidden_dim2, 16)
        self.relu = nn.ReLU()
        self.fc_out = nn.Linear(16, 1)
        
    def forward(self, x):
        # x shape: (batch_size, seq_len, input_dim)
        out, _ = self.lstm1(x)
        out, (hn, _) = self.lstm2(out)
        # Take the hidden state of the last time step
        last_hidden = hn[-1]
        out = self.dropout(last_hidden)
        out = self.fc1(out)
        out = self.relu(out)
        out = self.fc_out(out)
        return out.squeeze(-1)
