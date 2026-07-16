from fastapi import APIRouter

from app.api.schemas import HealthResponse

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Welcome to QuantumShield API",
        "status": "running"
    }


@router.get(
    "/health",
    response_model=HealthResponse
)
def health():

    return HealthResponse(
        status="healthy"
    )