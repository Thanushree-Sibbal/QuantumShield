from fastapi import APIRouter, HTTPException

from app.api.predictor import predictor
from app.api.schemas import (
    PredictionRequest,
    PredictionResponse,
    HealthResponse
)

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


@router.post(
    "/predict",
    response_model=PredictionResponse
)
def predict(request: PredictionRequest):

    result = predictor.predict_wallet(request.wallet)

    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )
    return PredictionResponse(**result)
   # return PredictionResponse(
    #    success=result["success"],
     #   wallet=result["wallet"],
      #  prediction=result["prediction"],
       # risk_level=result["risk_level"],
        #anomaly_score=result["anomaly_score"]
   # )