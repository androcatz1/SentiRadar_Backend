from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from app.models.videos import VideosModel


async def check_video_id_exist(db: AsyncSession, video_id:str):
    query = select(exists().where(VideosModel.video_id == video_id))
    
    result = await db.execute(query)
    
    return result.scalar() or False