import pandas as pd
import isodate, ast
import numpy as np
import json

from app.config.settings import Settings, Gemini
from app.etl.video_utils.helpers import call_gemini

def transform(rows):
    df = pd.DataFrame(rows, columns=Settings.COLUMNS_RAW)

    # Step 1: Type Casting
    # convert datetime columns
    df['published_at'] = pd.to_datetime(df['published_at']).dt.tz_localize(None)
    df['fetched_at'] = pd.to_datetime(df['fetched_at'])

    # convert numeric columns
    df['views'] = df['views'].astype(int)
    df['likes'] = df['likes'].astype(int)
    df['comments_count'] = df['comments_count'].astype(int)
    df['category_id'] = df['category_id'].astype(str)

    # convert video type columns to string
    df['platform'] = df['platform'].astype(str)

    #-----------------------------------------------------------------------------------------------
    # Step 2: Extract Specific Details
    # extract hour
    df['published_hour'] = df['published_at'].dt.hour

    # extract day of week
    df['published_day'] = df['published_at'].dt.day_name()

    # extract month
    df['published_month'] = df['published_at'].dt.month_name()

    #-----------------------------------------------------------------------------------------------
    # Step 3: Convert ISO 8601 duration to Minutes
    df['duration_mins'] = df['duration'].apply(
        lambda x: round(isodate.parse_duration(x).total_seconds() / 60, 2)
    )

    #-----------------------------------------------------------------------------------------------
    # Step 4: Caluclate Engagement Rate
    df['engagement_rate'] = round((df['likes'] + df['comments_count']) / df['views'], 4)

    #-----------------------------------------------------------------------------------------------
    # Step 5: Convert Tags to List and remove redundant tags
    df['tags'] = df['tags'].apply(ast.literal_eval)

    df['tags'] = df['tags'].apply(
        lambda tag_list: [
            tag.lower().strip() for tag in tag_list 
            if tag.lower().strip() not in Settings.TAGS_TO_REMOVE
        ] 
        if isinstance(tag_list, list) else tag_list
    )

    # convert back to string to store in db
    df['tags'] = df['tags'].apply(lambda x: json.dumps(x) if isinstance(x, list) else "[]")

    #-----------------------------------------------------------------------------------------------
    # Step 6: Generate category for duration
    log_bins = [0, 1, 5, 15, 30, 60, 120, 1440] 
    log_labels = ['<1 min', '1-5 min', '5-15 min', '15-30 min', '30-60 min', '1-2 hrs', '>2 hrs']

    df['duration_bucket'] = pd.cut(df['duration_mins'], bins=log_bins, labels=log_labels)

    #-----------------------------------------------------------------------------------------------
    # Step 7: add log values for charts
    df['log10_views'] = np.log10(df['views'] + 1)
    df['log10_likes'] = np.log10(df['likes'] + 1)
    df['log10_comments_count'] = np.log10(df['comments_count'] + 1)

    #-----------------------------------------------------------------------------------------------
    # Step 8: add 0 for pos, neg and neu (will update later)
    df['neutral'] = 0
    df['positive'] = 0
    df['negative'] = 0

    return df


def label_topic(clean_data):
    topics = []
    df = clean_data.copy()
    null_topics_df = df[df['topic'].isna()][['video_id', 'title']]

    for i in range(0, len(null_topics_df), Gemini.BATCH_SIZE):
        batch_df = null_topics_df.iloc[i: i+Gemini.BATCH_SIZE]

        titles = batch_df['title'].str.cat(sep="\n")
        print(titles)
        print("-----------------------------------------------------------")
        prompt = Gemini.USER_PROMPT_TEMPLATE.format(titles =titles)
        categories = call_gemini(prompt)

        categories = [
            line.strip()
            for line in categories.text.splitlines()
            if line.strip()
        ]
        topics.extend(categories)

        print(categories)
        if len(categories) != len(batch_df):
            raise ValueError(
                f"Expected {len(batch_df)} labels, got {len(categories)}"
            )
        
    null_topics_df['topic'] = topics   
    df.update(null_topics_df)

    return df


