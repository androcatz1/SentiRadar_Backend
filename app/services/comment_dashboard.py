from app.schemas.comments import FilterSchema
from app.models.comments import CommentsModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

async def get_card_data(db: AsyncSession, filters:FilterSchema, max_rows: int = 20):
    query = select(
                CommentsModel.video_id, 
                func.count(CommentsModel.video_id).label("count")
            ).group_by(CommentsModel.video_id)

    if filters.video_id:
        query = query.where(CommentsModel.video_id == filters.video_id)

    if filters.label:
        query = query.where(CommentsModel.label == filters.label)

    result = await db.execute(query)

    return result.mappings().all()
