from app.core.exceptions import OrderNotFoundError
from app.models import OrderItem
from app.repository.orders import OrderRepository
from app.schemas.orders import AddItemToOrderRequest


class OrderDomainLogic:
    """Доменная логика для пользователей"""

    def __init__(
            self,
            order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    async def get_user_orders_with_items(self, user_id: int):
        return await self.order_repository.get_user_orders_with_items(user_id=user_id)

    async def get_order_by_id(self, order_id: int):
        order = await self.order_repository.get_by_id(order_id=order_id)
        if not order:
            raise OrderNotFoundError(order_id)
        return order

    @staticmethod
    async def check_exist(items, product_id: int):
        """
            Ищет позицию товара в заказе.
            Возвращает OrderItem если товар уже есть в заказе, иначе None.
        """
        for item in items:
            if item.product_id == product_id:
                return item

    @staticmethod
    async def update_order_item(item: OrderItem, quantity: int, price: int):
        """
            Увеличивает количество товара на указанное значение и
            устанавливает актуальную цену товара на момент обновления.
        """
        item.quantity += quantity
        item.price_at_order = price
