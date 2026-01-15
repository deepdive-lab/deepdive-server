from datetime import date
from sqlalchemy import String, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    original_url: Mapped[str] = mapped_column(String(255), nullable=False)
    thumbnail_url: Mapped[str] = mapped_column(String(255), nullable=False)

    published_at: Mapped[date] = mapped_column(Date, nullable=False)
    read_time: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    view_count: Mapped[int] = mapped_column(Integer, nullable=False)

    company: Mapped["Company"] = relationship("Company", back_populates="articles")

    def __repr__(self) -> str:
        return f"Article(id={self.id}, company_id={self.company_id}, title={self.title}, description={self.description}, published_at={self.published_at})"
