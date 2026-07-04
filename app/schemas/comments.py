from pydantic import BaseModel
from typing import Optional

class FilterSchema(BaseModel):
    video_id: Optional[str] = None
    label: Optional[int] = None  