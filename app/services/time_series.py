from sqlalchemy import func, select, cast, Date, literal_column
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.videos_time_series import VideosTimeSeriesModel
from app.services.helpers import query_filters_ts
from app.schemas.analytics import Filters

async def get_consolidated_time_series_data(db: AsyncSession, filters: Filters) -> dict:
    # 1. Standardize UTC to Asia/Kuala_Lumpur (SGT / UTC+8)
    sgt_timezone_adjusted = VideosTimeSeriesModel.fetched_at.op('AT TIME ZONE')('UTC').op('AT TIME ZONE')('Asia/Kuala_Lumpur')
    sgt_fetched_at = cast(sgt_timezone_adjusted, Date)

    # 2. Build the Window Function to generate an index per video starting at 0
    time_index_expr = func.row_number().over(
        partition_by=VideosTimeSeriesModel.video_id,
        order_by=VideosTimeSeriesModel.fetched_at
    ) - 1

    # 3. Formulate selection statement pulling all chronological snapshot logs
    query = select(
        VideosTimeSeriesModel.video_id,
        VideosTimeSeriesModel.title,
        VideosTimeSeriesModel.platform,
        VideosTimeSeriesModel.topic,
        VideosTimeSeriesModel.views,
        VideosTimeSeriesModel.likes,
        VideosTimeSeriesModel.comments_count,
        VideosTimeSeriesModel.engagement_rate,
        sgt_fetched_at.label("sgt_time"),
        time_index_expr.label("time_index")
    )

    # 4. Integrate your standard dynamic dashboard filter variables
    query = query_filters_ts(query, filters)

    # Order rows systematically so your arrays align chronologically
    query = query.order_by(VideosTimeSeriesModel.video_id, VideosTimeSeriesModel.fetched_at)

    # 5. Execute query and fetch records
    result = await db.execute(query)
    rows = result.mappings().all()

    if not rows:
        return {
            "meta": {"video_count": 0, "total_observations": 0, "date_min": None, "date_max": None}, 
            "series": []
        }

    # 6. Process database output row-by-row into a nested video collection map
    video_map = {}
    all_dates = []

    for row in rows:
        vid = row["video_id"]
        date_str = row["sgt_time"].strftime("%Y-%m-%d") if row["sgt_time"] else None
        if date_str:
            all_dates.append(date_str)

        if vid not in video_map:
            video_map[vid] = {
                "video_id": vid,
                "title": row["title"],
                "platform": row["platform"],
                "topic": row["topic"] or "Unassigned",
                "points": []
            }

        iso_with_tz = row["sgt_time"].strftime("%Y-%m-%dT%H:%M:%S%z") if row["sgt_time"] else None

        video_map[vid]["points"].append({
            "time_index": int(row["time_index"]),
            "fetched_at": iso_with_tz,
            "views": int(row["views"] or 0),
            "likes": int(row["likes"] or 0),
            "comments": int(row["comments_count"] or 0),
            "engagement_rate": round(float(row["engagement_rate"] or 0.0), 4)
        })

    # 7. Formulate meta properties boundaries
    meta = {
        "video_count": len(video_map),
        "total_observations": len(rows),
        "date_min": min(all_dates) if all_dates else None,
        "date_max": max(all_dates) if all_dates else None
    }

    return {
        "meta": meta,
        "series": list(video_map.values())
    }

# -----------------------------------------------------------------------------------------------------
async def get_dynamic_aggregated_time_series(db: AsyncSession, filters: Filters, group_by_col: str) -> dict:
    # 1. 🛠️ FIX: Handle the "none" string option gracefully using a static SQL literal column
    if group_by_col == "none":
        group_column = literal_column("'All Videos'")
    else:
        group_column = getattr(VideosTimeSeriesModel, group_by_col)

    # 2. Setup the precise timezone conversion forward 8 hours to SGT
    sgt_timezone_adjusted = VideosTimeSeriesModel.fetched_at.op('AT TIME ZONE')('UTC').op('AT TIME ZONE')('Asia/Kuala_Lumpur')
    sgt_date_expr = cast(sgt_timezone_adjusted, Date)

    # 3. SUBQUERY: Pre-calculate the chronological 0-based time index for every log row
    time_index_expr = func.row_number().over(
        partition_by=VideosTimeSeriesModel.video_id,
        order_by=VideosTimeSeriesModel.fetched_at
    ) - 1

    subquery = select(
        group_column.label("group_label"),
        VideosTimeSeriesModel.video_id,
        VideosTimeSeriesModel.views,
        VideosTimeSeriesModel.engagement_rate,
        sgt_date_expr.label("calendar_date"),
        time_index_expr.label("time_index")
    )

    # Apply global filters inside the subquery to shrink data footprint early
    query = query_filters_ts(subquery, filters)
    subquery = query.subquery()

    # -------------------------------------------------------------------------
    # QUERY A: Cumulative Library Growth (Grouped by Calendar Date)
    # -------------------------------------------------------------------------
    calendar_query = select(
        subquery.c.group_label,
        subquery.c.calendar_date,
        func.sum(subquery.c.views).label("total_views"),
        func.count(func.distinct(subquery.c.video_id)).label("videos_tracked")
    ).group_by(subquery.c.group_label, subquery.c.calendar_date).order_by(subquery.c.calendar_date)

    # -------------------------------------------------------------------------
    # QUERY B: True Lifecycle Performance Curves (Grouped by Time Index)
    # -------------------------------------------------------------------------
    lifecycle_query = select(
        subquery.c.group_label,
        subquery.c.time_index,
        func.avg(subquery.c.views).label("avg_views"),
        func.avg(subquery.c.engagement_rate).label("avg_engagement")
    ).group_by(subquery.c.group_label, subquery.c.time_index).order_by(subquery.c.time_index)

    # Execute both calculations sequentially
    calendar_res = await db.execute(calendar_query)
    lifecycle_res = await db.execute(lifecycle_query)

    # -------------------------------------------------------------------------
    # PARSING: Format Output dynamically using the value of 'group_by_col'
    # -------------------------------------------------------------------------
    calendar_map = {}
    for row in calendar_res.mappings().all():
        label = row["group_label"] or "Unassigned"
        if label not in calendar_map:
            # If group_by_col is "none", we use a generic string key like "group" instead of "none"
            key_name = "group" if group_by_col == "none" else group_by_col
            calendar_map[label] = {key_name: label, "points": []}
            
        calendar_map[label]["points"].append({
            "date": row["calendar_date"].strftime("%Y-%m-%d") if row["calendar_date"] else None,
            "total_views": int(row["total_views"] or 0),
            "videos_tracked": int(row["videos_tracked"] or 0)
        })

    lifecycle_map = {}
    for row in lifecycle_res.mappings().all():
        label = row["group_label"] or "Unassigned"
        # Safe cap limits to protect UI graph workspace spacing
        if row["time_index"] is None or row["time_index"] > 30:
            continue
            
        if label not in lifecycle_map:
            key_name = "group" if group_by_col == "none" else group_by_col
            lifecycle_map[label] = {key_name: label, "points": []}
            
        lifecycle_map[label]["points"].append({
            "time_index": int(row["time_index"]),
            "avg_views": round(float(row["avg_views"] or 0)),
            "avg_engagement": round(float(row["avg_engagement"] or 0.0), 4)
        })

    return {
        "library_growth_over_time": list(calendar_map.values()),
        "video_lifecycle_progression": list(lifecycle_map.values())
    }
