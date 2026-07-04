import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comments import CommentsModel
from app.etl.load.videos import update_sentiment

async def insert_into_postgres(db: AsyncSession, df: pd.DataFrame):  
# ---------------------------------------------------------------------------------------    
    await update_sentiment(db, df) # updates sentiment record in db
#--------------------------------------------------------------------------------------
    raw_records = df.to_dict(orient="records")

    model_instances = [CommentsModel(**record) for record in raw_records]
    
    db.add_all(model_instances)
    await db.commit()

    return "Done"