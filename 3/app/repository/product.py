from app.models import Product
from app.repository.base import BaseRepo


class ProductRepository(BaseRepo):
    @property
    def model(self):
        return Product
