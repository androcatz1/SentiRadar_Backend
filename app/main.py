from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import comments, videos, analytics, time_series, model


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# 2. Inject the CORS structural pipeline layer
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows your React server to read values
    allow_credentials=True,
    allow_methods=["*"],              # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],              # Allows all custom content headers
)


app.include_router(comments.router)
app.include_router(videos.router)
app.include_router(analytics.router)
app.include_router(time_series.router)
app.include_router(model.router)