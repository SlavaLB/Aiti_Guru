from sqlalchemy import (
    ForeignKey,
    Numeric, UniqueConstraint,
    CheckConstraint, Integer
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    __table_args__ = (
        UniqueConstraint("order_id", "product_id",
                         name="uq_order_product"),
        CheckConstraint("quantity > 0",
                        name="check_order_quantity_positive"),
        CheckConstraint("price_at_order >= 0",
                        name="check_price_at_order_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        index=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"),
        index=True
    )

    quantity: Mapped[int]
    price_at_order: Mapped[float] = mapped_column(Numeric(12, 2))

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")
