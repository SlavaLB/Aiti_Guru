from fastapi import APIRouter, HTTPException, status

from app.core.depends import OrdersApplicationDep
from app.core.exceptions import OrderNotFoundError, ProductNotFoundError, InsufficientStockError
from app.schemas.orders import ErrorResponse, AddItemToOrderRequest

router = APIRouter()


@router.post(
    "/items/add",
    summary="Добавление товара в заказ",
    description="""
    Добавляет товар в существующий заказ.

    - Если товар уже есть в заказе, его количество увеличивается
    - Если товара нет в наличии, возвращается ошибка
    - Цена фиксируется на момент добавления
    """,
    responses={
        200: {"description": "Товар успешно добавлен в заказ"},
        400: {"model": ErrorResponse, "description": "Ошибка валидации или недостаточно товара"},
        404: {"model": ErrorResponse, "description": "Заказ или товар не найдены"},
        500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"}
    }
)
async def add_item_to_order(
    data: AddItemToOrderRequest,
    order_application: OrdersApplicationDep,
):
    """
        Добавляет товар в заказ.

        **Параметры запроса:**
        - **order_id**: ID заказа (обязательно, >0)
        - **product_id**: ID товара (обязательно, >0)
        - **quantity**: Количество (обязательно, от 1 до 9999)
        - **note**: Примечание (опционально)

        **Возвращает:**
        - Обновленную информацию о заказе

        **Возможные ошибки:**
        - 400: Недостаточно товара или превышен лимит
        - 404: Заказ или товар не найдены
    """

    try:
        # История операций по добавлению товар в заказ
        return await order_application.add_item_to_order(data=data)

    except OrderNotFoundError as e:
        # logger.warning(f"Заказ не найден: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": str(e), "error_code": "ORDER_NOT_FOUND"}
        )
    except ProductNotFoundError as e:
        # logger.warning(f"Товар не найден: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"detail": str(e), "error_code": "PRODUCT_NOT_FOUND"}
        )
    except InsufficientStockError as e:
        # logger.warning(f"Недостаточно товара: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"detail": str(e), "error_code": "INSUFFICIENT_STOCK"}
        )
    except Exception as e:
        # logger.error(f"Внутренняя ошибка сервера: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"detail": "Внутренняя ошибка сервера", "error_code": "INTERNAL_ERROR"}
        )
