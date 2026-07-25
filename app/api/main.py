from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.api.predictor import predictor
from app.api.websocket import router as websocket_router

app = FastAPI(
    title="QuantumShield API",
    description="Hybrid AI-based Ethereum Wallet Risk Detection",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Existing API routes
app.include_router(router)

# WebSocket routes
app.include_router(websocket_router)