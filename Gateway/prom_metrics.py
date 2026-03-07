from prometheus_client import Counter

CACHE_HITS = Counter(
    "cache_hits_total",
    "Total cache hits"
)

STALE_SERVED = Counter(
    "stale_served_total",
    "Total stale cache responses"
)

REBUILDS = Counter(
    "cache_rebuilds_total",
    "Total cache rebuilds"
)

WAIT_CACHE = Counter(
    "wait_cache_total",
    "Requests waiting for cache rebuild"
)

SERVICE_CALLS = Counter(
    "service_calls_total",
    "Backend service calls"
)