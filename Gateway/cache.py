import redis
import json
import time

r = redis.Redis(host="redis", port=6379, decode_responses=True)

SOFT_TTL = 5
HARD_TTL = 20
LOCK_EXPIRE = 10


def get_cache(key):

    raw = r.get(key)

    if not raw:
        return None, None

    payload = json.loads(raw)

    data = payload["data"]
    created_at = payload["created_at"]

    age = time.time() - created_at

    return data, age


def set_cache(key, value):

    payload = {
        "data": value,
        "created_at": time.time()
    }

    r.set(key, json.dumps(payload))


def acquire_lock(lock_key):

    return r.set(lock_key, "1", nx=True, ex=LOCK_EXPIRE)


def release_lock(lock_key):

    r.delete(lock_key)