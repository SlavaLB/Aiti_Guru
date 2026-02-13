from fastapi import APIRouter

from .categories import get_router as get_router_categories
from .order import get_router as get_router_orders
from .order import post_router as post_router_orders
main_router = APIRouter()

main_router.include_router(get_router_categories, tags=["Категории"])
main_router.include_router(get_router_orders, tags=["Заказы"])
main_router.include_router(post_router_orders, tags=["Заказы"])
