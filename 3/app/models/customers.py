from typing import List

from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.db import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="customer")
