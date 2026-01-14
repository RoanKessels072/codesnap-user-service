from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from src.database import init_db
from src.nats_client import NATSClient
from prometheus_fastapi_instrumentator import Instrumentator
from src.handlers import (
    handle_get_user,
    handle_create_user,
    handle_update_user,
    handle_list_users,
)

nats_client = NATSClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting User Service...")
    init_db()
    await nats_client.connect()
    
    await nats_client.subscribe("users.get", handle_get_user)
    await nats_client.subscribe("users.create", handle_create_user)
    await nats_client.subscribe("users.update", handle_update_user)
    await nats_client.subscribe("users.list", handle_list_users)
    
    print("User Service ready!")
    
    yield
    
    print("Shutting down User Service...")
    await nats_client.close()

app = FastAPI(title="User Service", lifespan=lifespan)
Instrumentator().instrument(app).expose(app)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "user-service"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)