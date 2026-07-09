from fastapi import Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError

from app.database.connection import get_db_static

from app.schemas.videos import UserInputSchema
from app.schemas.comments import PaginationParams
from app.schemas.analytics import Filters

from app.services.pipeline.videos import new_video_pipeline
from app.services.videos import check_video_id_exist, get_single_video_overview, get_filtered_video_details_list
from app.services.comments import get_paginated_video_comments, get_top_keywords

router = APIRouter(prefix="/api/videos")

# new video inputs
@router.get("/get_video")
async def get_new_video(db: AsyncSession = Depends(get_db_static), url:str = Query(...)):  
    try:
        video = UserInputSchema(url=url)
    except ValidationError as e:
        # Extract the exact message from your model_validator ("Invalid YouTube url!")
        error_msg = e.errors()[0]["msg"]
        if error_msg.startswith("Value error, "):
            error_msg = error_msg.replace("Value error, ", "")
            
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": error_msg}
        )
    
    exist = await check_video_id_exist(db, video.video_id)
    if exist:
        return {"status": "Exists", "video_id": video.video_id}
    
    try:
        await new_video_pipeline(db, video.video_id)
        return {"status": "New Video", "video_id": video.video_id}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": str(e)}
        )


# video level analysis
@router.get("/{video_id}/overview")
async def get_video_detailed_overview(video_id: str, db:AsyncSession = Depends(get_db_static)):
    video_data = await get_single_video_overview(db, video_id)
    
    # If the video_id is invalid or missing, fail immediately with a 404
    if not video_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Video with ID '{video_id}' could not be found."
        )
        
    return video_data

@router.get("/{video_id}/comments")
async def get_video_detailed_overview(video_id: str, db:AsyncSession = Depends(get_db_static),
                                      pagination_params: PaginationParams = Depends()):
    
    comments_data = await get_paginated_video_comments(db, video_id, pagination_params)
    
    return comments_data

@router.get("/{video_id}/keywords")
async def get_single_video_keywords(video_id: str, db: AsyncSession = Depends(get_db_static)):
    keywords = await get_top_keywords(db, video_id)
    
    return keywords

@router.get("/get_video_ids")
async def get_video_ids(db: AsyncSession = Depends(get_db_static), filters: Filters = Depends()):
    results = await get_filtered_video_details_list(db, filters)
    return results