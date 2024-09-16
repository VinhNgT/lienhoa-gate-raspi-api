class RequestCountTracker:
    def __init__(self, max_requests: int):
        self.max_requests = max_requests
        self.requests = 0

    def is_max_requests_reached(self):
        return self.requests >= self.max_requests

    def __enter__(self):
        self.requests += 1
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.requests -= 1
