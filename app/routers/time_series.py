from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.database.connection import get_db_ts

from app.schemas.analytics import Filters

from app.services.time_series import get_consolidated_time_series_data, get_dynamic_aggregated_time_series

router = APIRouter(prefix="/api/timeseries")

@router.get("/video-metrics")
async def get_time_series_analytics(filters: Filters = Depends(),db: AsyncSession = Depends(get_db_ts)):
    data = await get_consolidated_time_series_data(db, filters)
    
    return data

@router.get("/aggregate/{group_by}")
async def get_dashboard_aggregated_charts(group_by: Literal["topic", "duration_bucket", "channel_title", "platform", 'none'],
                                          filters: Filters = Depends(), db: AsyncSession = Depends(get_db_ts)):
    data = await get_dynamic_aggregated_time_series(db, filters, group_by)
    return data
