from typing import Any

from app.domain.category import CategoryDomainLogic
from app.repository.category import CategoryRepository


class CategoryApplication:
    """Сервис приложения для работы с пользователями"""

    def __init__(
            self,
            category_repository: CategoryRepository,
    ):
        # Инициализируем репозитории
        self.category_repository = category_repository
        ###
        # Создаем доменные сервисы
        self.pages_domain = CategoryDomainLogic(category_repository=self.category_repository)

    async def get_info_for_index_page(self) -> list[dict[str, Any]]:
        # 1. Получение дерева категорий
        return await self.pages_domain.build_category_tree()
