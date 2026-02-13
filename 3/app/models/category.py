from typing import List

from sqlalchemy import (
    Integer, String, ForeignKey, DateTime
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.core.db import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )
    root_category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True
    )
    parent: Mapped["Category"] = relationship(
        "Category",
        back_populates="children",
        remote_side=[id],
        foreign_keys=[parent_id],
    )

    children: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="parent",
        foreign_keys=[parent_id],
        cascade="all, delete"
    )

    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
        foreign_keys="Product.category_id",
        lazy="selectin"
    )

    # Продукты, у которых эта категория - корневая
    root_products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="root_category",
        foreign_keys="Product.root_category_id",
        lazy="selectin"
    )
