from pydantic import BaseModel


class PredictionRequest(BaseModel):
    wallet: str


class PredictionResponse(BaseModel):
    success: bool
    wallet: str
    wallet_found: bool
    prediction: str
    risk_level: str
    risk_score: int
    anomaly_score: float
    model: str
    embedding_dimension: int
    analysis_time_ms: int
    api_version: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str