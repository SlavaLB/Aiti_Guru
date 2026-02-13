from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select

from app.models import Order, OrderItem
from app.repository.base import BaseRepo


class OrderRepository(BaseRepo):
    @property
    def model(self):
        return Order

    @property
    def order_item_model(self):
        return OrderItem

    async def get_user_orders_with_items(self, user_id: int):
        """
        Получает все заказы пользователя с позициями и товарами.
        """
        stmt = select(self.model).where(
            self.model.customer_id == user_id
        ).options(
            selectinload(Order.items).selectinload(OrderItem.product),
            joinedload(Order.customer)
        ).order_by(
            Order.created_at.desc()
        )

        result = await self.session.execute(stmt)
        orders = result.unique().scalars().all()

        return orders

    async def get_by_id(self, order_id: int):
        query = select(self.model).where(self.model.id == order_id).options(
            selectinload(self.model.items)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_order_items(
            self,
            order_id: int,
            product_id: int,
            quantity: int,
            price_at_order: int
    ):
        """Создать новый элемент заказа."""
        new_item = self.order_item_model(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price_at_order=price_at_order
        )
        self.session.add(new_item)
