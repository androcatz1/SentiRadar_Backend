import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession

from app.etl.extract.comments import fetch_top_level_comments
from app.etl.transform.comments import run_pipeline, predict_labels
from app.etl.load.comments import insert_into_postgres


async def new_comments_pipeline(db: AsyncSession, video_id: str):
    rows =  await fetch_top_level_comments(video_id, max_pages =5)
    # Check if rows is None, empty list, or empty dict
    if not rows:
        return {"Status": "Skipped: No raw comments found", "video_id": video_id}
        
    df = pd.DataFrame(rows)
    
    # Double-check case where rows was a list of empty dicts, resulting in an empty DataFrame
    if df.empty:
        return {"Status": "Skipped: Initial DataFrame is empty", "video_id": video_id}
    
    # 2. Clean text
    df_cleaned = run_pipeline(df) 
    
    # Check if cleaning removed all rows (e.g., filtered out all spam/bots/short text)
    if df_cleaned.empty:
        return {"Status": "Skipped: No valid comments left after cleaning", "video_id": video_id}
      
    df_cleaned = run_pipeline(df) #clean text
    df_labelled = predict_labels(df_cleaned) # predict text sentiment
    status = await insert_into_postgres(db, df_labelled) # insert into db

    return {"Status": status, "video_id": video_id}

