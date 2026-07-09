import re
import pandas as pd

from collections import Counter

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, func

from app.models.comments import CommentsModel
from app.schemas.comments import PaginationParams
from app.config.settings import Settings

async def check_video_id_exist(db: AsyncSession, video_id:str):
    query = select(exists().where(CommentsModel.video_id == video_id))
    
    result = await db.execute(query)
    
    return result.scalar() or False

#Video Level Analysis-----------------------------------------------------------------------------
async def get_paginated_video_comments(
    db: AsyncSession, 
    video_id: str, 
    pagination: PaginationParams
) -> dict:
    # 1. Query the absolute total count of comments for this specific video
    count_query = select(func.count(CommentsModel.id)).where(CommentsModel.video_id == video_id)
    count_result = await db.execute(count_query)
    total_comments = count_result.scalar() or 0

    # 2. Base query to fetch the comment text records
    comments_query = (
        select(CommentsModel.text, CommentsModel.text_processed, CommentsModel.label)
        .where(CommentsModel.video_id == video_id)
        # Apply page window constraints
        .limit(pagination.limit)
        .offset(pagination.offset)
    )
    
    result = await db.execute(comments_query)
    rows = result.mappings().all()

    # 3. 🛠️ FIX: Put the label processing inside the list comprehension loop!
    return {
        "video_id": video_id,
        "total": total_comments,
        "comments": [
            {
                "text": row["text"],
                "text_processed": row["text_processed"],
                # Safely cast to int and look up the string name (e.g., "Negative", "Positive")
                # Fallback to a string format of the number if it's missing from your map
                "label": Settings.SENTIMENT_MAP.get(int(row["label"]))
            }
            for row in rows
        ]
    }

async def get_top_keywords(db: AsyncSession, video_id: str) -> list[dict]:
    # 1. Select only the clean text column to optimize database memory usage
    comments_query = select(CommentsModel.text_no_stopwords).where(
        CommentsModel.video_id == video_id
    )
    
    result = await db.execute(comments_query)
    comment_texts = list(result.scalars().all())

    # Safe guard: exit early if this video has no processed comments yet
    if not comment_texts:
        return []

    # 2. Leverage Pandas and Counter for high-speed string combining
    df_comments = pd.Series(comment_texts)
    combined_text = " ".join(df_comments.dropna().astype(str))

    # 3. Extract words and count frequencies using standard regex lookups
    all_words = re.findall(r"\w+", combined_text.lower())
    word_counts = Counter(all_words)

    # 4. Convert to DataFrame using your exact target JSON names
    word_freq_df = pd.DataFrame(word_counts.items(), columns=["word", "freq"])
    
    # 🛠️ FIX: Sort by 'freq' instead of 'value' to prevent system crashes
    word_freq_df = word_freq_df.sort_values(by="freq", ascending=False)

    # 5. Extract the top 25 records as a list of clean dictionaries
    top_words = word_freq_df.head(25).to_dict(orient="records")
    
    return top_words

async def get_random_comment_stream_samples(db: AsyncSession, video_ids: list[str]) -> list[dict]:
    # Safe guard: If no videos matched the parent filters, return empty array right away
    if not video_ids:
        return []

    # 1. Build selection query targeting the main comment elements
    query = (
        select(
            CommentsModel.video_id,
            CommentsModel.text,
            CommentsModel.text_processed,
            CommentsModel.label
        )
        # Filter comments belonging ONLY to our active filtered video group
        .where(CommentsModel.video_id.in_(video_ids))
        # 🎲 True Random Sampling: Shuffle rows natively at the database layer
        .order_by(func.random())
        # Cap the output constraint to exactly 10 comments to keep the UI feed neat
        .limit(10)
    )

    # 2. Execute query
    result = await db.execute(query)
    rows = result.mappings().all()

    # 4. Map rows into a clean, uniform structural format for your React feed
    formatted_stream = []
    for row in rows:
        raw_label = int(row["label"])
        
        formatted_stream.append({
            "text": row["text"],
            "text_processed": row["text_processed"],
            "sentiment": Settings.SENTIMENT_MAP.get(raw_label)
        })

    return formatted_stream