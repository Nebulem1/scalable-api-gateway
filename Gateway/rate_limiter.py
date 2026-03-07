import redis
import time
from fastapi import Request
from fastapi.responses import JSONResponse

r = redis.Redis(host="redis", port=6379, decode_responses=True)

LIMITS = {
    "/products": (20, 5),   # capacity, refill rate/sec
}

async def token_bucket_limiter(request: Request, call_next):

    ip = request.client.host
    path = request.url.path

    capacity, refill = LIMITS.get(path, (50, 10))

    key = f"bucket:{ip}:{path}"

    now = time.time()

    bucket = r.hgetall(key)

    if bucket:
        tokens = float(bucket["tokens"])
        last = float(bucket["last"])
    else:
        tokens = capacity
        last = now

    elapsed = now - last

    tokens = min(capacity, tokens + elapsed * refill)

    if tokens < 1:
        return JSONResponse(
            status_code=429,
            content={"error": "rate limit exceeded"}
        )

    tokens -= 1

    r.hset(key, mapping={
        "tokens": tokens,
        "last": now
    })

    r.expire(key, 60)

    response = await call_next(request)

    return response