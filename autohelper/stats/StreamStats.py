import time

import numpy as np


class StreamStats:
    last_frame_time = 0
    sleep_padding = 0

    def __init__(self, max_size=100):
        self.max_size = max_size
        self.data = []

    def add_frame(self):
        now = time.time()
        if self.last_frame_time != 0:
            if len(self.data) >= self.max_size:
                self.data.pop(0)
            self.data.append(int((now - self.last_frame_time - self.sleep_padding) * 1000))
        self.last_frame_time = now
        self.sleep_padding = 0

    def add_sleep(self, seconds):
        self.sleep_padding += seconds

    def mean(self):
        """Calculate and return the mean of the numbers in the stream."""
        return round(np.mean(self.data)) if self.data else 0

    def percentile(self, percentile):
        """Calculate and return the specified percentile of the numbers in the stream."""
        if not self.data:
            return 0
        return np.percentile(self.data, percentile)
