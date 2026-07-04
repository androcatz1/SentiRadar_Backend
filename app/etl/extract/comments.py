import requests
import time

from datetime import datetime

from app.config.settings import Settings

async def fetch_top_level_comments(video_id, max_pages=None):
    quota_used = 0
    comments = []
    page_token = None
    pages_fetched = 0
    fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    while True:

        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "key": Settings.YOUTUBE_API_KEY,
            "pageToken": page_token
        }

        r = requests.get(f"{Settings.BASE_URL}/commentThreads", params=params)
        data = r.json()

        for item in data.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "video_id": video_id,
                "text": snippet["textDisplay"],
                "likes": snippet.get("likeCount", 0),
                "reply_count": item["snippet"].get("totalReplyCount",0),
                "published_at": snippet["publishedAt"],
                "fetched_at": fetch_time
            })

        quota_used += 1
        print(f"Quota used: {quota_used} / {Settings.MAX_QUOTA}")

        page_token = data.get("nextPageToken")
        pages_fetched += 1
        if not page_token or (max_pages and pages_fetched >= max_pages):
            break

        # Optional throttle for safety
        time.sleep(0.2)

    return comments

