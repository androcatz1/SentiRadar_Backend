from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, desc

from app.models.videos import VideosModel
from app.schemas.analytics import Filters
from app.services.helpers import query_filters

# to check new input if exist
async def check_video_id_exist(db: AsyncSession, video_id:str):
    query = select(exists().where(VideosModel.video_id == video_id))
    
    result = await db.execute(query)
    
    return result.scalar() or False


# for comments filtering in analytics and videos
async def get_filtered_video_ids(db: AsyncSession, filters: Filters):
    query = select(VideosModel.video_id)

    query = query_filters(query, filters)

    result = await db.execute(query)

    return list(result.scalars().all())


async def get_filtered_video_details_list(db: AsyncSession, filters: Filters) -> list[dict]:
    # 1. Select ONLY the specific columns needed for your frontend dropdown/list selector
    query = select(
        VideosModel.video_id,
        VideosModel.title,
        VideosModel.channel_title
    )

    # 2. Apply your shared dynamic query filters
    query = query_filters(query, filters)

    query = query.order_by(desc(VideosModel.fetched_at))

    # 3. Execute the query
    result = await db.execute(query)
    
    # 4. Use .mappings().all() to convert the rows to standard dictionaries instantly
    # This automatically matches your target: [{"video_id": "...", "title": "...", "channel_title": "..."}]
    return [dict(row) for row in result.mappings().all()]    

# Video level Analysis--------------------------------------------------------------------------------------------
async def get_single_video_overview(db: AsyncSession, video_id: str):
    # 1. Query for the exact video matching the provided video_id
    query = select(VideosModel).where(VideosModel.video_id == video_id)
    
    result = await db.execute(query)
    video = result.scalar_one_or_none()
    
    # 2. Return None if the video doesn't exist so the router can trigger a 404
    if not video:
        return None
        
    # 3. Format the data to nest sentiment tracking properties cleanly
    return {
        "video_id": video.video_id,
        "title": video.title,
        "channel_title": video.channel_title,
        # Convert datetime to ISO string format for safe frontend rendering
        "published_at": video.published_at.isoformat() if video.published_at else None,
        "views": int(video.views or 0),
        "likes": int(video.likes or 0),
        "comments_count": int(video.comments_count or 0),
        "duration_mins": round(float(video.duration_mins or 0.0), 2),
        "engagement_rate": round(float(video.engagement_rate or 0.0), 4),
        "platform": video.platform,
        "topic": video.topic or "Unassigned",
        "sentiment": {
            "positive": int(video.positive or 0),
            "neutral": int(video.neutral or 0),
            "negative": int(video.negative or 0)
        }
    }

