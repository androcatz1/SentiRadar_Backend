import re
import pandas as pd
import asyncio

from collections import Counter
from sqlalchemy import func, select, desc, asc, case, Float, text, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from typing import get_args


from app.models.videos import VideosModel
from app.models.comments import CommentsModel
from app.schemas.analytics import Filters, TopVideosQuery, HeatmapQuery, ScatterQuery
from app.services.helpers import query_filters

async def get_video_dashboard_stats(db: AsyncSession, filters: Filters) -> dict:
    # 1. Build the base aggregation query selection matrix
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
    
    # 2. Safely apply your external dynamic query filters
    query = query_filters(query, filters)
    
    # 3. Execute exactly once (Extract once to protect result stream state)
    result = await db.execute(query)
    row = result.mappings().one_or_none()
    
    # 4. Handle edge cases where your filtered query returns completely empty rows
    if not row or row["total_videos"] == 0:
        return {
            "total_videos": 0, "total_views": 0, "total_likes": 0, "total_comments": 0,
            "avg_duration": 0.0, "avg_engagement_rate": 0.0,
            "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0}
        }
        
    # 5. Format and convert SQL Decimal types to cleanly rounded Python primitives
    return {
        "total_videos": int(row["total_videos"]),
        "total_views": int(row["total_views"] or 0),
        "total_likes": int(row["total_likes"] or 0),
        "total_comments": int(row["total_comments"] or 0),
        "avg_duration": round(float(row["avg_duration"] or 0.0), 2),
        "avg_engagement_rate": round(float(row["avg_engagement_rate"] or 0.0), 4),
        "sentiment_distribution": {
            "positive": int(row["total_positive"] or 0),
            "neutral": int(row["total_neutral"] or 0),
            "negative": int(row["total_negative"] or 0)
        }
    }

async def get_stats(column: str, db: AsyncSession, filters: Filters) -> list[dict]:
    # 1. Dynamically target the requested grouping column from your model schema
    group_column = getattr(VideosModel, column)
    
    # 2. Establish your safe group-level total sentiment denominator
    sum_pos = func.sum(VideosModel.positive)
    sum_neu = func.sum(VideosModel.neutral)
    sum_neg = func.sum(VideosModel.negative)
    total_sentiment = func.nullif(sum_pos + sum_neu + sum_neg, 0)

    # 3. Assemble your core query logic matrix
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
        sum_pos.label("total_positive"),
        sum_neu.label("total_neutral"),
        sum_neg.label("total_negative"),
        ((sum_pos * 100.0) / total_sentiment).label("pct_positive"),
        ((sum_neu * 100.0) / total_sentiment).label("pct_neutral"),
        ((sum_neg * 100.0) / total_sentiment).label("pct_negative")
    ).group_by(group_column)

    # 4. Integrate your global helper filter function
    query = query_filters(query, filters)

    # 5. Execute and extract all matching row items
    result = await db.execute(query)
    rows = result.mappings().all()
    
    # 6. Transform the row collection payload into structured JSON arrays
    formatted_stats = []
    for row in rows:
        # Skip empty unassigned labels to protect frontend presentation widgets
        if row["label"] is None:
            continue

        formatted_stats.append({
            "label": str(row["label"]),
            "total_videos": int(row["total_videos"]),
            "total_views": int(row["total_views"] or 0),
            "total_likes": int(row["total_likes"] or 0),
            "total_comments": int(row["total_comments"] or 0),
            "avg_views": round(float(row["avg_views"] or 0.0), 2),
            "avg_likes": round(float(row["avg_likes"] or 0.0), 2),
            "avg_duration": round(float(row["avg_duration"] or 0.0), 2),
            "avg_engagement_rate": round(float(row["avg_engagement_rate"] or 0.0), 4),
            
            # Cleanly organized raw counts nested sub-object block
            "sentiment_counts": {
                "positive": int(row["total_positive"] or 0),
                "neutral": int(row["total_neutral"] or 0),
                "negative": int(row["total_negative"] or 0)
            },
            
            # Cleanly organized normalized percentage ratios nested block
            "sentiment_percentages": {
                "positive": round(float(row["pct_positive"] or 0.0), 2),
                "neutral": round(float(row["pct_neutral"] or 0.0), 2),
                "negative": round(float(row["pct_negative"] or 0.0), 2)
            }
        })
        
    return formatted_stats


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

    word_freq_df = pd.DataFrame(word_counts.items(), columns=["word", "freq"]) # Renamed to match typical charting formats
    word_freq_df = word_freq_df.sort_values(by="freq", ascending=False)

    # take top 25 words for keyword frequency chart
    top_words = word_freq_df.head(50).to_dict(orient="records")
    
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
        "views": VideosModel.log10_views,
        "likes": VideosModel.log10_likes,
        "comments_count": VideosModel.log10_comments_count,
        "negative_ratio": negative_pct_expr,
        "positive_ratio": positive_pct_expr
    }

    # Extract the requested X and Y expressions
    expr_x = axis_mappings.get(params.x)
    expr_y = axis_mappings.get(params.y)
    
    # 4. Extract the requested COLOR_BY database column dynamically
    if params.color_by  == "none":
        expr_color = literal_column("'All Videos'")
    else:
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
        is_x_ratio = params.x in ["views", "likes", "comments_count", "negative_ratio", "positive_ratio"]
        is_y_ratio = params.y in ["views", "likes", "comments_count", "negative_ratio", "positive_ratio"]

        x_val = round(float(row["x"] or 0.0), 4) if is_x_ratio else int(row["x"] or 0)
        y_val = round(float(row["y"] or 0.0), 4) if is_y_ratio else int(row["y"] or 0)

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
        "channel_title": sorted(list(res_channels.all())),
        "topic": sorted(list(res_topics.all())),
        "platform": sorted(list(res_platforms.all())),
        "duration_bucket": sorted(list(res_buckets.all()))
    }

def get_chart_query_options():
    # Helper lambda function to reach into Pydantic v2 structure 
    # and pull the raw tuple choices inside Literal[...]
    get_literal_choices = lambda model, field_name: list(get_args(model.model_fields[field_name].annotation))

    return {
        "scatter": {
            "x": get_literal_choices(ScatterQuery, "x"),
            "y": get_literal_choices(ScatterQuery, "y"),
            "color_by": get_literal_choices(ScatterQuery, "color_by")
        },
        "heatmap": {
            "x": get_literal_choices(HeatmapQuery, "x"),
            "y": get_literal_choices(HeatmapQuery, "y"),
            "metric": get_literal_choices(HeatmapQuery, "metric")
        },
        "topVideos": {
            "metric": get_literal_choices(TopVideosQuery, "metric")
        }
    }   


async def get_kpi_dashboard(db: AsyncSession,filters: Filters) -> dict:
    
    # 2. Execute all your existing database queries 
    main_stats = await  get_video_dashboard_stats(db, filters)
    topic_stats = await get_stats(column="topic", db=db, filters=filters)
    platform_stats = await get_stats(column="platform", db=db, filters=filters)
    duration_stats = await get_stats(column="duration_bucket", db=db, filters=filters)
    top_vids = await get_top_videos(db, filters, TopVideosQuery())

    # 3. Cleanly restructure and transform the raw outputs from your functions
    # into your exact target nested JSON layout
    return {
        "overview": {
            "total_videos": main_stats["total_videos"],
            "total_views": main_stats["total_views"],
            "total_likes": main_stats["total_likes"],
            "total_comments": main_stats["total_comments"],
            "avg_duration": main_stats["avg_duration"],
            "avg_engagement_rate": main_stats["avg_engagement_rate"]
        },
        
        "sentiment": {
            "positive": main_stats["sentiment_distribution"]["positive"],
            "neutral": main_stats["sentiment_distribution"]["neutral"],
            "negative": main_stats["sentiment_distribution"]["negative"]
        },
        
        # Pull required key values dynamically from your generic get_stats loop outputs
        "topics": [
            {
                "topic": item["label"],
                "video_count": item["total_videos"],
                "avg_views": item["avg_views"],
                'avg_likes': item["avg_likes"],
                "avg_duration": item['avg_duration'],
                "avg_engagement_rate": item['avg_engagement_rate']
            }
            for item in topic_stats
        ],
        
        "platforms": [
            {
                "platform": item["label"],
                "video_count": item["total_videos"],
                "avg_views": item["avg_views"],
                'avg_likes': item["avg_likes"],
                "avg_duration": item['avg_duration'],
                "avg_engagement_rate": item['avg_engagement_rate']
            }
            for item in platform_stats
        ],
        
        "duration_buckets": [
            {
                "bucket": item["label"],
                "video_count": item["total_videos"],
                "avg_views": item["avg_views"],
                'avg_likes': item["avg_likes"],
                "avg_duration": item['avg_duration'],
                "avg_engagement_rate": item['avg_engagement_rate']
            }
            for item in duration_stats
        ],
        
        "top_videos": top_vids
    }    

async def get_engagement_dashboard(db: AsyncSession, filters: Filters):
    
    # 2. RUN IN PARALLEL: Fire all three database query engines simultaneously
    summary_data = await get_topic_summary_table(db, filters)
    scatter_data = await get_generic_scatter_plot(db, filters, ScatterQuery())
    heatmap_data = await get_generic_heatmap(db, filters, HeatmapQuery())


    # 3. Structural Output Mapping
    return {
        # Your topic summary function already calculates percentages and platforms beautifully!
        "summary_table": [
            {
                "topic": item["topic"],
                "video_count": item.get("video_count", 0), # Fallback if missing
                "avg_views": item["avg_views"],
                "avg_engagement_rate": item["avg_engagement_rate"],
                "dominant_sentiment": item["dominant_sentiment"],
                "best_platform": item["best_platform"],
                "positive_pct": item.get("positive_pct", 0.0), # Maps your table pct fields
                "negative_pct": item.get("negative_pct", 0.0)
            }
            for item in summary_data
        ],

        # Your scatter function already outputs standard "x", "y", and "group" keys for React!
        "scatter": scatter_data,

        # Your heatmap function already outputs clean "x", "y", and "value" keys!
        "heatmap": heatmap_data
    }

async def get_sentiment_dashboard(db: AsyncSession, filters: Filters):

    topic_raw_stats = await get_stats(column="topic", db=db, filters=filters)
    platform_raw_stats = await get_stats(column="platform", db=db, filters=filters)
    channel_raw_stats = await get_stats(column="channel_title", db=db, filters=filters)  

    return {
        "sentiment_by_topic": [
            {
                "topic": item["label"],
                "positive": item["sentiment_counts"]["positive"],
                "neutral": item["sentiment_counts"]["neutral"],
                "negative": item["sentiment_counts"]["negative"],
                "positive_pct": item["sentiment_percentages"]["positive"],
                "neutral_pct": item["sentiment_percentages"]["neutral"],
                "negative_pct": item["sentiment_percentages"]["negative"]
            } for item in topic_raw_stats
        ],
        "sentiment_by_platform": [
            {
                "platform": item["label"],
                "positive": item["sentiment_counts"]["positive"],
                "neutral": item["sentiment_counts"]["neutral"],
                "negative": item["sentiment_counts"]["negative"],
                "positive_pct": item["sentiment_percentages"]["positive"],
                "neutral_pct": item["sentiment_percentages"]["neutral"],
                "negative_pct": item["sentiment_percentages"]["negative"]
            } for item in platform_raw_stats
        ],

        "sentiment_by_channel": [
            {
                "channel": item["label"],
                "positive": item["sentiment_counts"]["positive"],
                "neutral": item["sentiment_counts"]["neutral"],
                "negative": item["sentiment_counts"]["negative"],
                "positive_pct": item["sentiment_percentages"]["positive"],
                "neutral_pct": item["sentiment_percentages"]["neutral"],
                "negative_pct": item["sentiment_percentages"]["negative"]
            } for item in channel_raw_stats
        ]
    }