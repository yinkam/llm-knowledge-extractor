from datetime import datetime

from sqlalchemy import func, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.app.database.connection import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text_input: Mapped[str] = mapped_column(Text, nullable=True)
    summary: Mapped[str] = mapped_column(nullable=True)
    title: Mapped[str] = mapped_column(nullable=True)
    sentiment: Mapped[str] = mapped_column(nullable=True)
    keywords: Mapped[str] = mapped_column(JSON, nullable=True)
    topics: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    confidence_score: Mapped[float] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())


