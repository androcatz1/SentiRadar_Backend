from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.videos import UserInputSchema
from app.database.connection import get_db_static
from app.services.pipeline.videos import new_video_pipeline
from app.services.videos import check_video_id_exist

router = APIRouter(prefix="/api/videos")

@router.get("/get_video")
async def get_new_video(db: AsyncSession = Depends(get_db_static), video: UserInputSchema = Depends()):  
    exist = await check_video_id_exist(db, video.video_id)
    if exist:
        return {"status": "Exists", "video_id": video.video_id}
    
    status = await new_video_pipeline(db, video.video_id)
    return {"status": "New Video", "video_id": video.video_id, "inserted": status}

# video level analysis
@router.get("/{video_id}/dashboard")
async def display_dashboard(video_id: str, db:AsyncSession = Depends(get_db_static)):
    pass