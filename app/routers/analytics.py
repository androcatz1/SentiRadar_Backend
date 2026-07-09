from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.database.connection import get_db_static

from app.schemas.analytics import Filters, TopVideosQuery, HeatmapQuery, ScatterQuery

from app.services.comments import get_random_comment_stream_samples
from app.services.videos import get_filtered_video_ids
from app.services.analytics import (get_video_dashboard_stats, get_stats, get_top_videos, get_top_keywords, 
                                    get_topic_summary_table, get_generic_heatmap, get_generic_scatter_plot,
                                    get_dashboard_filter_options, get_chart_query_options, get_kpi_dashboard,
                                    get_engagement_dashboard, get_sentiment_dashboard)

router = APIRouter(prefix="/api/analytics")

@router.get("/overview")
async def dashboard_overview(db: AsyncSession = Depends(get_db_static), filters: Filters = Depends()):
    results = await get_video_dashboard_stats(db, filters)
    return results

@router.get("/distribution/{column}")
async def column_distribution(column: Literal["topic","channel_title","platform","duration_bucket"], 
                              db: AsyncSession = Depends(get_db_static), filters: Filters = Depends()):
    results = await get_stats(column, db, filters)
    return results

@router.get("/top-videos")
async def top_videos(db: AsyncSession = Depends(get_db_static), 
                              sort_params: TopVideosQuery = Depends(), filters: Filters = Depends()):
    results = await get_top_videos(db, filters, sort_params)
    return results

@router.get("/keywords")
async def keywords(db: AsyncSession = Depends(get_db_static), filters: Filters = Depends()):
    video_ids = await get_filtered_video_ids(db, filters)
    results = await get_top_keywords(db, video_ids)
    return results

@router.get("/comment-samples")
async def comments(db: AsyncSession = Depends(get_db_static), filters: Filters = Depends()):
    video_ids = await get_filtered_video_ids(db, filters)
    results = await get_random_comment_stream_samples(db, video_ids)
    return results

@router.get("/summary")
async def topic_summary(db: AsyncSession = Depends(get_db_static), filters: Filters = Depends()):
    results = await get_topic_summary_table(db, filters)
    return results

@router.get("/heatmap")
async def heatmap(db: AsyncSession = Depends(get_db_static), filters: Filters = Depends(),
                  heatmap_params: HeatmapQuery = Depends()):
    results = await get_generic_heatmap(db, filters, heatmap_params)
    return results

@router.get("/scatter")
async def scatter_plot(db: AsyncSession = Depends(get_db_static), filters: Filters = Depends(),
                  scatter_params: ScatterQuery = Depends()):
    results = await get_generic_scatter_plot(db, filters, scatter_params)
    return results

@router.get("/filter-options")
async def get_all_dropdown_filters(db: AsyncSession = Depends(get_db_static)):
    results = await get_dashboard_filter_options(db)
    chart_options = get_chart_query_options()
    return {
        "filters": results,
        "chart_options": chart_options
    }

# -----------------------------------------------------------------------------------------------------------
@router.get("/dashboard/kpi")
async def get_master_kpi_dashboard(db: AsyncSession = Depends(get_db_static), filters: Filters = Depends()):
    results = await get_kpi_dashboard(db, filters)
    return results

@router.get("/dashboard/engagement")
async def get_full_engagement_dashboard(db: AsyncSession = Depends(get_db_static), filters: Filters = Depends()):
    results = await get_engagement_dashboard(db, filters)
    return results

@router.get("/dashboard/sentiment")
async def get_full_sentiment_dashboard(db: AsyncSession = Depends(get_db_static), filters: Filters = Depends()):
    results = await get_sentiment_dashboard(db, filters)
    return results
# -----------------------------------------------------------------------------------------------------------