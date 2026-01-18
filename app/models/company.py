"""
Company 모델
Company-Article = 단방향 관계
Company를 통해 Article은 참조가능하지만, Article에서 Company는 참조 불가능
Company 삭제 시 cascade 옵션을 통해 Article도 함께 삭제되도록 함
"""

from datetime import date
from typing import List
from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    
    articles: Mapped[List["Article"]] = relationship("Article", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"Company(id={self.id}, name={self.name}, created_at={self.created_at})"
