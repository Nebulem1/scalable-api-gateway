from fastapi import FastAPI
from router import fetch_products,fetch_users
from cache import get_cache, set_cache, acquire_lock, release_lock, SOFT_TTL, HARD_TTL
import asyncio
from prometheus_client import generate_latest
from fastapi.responses import Response

from rate_limiter import token_bucket_limiter
from logger import request_logger
from fastapi.responses import JSONResponse
from prom_metrics import *
import socket

HOSTNAME = socket.gethostname()

app = FastAPI()

app.middleware("http")(request_logger)
app.middleware("http")(token_bucket_limiter)

async def rebuild_cache(cache_key, lock_key):

    data = await fetch_products()
    REBUILDS.inc()
    if "error" not in data:
        set_cache(cache_key, data)

    release_lock(lock_key)


@app.get("/products")
async def get_products():

    cache_key = "cache:products"
    lock_key = "lock:products"

    data, age = get_cache(cache_key)

    # no cache
    if data is None:

        if acquire_lock(lock_key):

            data = await fetch_products()
            REBUILDS.inc()
            if "error" not in data:
                set_cache(cache_key, data)

            release_lock(lock_key)

            return JSONResponse(
            content={"data": data},
            headers={"X-Cache": "rebuild"}
        )

        else:
            WAIT_CACHE.inc()
            while True:
                data, age = get_cache(cache_key)
                if data:
                   return JSONResponse(
                    content={"data": data},
                    headers={"X-Cache": "wait"}
                )

                await asyncio.sleep(0.1)

    # fresh
    if age < SOFT_TTL:
        CACHE_HITS.inc()
        return JSONResponse(
                content={"data": data},
                headers={"X-Cache": "fresh"}
            )

    # stale
    if age < HARD_TTL:

        if acquire_lock(lock_key):
            asyncio.create_task(rebuild_cache(cache_key, lock_key))
        STALE_SERVED.inc()
        return JSONResponse(
            content={"data": data},
            headers={"X-Cache": "stale"}
        )

    # hard expired
    if acquire_lock(lock_key):

        data = await fetch_products()
        REBUILDS.inc()
        if "error" not in data:
            set_cache(cache_key, data)

        release_lock(lock_key)

        return JSONResponse(
            content={"data": data},
            headers={"X-Cache": "rebuild"}
        )

    else:
        WAIT_CACHE.inc()
        while True:
            data, age = get_cache(cache_key)
            if data:
                return JSONResponse(
                content={"data": data},
                headers={"X-Cache": "wait"}
            )

            await asyncio.sleep(0.1)

@app.get("/who")
def who():

    return {
        "gateway": HOSTNAME
    }

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.get("/users")
async def get_users():
    data = await fetch_users()
    return data