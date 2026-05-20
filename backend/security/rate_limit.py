import time

class RateLimiter:

    def __init__(self):

        self.requests = {}

    def is_allowed(
        self,
        ip,
        limit=100
    ):

        now = time.time()

        if ip not in self.requests:
            self.requests[ip] = []

        self.requests[ip] = [
            t for t in self.requests[ip]
            if now - t < 60
        ]

        if len(self.requests[ip]) >= limit:
            return False

        self.requests[ip].append(now)

        return True
