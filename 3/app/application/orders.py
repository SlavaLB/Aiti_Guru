from app.domain.orders import OrderDomainLogic
from app.domain.product import ProductDomainLogic
from app.repository.orders import OrderRepository
from app.repository.product import ProductRepository
from app.schemas.orders import AddItemToOrderRequest


class OrdersApplication:
    """Сервис приложения для работы с заказами"""

    def __init__(
            self,
            order_repository: OrderRepository,
            product_repository: ProductRepository
    ):
        # Инициализируем репозитории
        self.order_repository = order_repository
        self.product_repository = product_repository
        ###
        # Создаем доменные сервисы
        self.order_domain = OrderDomainLogic(
            order_repository=self.order_repository
        )
        self.product_domain = ProductDomainLogic(
            product_repository=self.product_repository
        )

    async def get_user_orders_info(self, user_id: int):
        # Получение заказов пользователя
        user_items = await self.order_domain.get_user_orders_with_items(user_id=user_id)
        return user_items

    async def add_item_to_order(self, data: AddItemToOrderRequest):
        # 1. Получение Продукта
        product = await self.product_domain.get_product_by_id(product_id=data.product_id)

        # 2. Проверка, что достаточно количества которое запрашивают
        await self.product_domain.check_quantity_product(product=product, data=data)

        # 3. Поиск заказа, если нет, вернуть 404
        order = await self.order_domain.get_order_by_id(data.order_id)

        # Сохраняем состояние "на виду в методе" "БЫЛО" до изменений чтобы в свагере вам было проще
        before_state = {
            "order_id": order.id,
            "customer_id": order.customer_id,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price_at_order": float(item.price_at_order) if item.price_at_order else None
                }
                for item in order.items
            ]
        }

        # 4. Проверяем, есть ли уже такой товар в заказе
        existing_item = await self.order_domain.check_exist(items=order.items, product_id=data.product_id)

        if existing_item:
            # Обновляем объект
            await self.order_domain.update_order_item(item=existing_item, quantity=data.quantity, price=product.price)
        else:
            # Если товара нет в заказе - создаем новый элемент заказа
            await self.order_repository.create_order_items(
                order_id=order.id,
                product_id=product.id,
                quantity=data.quantity,
                price_at_order=product.price
            )

        # 5. Уменьшаем количество продукта на складе
        product.quantity -= data.quantity

        # Как изменился объект для свагера
        after_state = {
            "order_id": order.id,
            "customer_id": order.customer_id,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price_at_order": float(item.price_at_order) if item.price_at_order else None
                }
                for item in order.items
            ]
        }

        # 6. Сохраняем изменения
        await self.order_repository.session.commit()
        # Возвращаем результат с состояниями
        return {
            "message": "Успех",
            "before": before_state,
            "after": after_state,
            "changes": {
                "product_id": data.product_id,
                "quantity_added": data.quantity,
                "action": "updated" if existing_item else "created"
            }
        }
