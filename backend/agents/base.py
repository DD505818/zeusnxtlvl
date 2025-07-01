class AbstractAgent:
    def signal(self, data):
        """Return a trading signal and confidence."""
        raise NotImplementedError
