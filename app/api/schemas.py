from pydantic import BaseModel


class PredictionRequest(BaseModel):
    wallet: str


class PredictionResponse(BaseModel):
    wallet: str
    prediction: str
    risk_level: str
    anomaly_score: float


class HealthResponse(BaseModel):
    status: str