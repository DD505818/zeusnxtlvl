from .base import AbstractAgent

class QuantumBoostAgent(AbstractAgent):
    def signal(self, data):
        return "BUY", 0.95

class PredictiveProphetAgent(AbstractAgent):
    def __init__(self, model):
        self.model = model
    def signal(self, data):
        return "BUY", 0.90

class VWAPScalperXAgent(AbstractAgent):
    def signal(self, data):
        return "BUY", 0.92
