import asyncio
from typing import List, Dict, Any

from sqlalchemy.exc import SQLAlchemyError

from app.models import Product, Category
from app.repository.category import CategoryRepository


class CategoryDomainLogic:
    """Доменная логика для категории"""

    def __init__(
            self,
            category_repository: CategoryRepository,
    ):
        self.category_repository = category_repository

    async def build_category_tree(self) -> List[Dict[str, Any]]:
        """
        Строит дерево категорий, загружая каждый уровень по мере необходимости.
        Использует relationship, но контролирует загрузку через репозиторий.
        """

        # logger.info("Начало построения дерева категорий")
        try:
            root_categories = await self.category_repository.get_root_categories()
        except SQLAlchemyError as e:
            # logger.error(f"Ошибка БД при загрузке корневых категорий: {e}")
            raise
        except asyncio.TimeoutError as e:
            # logger.error(f"Таймаут при загрузке корневых категорий: {e}")
            raise

        # logger.debug(f"Загружено корневых категорий: {len(root_categories)}")

        if not root_categories:
            # logger.info("Корневые категории не найдены")
            return []

        tree = []
        for root in root_categories:
            try:
                category_node = await self._build_category_node(root)
                tree.append(category_node)
            except (ValueError, KeyError) as e:
                # logger.error(f"Ошибка данных при обработке корневой категории ID {root.id}: {e}")
                continue
            except SQLAlchemyError as e:
                # logger.error(f"Ошибка БД при обработке корневой категории ID {root.id}: {e}")
                continue
            except asyncio.CancelledError:
                # logger.warning(f"Отмена задачи при обработке категории ID {root.id}")
                raise
            except Exception as e:
                # logger.critical(
                #    f"Неизвестная критическая ошибка при обработке категории ID {root.id}: {type(e).__name__}: {e}")
                continue
        # logger.info(f"Построено дерево категорий: {len(tree)} корневых узлов")
        return tree

    async def _build_category_node(self, category: Category) -> Dict[str, Any]:
        """
        Рекурсивно строит узел категории, загружая детей при необходимости.
        """
        # logger.debug(f"Построение узла для категории ID {category.id}: {category.name}")

        node = {
            "id": category.id,
            "category_name": category.name,
            "root_category_id": category.root_category_id,
            "parent_name": category.parent.name if category.parent else None,
        }

        try:
            if category.products:
                node["products"] = await self._format_products(category.products)
        except (TypeError, ValueError) as e:
            # logger.warning(f"Ошибка форматирования продуктов для категории ID {category.id}: {e}")
            node["products"] = []
            node["products_count"] = 0
        except SQLAlchemyError as e:
            # logger.error(f"Ошибка БД при доступе к продуктам категории ID {category.id}: {e}")
            node["products"] = []
            node["products_count"] = 0

        try:
            child_categories = await self.category_repository.get_child_categories(category.id)
        except SQLAlchemyError as e:
            # logger.error(f"Ошибка БД при загрузке дочерних категорий для ID {category.id}: {e}")
            child_categories = []
        except asyncio.TimeoutError as e:
            # logger.error(f"Таймаут при загрузке дочерних категорий для ID {category.id}: {e}")
            child_categories = []

        if child_categories:
            node["children"] = []
            for child in child_categories:
                try:
                    child_node = await self._build_category_node(child)
                    node["children"].append(child_node)
                except RecursionError as e:
                    # logger.error(f"Рекурсия слишком глубокая при обработке категории ID {child.id}: {e}")
                    continue
                except SQLAlchemyError as e:
                    # logger.error(f"Ошибка БД при обработке дочерней категории ID {child.id}: {e}")
                    continue
                except (ValueError, KeyError) as e:
                    # logger.error(f"Ошибка данных при обработке дочерней категории ID {child.id}: {e}")
                    continue

            node["children_count"] = len(node["children"])

        return node

    @staticmethod
    async def _format_products(products: List[Product]) -> List[Dict]:
        """
        Форматирует список продуктов.
        """
        return [
            {
                "id": p.id,
                "name": p.name,
                "price": float(p.price) if p.price else 0,
                "quantity": p.quantity or 0,
            }
            for p in products
        ]
