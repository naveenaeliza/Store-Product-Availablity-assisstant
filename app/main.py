from fastapi import FastAPI
from app.api.routes import router
import app.logging_config

app = FastAPI(
    title="Store Product Availability Assistant",
    version="1.0.0"
)

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Store Product Availability Assistant API is running!"
    }