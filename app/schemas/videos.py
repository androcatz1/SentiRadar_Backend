import re

from pydantic import BaseModel, model_validator, Field
from app.config.settings import Settings

class UserInputSchema(BaseModel):
    url: str = Field(...)
    video_id: str = None

    @model_validator(mode='before')
    @classmethod
    def validate_and_extract(cls, data):
        data = dict(data)
        url = data.get("url", "")
        
        match = re.search(Settings.YOUTUBE_REGEX, url)
        if not match:
            raise ValueError("Invalid YouTube url!")
        
        data['video_id'] = match.group(1)

        return data