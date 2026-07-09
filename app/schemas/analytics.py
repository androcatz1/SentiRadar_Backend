from typing import Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class Filters(BaseModel):
    channel_title: Optional[str] = None
    topic: Optional[str] = None
    platform: Optional[str] = None
    duration_bucket: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class TopVideosQuery(BaseModel):
    metric: Literal["views", "likes", "comments_count", "engagement_rate", 'neutral', 'positive', 'negative'] = "views"
    limit: int = Field(default =10, le=100)
    order: Literal["asc", "desc"] = "desc"

class HeatmapQuery(BaseModel):
    x: Literal["channel_title", "platform", "duration_bucket", "topic"] = "channel_title"
    y: Literal["channel_title", "platform", "duration_bucket", "topic"] = "topic"
    
    metric: Literal["avg_views", "video_count", "avg_engagement_rate"] = "avg_views"  

class ScatterQuery(BaseModel):
    x: Literal["views", "likes", 'comments_count', "negative_ratio", "positive_ratio"] = "views"
    y: Literal["views", "likes", 'comments_count', "negative_ratio", "positive_ratio"] = "likes"
    color_by: Literal["topic", "channel_title", "platform", "duration_bucket",  "none"] = "none"
    limit: int = Field(default=1000, le=28000) 
