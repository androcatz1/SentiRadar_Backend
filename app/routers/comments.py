from fastapi import Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db_static
from app.services.comments import check_video_id_exist
from app.services.pipeline.comments import new_comments_pipeline

router = APIRouter(prefix="/api/comments")

@router.get("/get_comments")
async def get_new_comments(db: AsyncSession = Depends(get_db_static), video_id: str = Query(...)):  
    exists = await check_video_id_exist(db, video_id)
    if exists:
        return {"Status": "Exists", "video_id": video_id}
    
    status = await new_comments_pipeline(db, video_id)
    return status;
