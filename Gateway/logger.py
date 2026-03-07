import time
from fastapi import Request

async def request_logger(request: Request, call_next):

    start = time.time()

    response = await call_next(request)

    latency = (time.time() - start) * 1000

    ip = request.client.host
    path = request.url.path
    status = response.status_code

    source = response.headers.get("X-Cache", "none")

    print(
        f"[REQ] ip={ip} path={path} status={status} "
        f"source={source} latency={latency:.2f}ms"
    )

    return response