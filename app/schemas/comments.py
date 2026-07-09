import pandas as pd

from app.etl.transform.comments import run_pipeline
from pydantic import BaseModel, Field, model_validator
from typing import Optional

class PaginationParams(BaseModel):
    limit: int = Field(default=20, ge=1, le=50) # Enforce a safe cap max of 50 per page
    offset: int = Field(default=0, ge=0)

class UserInputSchema(BaseModel):
    text: str = None

    @model_validator(mode = "before")
    @classmethod
    def clean_text(cls, data: dict):
        text_value = data.get("text")
        
        # 2. Guard against empty string or None values
        if not text_value:
            return data
            
        # 3. Adapt your previous DataFrame pipeline logic for a single string
        # Wrap the single text string into a temporary DataFrame
        df_temp = pd.DataFrame([{"text": text_value}])
        
        # Run your existing cleaning function on the DataFrame
        df_cleaned = run_pipeline(df_temp)
        
        # 4. Check if the pipeline completely wiped out the text (e.g. all punctuation/emojis)
        if df_cleaned.empty or "text" not in df_cleaned.columns or df_cleaned["text"].isna().all():
            data["text"] = ""  # Or raise a ValueError if you want to block the request
        else:
            # Extract the single cleaned string out of the processed DataFrame
            data["text"] = df_cleaned["text"].iloc[0]
            
        # 5. Return the modified dictionary back to Pydantic
        return data
