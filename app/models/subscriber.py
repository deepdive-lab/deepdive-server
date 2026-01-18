"""
Subscriber 모델
Subscriber-Subscription = 단방향 관계
Subscriber를 통해 Subscription은 참조가능하지만, Subscription에서 Subscriber는 참조 불가능
Subscriber 삭제 시 cascade 옵션을 통해 Subscription도 함께 삭제되도록 수 있도록 함
"""

from datetime import date
from typing import List
from sqlalchemy import String, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class Subscriber(Base):
    __tablename__ = "subscribers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)
    
    subscriptions: Mapped[List["Subscription"]] = relationship("Subscription", back_populates="subscriber", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"Subscriber(id={self.id}, email={self.email}, created_at={self.created_at})"

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subscriber_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscribers.id"), nullable=False)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("companies.id"), nullable=False)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)
     
    def __repr__(self) -> str:
        return f"Subscription(id={self.id}, subscriber_id={self.subscriber_id}, company_id={self.company_id}, created_at={self.created_at})"
