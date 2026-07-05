import re
import pandas as pd
import asyncio

from collections import Counter
from sqlalchemy import func, select, desc, asc, case, Float, text
from sqlalchemy.ext.asyncio import AsyncSession


from app.models.videos import VideosModel
from app.models.comments import CommentsModel
from app.schemas.analytics import Filters, TopVideosQuery, HeatmapQuery, ScatterQuery
from app.services.helpers import query_filters

async def get_video_dashboard_stats(db: AsyncSession, filters: Filters) -> dict:
    query = select(
        func.count(VideosModel.video_id).label("total_videos"),
        func.sum(VideosModel.views).label("total_views"),
        func.sum(VideosModel.likes).label("total_likes"),
        func.sum(VideosModel.comments_count).label("total_comments"),
        func.avg(VideosModel.duration_mins).label("avg_duration"),
        func.avg(VideosModel.engagement_rate).label("avg_engagement_rate"),
        func.sum(VideosModel.positive).label("total_positive"),
        func.sum(VideosModel.neutral).label("total_neutral"),
        func.sum(VideosModel.negative).label("total_negative")
    )
# --------------------------------------------------------------------------------------    
    query = query_filters(query, filters)
# --------------------------------------------------------------------------------------    

    result = await db.execute(query)
    
    row = result.mappings().one_or_none()

    return row

async def get_stats(column, db: AsyncSession, filters: Filters) -> dict:
    group_column = getattr(VideosModel, column)
    
    total_sentiment = func.nullif(
        func.sum(VideosModel.positive) + func.sum(VideosModel.neutral) + func.sum(VideosModel.negative),0)

    query = select(
        group_column.label("label"),
        func.count(VideosModel.video_id).label("total_videos"),
        func.sum(VideosModel.views).label("total_views"),
        func.sum(VideosModel.likes).label("total_likes"),
        func.sum(VideosModel.comments_count).label("total_comments"),
        func.avg(VideosModel.views).label("avg_views"),
        func.avg(VideosModel.likes).label("avg_likes"),
        func.avg(VideosModel.duration_mins).label("avg_duration"),
        func.avg(VideosModel.engagement_rate).label("avg_engagement_rate"),
        func.sum(VideosModel.positive).label("total_positive"),
        func.sum(VideosModel.neutral).label("total_neutral"),
        func.sum(VideosModel.negative).label("total_negative"),

        ((func.sum(VideosModel.positive) * 100.0) / total_sentiment).label("pct_positive"),
        ((func.sum(VideosModel.neutral) * 100.0) / total_sentiment).label("pct_neutral"),
        ((func.sum(VideosModel.negative) * 100.0) / total_sentiment).label("pct_negative")
    ).group_by(group_column)
# --------------------------------------------------------------------------------------    
    query = query_filters(query, filters)
# --------------------------------------------------------------------------------------    

    result = await db.execute(query)
    
    row = result.mappings().all()
    
    return row


async def get_top_videos(db: AsyncSession, filters: Filters, sort_params: TopVideosQuery):
    sort_column = getattr(VideosModel, sort_params.metric)

    query = select(
        VideosModel.video_id,
        VideosModel.channel_title,
        VideosModel.title,
        VideosModel.topic, 
        VideosModel.platform,
        VideosModel.views,
        VideosModel.likes,
        VideosModel.comments_count,
        VideosModel.engagement_rate,
        VideosModel.positive,
        VideosModel.negative,
        VideosModel.neutral,
    )
# --------------------------------------------------------------------------------------
    query = query_filters(query, filters)
# --------------------------------------------------------------------------------------
    if sort_params.order == 'desc':
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    query = query.limit(sort_params.limit)

    result = await db.execute(query)

    return result.mappings().all()


async def get_top_keywords(db: AsyncSession, video_ids:list):
    comments_query = select(CommentsModel.text_no_stopwords).where(
        CommentsModel.video_id.in_(video_ids))
    
    result = await db.execute(comments_query)

    comment_texts = list(result.scalars().all())

    if not comment_texts:
        return []

    # convert to pandas for keyword counting
    df_comments = pd.Series(comment_texts)

    combined_text = " ".join(df_comments.dropna().astype(str))

    all_words = re.findall(r"\w+", combined_text.lower())

    word_counts = Counter(all_words)

    word_freq_df = pd.DataFrame(word_counts.items(), columns=["text", "value"]) # Renamed to match typical charting formats
    word_freq_df = word_freq_df.sort_values(by="value", ascending=False)

    # take top 25 words for keyword frequency chart
    top_words = word_freq_df.head(25).to_dict(orient="records")
    
    return top_words

async def get_topic_summary_table(db: AsyncSession, filters: Filters) -> list[dict]:
    # 1. Sum up the sentiment columns first for grouping
    sum_pos = func.sum(VideosModel.positive)
    sum_neu = func.sum(VideosModel.neutral)
    sum_neg = func.sum(VideosModel.negative)

    total_sentiment = func.nullif(sum_pos + sum_neu + sum_neg, 0)
    # 2. Use func.greatest to find the highest value sideways across columns
    highest_sum = func.greatest(sum_pos, sum_neu, sum_neg)

    # 3. Use a clean CASE statement to see which category matched the highest sum
    dominant_sentiment_case = case(
        (highest_sum == sum_pos, "Positive"),
        (highest_sum == sum_neu, "Neutral"),
        else_="Negative"
    )

    # 4. Build the main aggregation query
    query = select(
        VideosModel.topic,
        func.count(VideosModel.video_id).label("video_count"),
        func.avg(VideosModel.views).label("avg_views"),
        func.avg(VideosModel.engagement_rate).label("avg_engagement_rate"),
        dominant_sentiment_case.label("dominant_sentiment"),
        # Sub-aggregations to evaluate the best platform performance
        func.avg(case((VideosModel.platform == "Regular", VideosModel.engagement_rate), else_=0)).label("avg_eng_regular"),
        func.avg(case((VideosModel.platform == "Short", VideosModel.engagement_rate), else_=0)).label("avg_eng_short"),
        ((sum_pos * 100.0) / total_sentiment).label("pct_positive"),
        ((sum_neg * 100.0) / total_sentiment).label("pct_negative")
        
    ).group_by(VideosModel.topic)

    # 5. Apply your dynamic global filters
    query = query_filters(query, filters)


    # 6. Execute the query
    result = await db.execute(query)
    rows = result.all()

    # 7. Format the final output list
    summary_table = []
    for row in rows:
        if not row.topic:
            continue
            
        # Determine the best platform based on engagement rate margins
        best_platform = "Regular"
        if (row.avg_eng_short or 0) > (row.avg_eng_regular or 0):
            best_platform = "Short"

        summary_table.append({
            "topic": row.topic,
            "video_count": row.video_count,
            "avg_views": round(float(row.avg_views or 0)),
            "avg_engagement_rate": round(float(row.avg_engagement_rate or 0.0), 4),
            "dominant_sentiment": row.dominant_sentiment,
            "best_platform": best_platform,
            "positive_pct": round(float(row.pct_positive),2),
            "negative_pct": round(float(row.pct_negative),2)
        })

    return summary_table


async def get_generic_heatmap(db: AsyncSession, filters: Filters, params: HeatmapQuery) -> list[dict]:
    # 1. Resolve column objects for X and Y axes dynamically
    col_x = getattr(VideosModel, params.x)
    col_y = getattr(VideosModel, params.y)

    # 2. Resolve the math aggregation function based on the metric string
    metric_mappings = {
        "avg_views": func.avg(VideosModel.views),
        "video_count": func.count(VideosModel.video_id),
        "avg_engagement_rate": func.avg(VideosModel.engagement_rate)
    }

    # Default to avg_views if nothing is specified
    chosen_metric = metric_mappings.get(params.metric)

    # 3. Formulate the dynamic query with grouping
    query = select(
        col_x.label("x"),
        col_y.label("y"),
        chosen_metric.label("value")
    ).group_by(col_x, col_y)

    # 4. Apply your standard global filters
    query = query_filters(query, filters)

    # 5. Execute and extract mappings
    result = await db.execute(query)
    rows = result.mappings().all()

    # 6. Format numbers (round floats to prevent large decimals)
    formatted_heatmap = []
    for row in rows:
        if row["x"] is None or row["y"] is None:
            continue
            
        raw_val = row["value"] or 0
        
        # Format according to the chosen metric type
        if params.metric == "video_count":
            value = int(raw_val)
        elif params.metric == "avg_engagement_rate":
            value = round(float(raw_val), 4) # Keeping 4 decimal places for rates (e.g. 0.0415)
        else:
            value = round(float(raw_val), 0) # Rounding views to whole numbers

        formatted_heatmap.append({
            "x": str(row["x"]),
            "y": str(row["y"]),
            "value": value
        })

    return formatted_heatmap

async def get_generic_scatter_plot(db: AsyncSession, filters: Filters, params: ScatterQuery) -> list[dict]:
    # 1. Set the random state seed 
    await db.execute(text("SELECT setseed(0.42)"))

    # 2. Base row-level total sentiment calculations
    row_total_sentiment = func.nullif(VideosModel.positive + VideosModel.neutral + VideosModel.negative, 0)
    negative_pct_expr = (func.cast(VideosModel.negative, Float) * 100.0) / row_total_sentiment
    positive_pct_expr = (func.cast(VideosModel.positive, Float) * 100.0) / row_total_sentiment

    # 3. Axis mapping registry
    axis_mappings = {
        "views": VideosModel.views,
        "likes": VideosModel.likes,
        "comments_count": VideosModel.comments_count,
        "negative_ratio": negative_pct_expr,
        "positive_ratio": positive_pct_expr
    }

    # Extract the requested X and Y expressions
    expr_x = axis_mappings.get(params.x)
    expr_y = axis_mappings.get(params.y)
    
    # 4. Extract the requested COLOR_BY database column dynamically
    expr_color = getattr(VideosModel, params.color_by)

    # 5. Formulate selection query utilizing clean, generic targets
    query = select(
        VideosModel.video_id,
        VideosModel.title,
        expr_x.label("x"),
        expr_y.label("y"),
        expr_color.label("group")
    )

    # 6. Apply standard global dashboard filters 
    query = query_filters(query, filters)

    # 7. Unbiased Random Sampling Strategy to bypass data skew and protect performance
    query = query.order_by(func.random()).limit(params.limit)

    # 8. Execute and extract mappings
    result = await db.execute(query)
    rows = result.mappings().all()

    formatted_scatter = []
    for row in rows:
        is_x_ratio = params.x in ["negative_ratio", "positive_ratio"]
        is_y_ratio = params.y in ["negative_ratio", "positive_ratio"]

        x_val = round(float(row["x"] or 0.0), 2) if is_x_ratio else int(row["x"] or 0)
        y_val = round(float(row["y"] or 0.0), 2) if is_y_ratio else int(row["y"] or 0)

        formatted_scatter.append({
            "video_id": row["video_id"],
            "title": row["title"],
            "x": x_val,
            "y": y_val,
            "group": row["group"] or "Unassigned" 
        })

    return formatted_scatter

async def get_dashboard_filter_options(db: AsyncSession) -> dict:
    # 1. Query each column individually 
    q_channels = select(func.distinct(VideosModel.channel_title)).where(VideosModel.channel_title.isnot(None))
    q_topics = select(func.distinct(VideosModel.topic)).where(VideosModel.topic.isnot(None))
    q_platforms = select(func.distinct(VideosModel.platform)).where(VideosModel.platform.isnot(None))
    q_buckets = select(func.distinct(VideosModel.duration_bucket)).where(VideosModel.duration_bucket.isnot(None))

    # 2. Await them step-by-step to prevent concurrent session state crashes
    res_channels = await db.scalars(q_channels)
    res_topics = await db.scalars(q_topics)
    res_platforms = await db.scalars(q_platforms)
    res_buckets = await db.scalars(q_buckets)

    # 3. Unpack into clean sorted lists for your React dropdown menus
    return {
        "channels": sorted(list(res_channels.all())),
        "topics": sorted(list(res_topics.all())),
        "platforms": sorted(list(res_platforms.all())),
        "duration_buckets": sorted(list(res_buckets.all()))
    }