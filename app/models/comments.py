from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class CommentsModel(Base):
    __tablename__ = "comments_test"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement= True)
    video_id: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(String)
    text_processed: Mapped[str] = mapped_column(String)
    text_no_stopwords: Mapped[str] = mapped_column(String)
    label: Mapped[int] = mapped_column(Integer)


