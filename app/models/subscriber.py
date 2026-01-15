from datetime import date
from sqlalchemy import String, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Subscriber(Base):
    __tablename__ = "subscribers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[date] = mapped_column(Date, default=date.today)
    
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
