import numpy as np


class StreamStats:
    def __init__(self, max_size=100):
        self.max_size = max_size
        self.data = []

    def add(self, num):
        """Add a new number to the stream, keeping the total count within max_size."""
        if len(self.data) >= self.max_size:
            self.data.pop(0)  # Remove the oldest number
        self.data.append(num)

    def mean(self):
        """Calculate and return the mean of the numbers in the stream."""
        return round(np.mean(self.data)) if self.data else 0

    def percentile(self, percentile):
        """Calculate and return the specified percentile of the numbers in the stream."""
        if not self.data:
            return 0
        return np.percentile(self.data, percentile)
