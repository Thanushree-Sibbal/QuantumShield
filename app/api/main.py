from fastapi import FastAPI

from app.api.routes import router
from app.api.predictor import predictor

app = FastAPI(
    title="QuantumShield API",
    description="Hybrid AI-based Ethereum Wallet Risk Detection",
    version="1.0.0"
)

app.include_router(router)