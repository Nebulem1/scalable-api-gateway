from fastapi import FastAPI

app = FastAPI()

users = [
    {"id": 1, "name": "Hitesh"},
    {"id": 2, "name": "Aman"},
    {"id": 3, "name": "Ravi"}
]

@app.get("/users")
def get_users():
    return {"users": users}