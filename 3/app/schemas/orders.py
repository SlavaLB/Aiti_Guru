from pydantic import BaseModel, Field, ConfigDict


class AddItemToOrderRequest(BaseModel):
    """
    Схема запроса на добавление товара в заказ.
    """
    order_id: int = Field(..., gt=0, description="ID заказа", examples=[1,])
    product_id: int = Field(..., gt=0, description="ID товара (номенклатуры)", examples=[42,])
    quantity: int = Field(..., gt=0, le=9999, description="Количество товара", examples=[2,])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "order_id": 1,
                "product_id": 1,
                "quantity": 1
            }
        }
    )


class ErrorResponse(BaseModel):
    """
    Схема ответа с ошибкой.
    """
    detail: str = Field(..., description="Детальное описание ошибки")
    error_code: str = Field(..., description="Код ошибки")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Недостаточно товара на складе",
                "error_code": "INSUFFICIENT_STOCK"
            }
        }
    )