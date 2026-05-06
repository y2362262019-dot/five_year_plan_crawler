import random
import threading
import time


class RateLimiter:
    def __init__(self, min_delay: float, max_delay: float):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.consecutive_errors = 0
        self._lock = threading.Lock()

    def wait(self):
        with self._lock:
            jitter = random.uniform(self.min_delay, self.max_delay)
            backoff = 2 ** min(self.consecutive_errors, 5)
            delay = jitter * backoff
        time.sleep(delay)

    def report_success(self):
        with self._lock:
            self.consecutive_errors = max(0, self.consecutive_errors - 1)

    def report_error(self):
        with self._lock:
            self.consecutive_errors += 1
