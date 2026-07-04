import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession

from app.etl.extract.comments import fetch_top_level_comments
from app.etl.transform.comments import run_pipeline, predict_labels
from app.etl.load.comments import insert_into_postgres


async def new_comments_pipeline(db: AsyncSession, video_id: str):
    rows =  await fetch_top_level_comments(video_id, max_pages =5)
    df = pd.DataFrame(rows)

    df_cleaned = run_pipeline(df) #clean text
    df_labelled = predict_labels(df_cleaned) # predict text sentiment
    status = await insert_into_postgres(db, df_labelled) # insert into db

    return {"Status": status, "video_id": video_id}

