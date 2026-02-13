from typing import Optional

from sqlalchemy import (
    Integer, String, ForeignKey,
    DateTime, Numeric, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.db import Base


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_positive"),
        CheckConstraint("quantity >= 0", name="check_quantity_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    quantity: Mapped[int | None]
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    root_category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    category: Mapped[Optional["Category"]] = relationship(
        "Category",
        foreign_keys=[category_id],
        back_populates="products"
    )

    # Связь с корневой категорией
    root_category: Mapped[Optional["Category"]] = relationship(
        "Category",
        foreign_keys=[root_category_id],
        back_populates="root_products"
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product"
    )