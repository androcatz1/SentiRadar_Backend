import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from app.models.videos import VideosModel


async def insert_into_postgres(db: AsyncSession, df: pd.DataFrame):    
    raw_records = df.to_dict(orient="records")

    model_instances = [VideosModel(**record) for record in raw_records]
    
    db.add_all(model_instances)
    await db.commit()

    return "Success"


async def update_sentiment(db: AsyncSession, df: pd.DataFrame):
    # update video's neu, pos and negative columns in video table first
    label_counts = pd.crosstab(df['video_id'], df['label'])

    # extract details
    video_id = df['video_id'].iloc[0]
    row_data = label_counts.loc[video_id]

    neu_count = int(row_data.get(0.0, 0))
    pos_count = int(row_data.get(1.0, 0))
    neg_count = int(row_data.get(2.0, 0))

    print(neu_count, pos_count, neg_count)
    query = (
        update(VideosModel)
        .where(VideosModel.video_id == video_id)
        .values(neutral=neu_count, positive=pos_count, negative=neg_count)
    )
    
    await db.execute(query)
    await db.commit()