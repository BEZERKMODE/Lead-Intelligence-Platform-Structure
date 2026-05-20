from prometheus_client import Counter
from prometheus_client import Histogram

REQUEST_COUNT = Counter(
    "request_count",
    "Total Request Count"
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency"
)
