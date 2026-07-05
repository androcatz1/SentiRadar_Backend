from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists

from app.models.videos import VideosModel
from app.schemas.analytics import Filters
from app.services.helpers import query_filters


async def check_video_id_exist(db: AsyncSession, video_id:str):
    query = select(exists().where(VideosModel.video_id == video_id))
    
    result = await db.execute(query)
    
    return result.scalar() or False


async def get_filtered_video_ids(db: AsyncSession, filters: Filters):
    query = select(VideosModel.video_id)
# -----------------------------------------------------------------------------
    query = query_filters(db, filters)
# -----------------------------------------------------------------------------
    result = await db.execute(query)

    return list(result.scalars().all())