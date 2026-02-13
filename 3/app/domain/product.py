from app.core.exceptions import ProductNotFoundError, InsufficientStockError
from app.models import Product
from app.repository.product import ProductRepository
from app.schemas.orders import AddItemToOrderRequest


class ProductDomainLogic:
    """Доменная логика для пользователей"""

    def __init__(
            self,
            product_repository: ProductRepository
    ):
        self.product_repository = product_repository

    async def get_product_by_id(self, product_id: int):
        product = await self.product_repository.get_by_id(id=product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product

    @staticmethod
    async def check_quantity_product(product: Product, data: AddItemToOrderRequest):
        if product.quantity < data.quantity:
            raise InsufficientStockError(
                product_id=product.id,
                requested=data.quantity,
                available=product.quantity
            )
