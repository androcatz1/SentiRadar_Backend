from fastapi import APIRouter

from app.config.settings import Settings
from app.ml.inference.inference import predict
from app.schemas.comments import UserInputSchema

router = APIRouter(prefix="/api/inference")

@router.post("/predict")
async def make_prediction(input: UserInputSchema):

    if not input.text or input.text.strip() == "":
        return {"error": "Text was empty or invalid after cleaning pipeline ran"}
        
    result_array = predict([input.text])
    return {"prediction": Settings.SENTIMENT_MAP.get(result_array[0])}