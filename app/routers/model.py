from fastapi import APIRouter, HTTPException, Query

from app.config.model_results import MODELS
from app.ml.inference.inference import predict_sentiment
from app.schemas.comments import UserInputSchema
from app.services.model import load_overview, load_performance, load_tuning
from typing import Literal

router = APIRouter(prefix="/api/model")

@router.post("/predict")
async def make_prediction(input: UserInputSchema):
    if not input.text or input.text.strip() == "":
        raise HTTPException(status_code=422, detail="Text was empty or invalid after cleaning.")

    try:
        result = predict_sentiment(input.text, input.model_key.lower(), MODELS)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result

@router.get("/overview")
def get_overview():
    return load_overview()

@router.get("/performance/{model}")
def get_performance(model: Literal['malaya', 'heuristic', 'merged']):
    return load_performance(model)

@router.get("/tuning/{model}")
def get_tuning(model: Literal['malaya', 'heuristic', 'merged']):
    return load_tuning(model)
