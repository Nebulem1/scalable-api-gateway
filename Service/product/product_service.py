from fastapi import FastAPI
import time

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Phone"},
    {"id": 3, "name": "Headphones"}
]

@app.get("/products")
def get_products():
    time.sleep(3)
    return {"products": products}