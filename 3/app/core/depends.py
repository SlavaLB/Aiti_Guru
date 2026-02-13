from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.orders import OrdersApplication
from app.application.pages import CategoryApplication
from app.core.db import AsyncSessionLocal
from app.repository.orders import OrderRepository
from app.repository.category import CategoryRepository
from app.repository.product import ProductRepository


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def get_category_application(
        db: Annotated[AsyncSession, Depends(get_async_session)]
) -> CategoryApplication:
    """
    Зависимость для получения PagesApplication.
    Инжектирует все зависимости в одном месте.
    """
    # Создаем репозитории
    category_repository = CategoryRepository(session=db)

    # Создаем и возвращаем CategoryApplication
    return CategoryApplication(category_repository=category_repository)


async def get_orders_application(
        db: Annotated[AsyncSession, Depends(get_async_session)]
) -> OrdersApplication:
    """
    Зависимость для получения OrdersApplication.
    Инжектирует все зависимости в одном месте.
    """
    # Создаем репозитории
    order_repository = OrderRepository(session=db)
    product_repository = ProductRepository(session=db)

    # Создаем и возвращаем OrdersApplication
    return OrdersApplication(order_repository=order_repository, product_repository=product_repository)


CategoryApplicationDep = Annotated[CategoryApplication, Depends(get_category_application)]
OrdersApplicationDep = Annotated[OrdersApplication, Depends(get_orders_application)]
