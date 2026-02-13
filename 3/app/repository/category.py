from typing import Sequence

from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.models import Category
from app.repository.base import BaseRepo


class CategoryRepository(BaseRepo):
    @property
    def model(self):
        return Category

    async def get_root_categories(self) -> Sequence[Category]:
        """
        Загружает только корневые категории с продуктами.
        """
        stmt = select(Category).where(
            Category.parent_id.is_(None)
        ).options(
            selectinload(Category.products)
        ).order_by(Category.id)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_child_categories(self, parent_id: int) -> Sequence[Category]:
        """
        Загружает дочерние категории для указанного родителя.
        """
        stmt = select(Category).where(
            Category.parent_id == parent_id
        ).options(
            selectinload(Category.products)
        ).order_by(Category.id)

        result = await self.session.execute(stmt)
        return result.scalars().all()
