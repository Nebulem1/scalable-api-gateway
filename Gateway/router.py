import httpx
from prom_metrics import SERVICE_CALLS
PRODUCT_SERVICE = "http://product_service:8001"
USER_SERVICE = "http://user_service:8002"

async def fetch_products():
    try:
        async with httpx.AsyncClient() as client:
            SERVICE_CALLS.inc()
            response = await client.get(f"{PRODUCT_SERVICE}/products")
            return response.json()

    except httpx.ConnectError:
        return {"error": "Product service unavailable"}

async def fetch_users():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{USER_SERVICE}/users")
            return response.json()
    except httpx.ConnectError:
        return {"error": "Product service unavailable"}