from __future__ import annotations
import pandas as pd
from .base import AbstractAgent

class QuantumBoostAgent(AbstractAgent):
    def signal(self, df: pd.DataFrame):
        if len(df) < 20:
            return "HOLD", 0.0
        if df['close'].iloc[-1] > df['close'].iloc[-20]:
            return "BUY", 0.95
        return "HOLD", 0.5

class PredictiveProphetAgent(AbstractAgent):
    def __init__(self, model=None):
        self.model = model

    def signal(self, df: pd.DataFrame):
        return "BUY", 0.96 if len(df) % 2 == 0 else ("HOLD", 0.5)

class VWAPScalperXAgent(AbstractAgent):
    def signal(self, df: pd.DataFrame):
        return "BUY", 0.97 if df['close'].iloc[-1] % 2 == 0 else ("HOLD", 0.5)
