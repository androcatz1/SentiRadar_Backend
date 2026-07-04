import time
import requests

from dotenv import load_dotenv
from datetime import datetime

from app.config.settings import Settings
from app.etl.video_utils.helpers import detect_short

load_dotenv()
quota_used = 0

session = requests.Session()


async def fetch_video_metadata(video_id):
    global quota_used

    fetch_time = datetime.now()

    results = []

    params = {
        "part": "snippet,statistics,contentDetails",
        "id": video_id,
        "key": Settings.YOUTUBE_API_KEY,
    }

    r = requests.get(f"{Settings.BASE_URL}/videos", params=params)
    r.raise_for_status()

    quota_used += 1

    items = r.json().get("items", [])

    video = items[0]

    snippet = video["snippet"]
    stats = video.get("statistics", {})
    video_id = video["id"]

    duration = video.get("contentDetails", {}).get("duration", "")

    if duration == "" or duration == "P0D":
        raise ValueError("Video is still processing, please try again!")

    platform = detect_short(video_id)
    
    topic = None

    published_at = snippet.get("publishedAt", "") 

    results.append((
        video_id,
        snippet["title"],
        snippet.get("description", ""),
        str(snippet.get("tags", [])),
        snippet.get("categoryId", ""),
        snippet.get("channelTitle", ""),
        published_at,
        int(stats.get("viewCount", 0)),
        int(stats.get("likeCount", 0)),
        int(stats.get("commentCount", 0)),
        platform,
        topic,
        fetch_time,
        video.get("contentDetails", {}).get("duration", "")
    ))

    print(f"Fetched {len(items)} videos (quota: {quota_used})")

    time.sleep(Settings.THROTTLE)

    return results