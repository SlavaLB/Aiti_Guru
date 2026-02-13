from fastapi import APIRouter, status

from app.core.depends import OrdersApplicationDep

router = APIRouter()


@router.get(
    "/my_orders/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Получение информации о заказах пользователя по id"
)
async def get_my_orders(
        order_application: OrdersApplicationDep,
        user_id: int,
):
    """
    Получение информации о заказах пользователя по id
    """
    return await order_application.get_user_orders_info(user_id=user_id)
