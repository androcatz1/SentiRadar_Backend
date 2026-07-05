from fastapi import FastAPI
from app.routers import comments, videos, analytics


app = FastAPI()

app.include_router(comments.router)
app.include_router(videos.router)
app.include_router(analytics.router)