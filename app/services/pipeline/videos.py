from sqlalchemy.ext.asyncio import AsyncSession

from app.etl.extract.videos import fetch_video_metadata
from app.etl.transform.videos import transform, label_topic
from app.etl.load.videos import insert_into_postgres

async def new_video_pipeline(db: AsyncSession, video_id: str):
    rows = await fetch_video_metadata(video_id)
    if rows is None:
        raise ValueError ("ID Does Not Exist")
    df = transform(rows)
    df_labelled = label_topic(df)

    status = await insert_into_postgres(db, df_labelled)
    
    return status
