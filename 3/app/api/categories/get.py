from fastapi import APIRouter, status

from app.core.depends import CategoryApplicationDep

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Получение категорий"
)
async def get_me_info(
        pages_application: CategoryApplicationDep,
):
    """
    Получение категорий + вложенных категорий и товаров
    """
    # 1. История операций в PagesApplication
    return await pages_application.get_info_for_index_page()
