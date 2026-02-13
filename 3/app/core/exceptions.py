from typing import Any, Dict, Optional


class BaseAppException(Exception):
    """Базовое исключение для всех кастомных ошибок приложения"""
    def __init__(
        self,
        status_code: int = 500,
        detail: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.detail = detail or {"error": "INTERNAL_ERROR", "message": "Внутренняя ошибка"}
        super().__init__(str(self.detail))


class OrderNotFoundError(BaseAppException):
    """Исключение: заказ не найден"""
    def __init__(self, order_id: int):
        super().__init__(
            status_code=404,
            detail={
                "error": "ORDER_NOT_FOUND",
                "message": f"Заказ с ID {order_id} не найден",
                "order_id": order_id
            }
        )


class ProductNotFoundError(BaseAppException):
    """Исключение: товар не найден"""
    def __init__(self, product_id: int):
        super().__init__(
            status_code=404,
            detail={
                "error": "PRODUCT_NOT_FOUND",
                "message": f"Товар с ID {product_id} не найден",
                "product_id": product_id
            }
        )


class InsufficientStockError(BaseAppException):
    """Исключение: недостаточно товара на складе"""
    def __init__(self, product_id: int, requested: int, available: int):
        super().__init__(
            status_code=400,
            detail={
                "error": "INSUFFICIENT_STOCK",
                "message": f"Недостаточно товара ID {product_id}. Запрошено: {requested}, доступно: {available}",
                "product_id": product_id,
                "requested": requested,
                "available": available
            }
        )


class OrderCannotBeModifiedError(BaseAppException):
    """Исключение: заказ нельзя изменить"""
    def __init__(self, order_id: int, status: str):
        super().__init__(
            status_code=400,
            detail={
                "error": "ORDER_CANNOT_BE_MODIFIED",
                "message": f"Заказ ID {order_id} со статусом '{status}' нельзя изменить",
                "order_id": order_id,
                "status": status
            }
        )


class ValidationError(BaseAppException):
    """Исключение: ошибка валидации"""
    def __init__(self, message: str, field: Optional[str] = None):
        detail = {
            "error": "VALIDATION_ERROR",
            "message": message
        }
        if field:
            detail["field"] = field
        super().__init__(status_code=422, detail=detail)
