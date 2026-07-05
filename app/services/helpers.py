from sqlalchemy.ext.asyncio import AsyncSession

from app.models.videos import VideosModel
from app.schemas.analytics import Filters

def query_filters(query, filters:Filters):
    if filters.channel_title:
        query = query.where(VideosModel.channel_title == filters.channel_title)
    if filters.topic:
        query = query.where(VideosModel.topic == filters.topic)
    if filters.platform:
        query = query.where(VideosModel.platform == filters.platform)
    if filters.start_date:
        query = query.where(VideosModel.published_at >= filters.start_date)
    if filters.end_date:
        query = query.where(VideosModel.published_at <= filters.end_date)

    return query