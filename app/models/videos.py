from app.models.base import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Double, BigInteger, TIMESTAMP


class VideosModel(Base):
    __tablename__ = "video_metrics_test"

    id: Mapped[int] = mapped_column(Integer, primary_key= True, autoincrement=True)
    video_id: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    tags: Mapped[str] = mapped_column(String)
    category_id: Mapped[str] = mapped_column(String)
    channel_title: Mapped[str] = mapped_column(String)
    
    # TIMESTAMP maps to python datetime
    published_at: Mapped[datetime] = mapped_column(TIMESTAMP)
    
    # BIGINT maps to BigInteger to handle large numbers safely
    views: Mapped[int] = mapped_column(BigInteger)
    likes: Mapped[int] = mapped_column(BigInteger)
    comments_count: Mapped[int] = mapped_column(BigInteger)
    
    platform: Mapped[str] = mapped_column(String)
    topic: Mapped[str] = mapped_column(String)
    
    # TIMESTAMP(0) drops milliseconds
    fetched_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False))
    
    duration: Mapped[str] = mapped_column(String)
    published_hour: Mapped[int] = mapped_column(Integer)
    published_day: Mapped[str] = mapped_column(String(9))
    published_month: Mapped[str] = mapped_column(String(9))
    
    # DOUBLE PRECISION maps to float/Double
    duration_mins: Mapped[float] = mapped_column(Double)
    engagement_rate: Mapped[float] = mapped_column(Double)
    duration_bucket: Mapped[str] = mapped_column(String)
    
    log10_views: Mapped[float] = mapped_column(Double)
    log10_likes: Mapped[float] = mapped_column(Double)
    log10_comments_count: Mapped[float] = mapped_column(Double)
    
    neutral: Mapped[int] = mapped_column(Integer)
    positive: Mapped[int] = mapped_column(Integer)
    negative: Mapped[int] = mapped_column(Integer)