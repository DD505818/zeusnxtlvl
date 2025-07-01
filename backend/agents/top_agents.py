from .base import AbstractAgent
import random

class QuantumBoostAgent(AbstractAgent):
    def signal(self, data):
        return ("BUY", random.random())

class PredictiveProphetAgent(AbstractAgent):
    def __init__(self, model=None):
        self.model = model

    def signal(self, data):
        return ("HOLD", random.random())

class VWAPScalperXAgent(AbstractAgent):
    def signal(self, data):
        return ("SELL", random.random())
