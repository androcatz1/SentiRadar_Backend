from sqlalchemy.ext.asyncio import AsyncSession

from app.models.videos_time_series import VideosTimeSeriesModel
from app.models.videos import VideosModel
from app.schemas.analytics import Filters

def query_filters(query, filters:Filters):
    if filters.channel_title:
        query = query.where(VideosModel.channel_title == filters.channel_title)
    if filters.topic:
        query = query.where(VideosModel.topic == filters.topic)
    if filters.platform:
        query = query.where(VideosModel.platform == filters.platform)
    if filters.duration_bucket:
        query = query.where(VideosModel.duration_bucket == filters.duration_bucket)
    if filters.start_date:
        query = query.where(VideosModel.published_at >= filters.start_date)
    if filters.end_date:
        query = query.where(VideosModel.published_at <= filters.end_date)

    return query

def query_filters_ts(query, filters:Filters):
    if filters.channel_title:
        query = query.where(VideosTimeSeriesModel.channel_title == filters.channel_title)
    if filters.topic:
        query = query.where(VideosTimeSeriesModel.topic == filters.topic)
    if filters.platform:
        query = query.where(VideosTimeSeriesModel.platform == filters.platform)
    if filters.duration_bucket:
        query = query.where(VideosTimeSeriesModel.duration_bucket == filters.duration_bucket)
    if filters.start_date:
        query = query.where(VideosTimeSeriesModel.published_at >= filters.start_date)
    if filters.end_date:
        query = query.where(VideosTimeSeriesModel.published_at <= filters.end_date)

    return query