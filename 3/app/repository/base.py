from abc import ABC, abstractmethod
from typing import Type, TypeVar, Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)


class BaseRepo(ABC):
    """Абстрактный сервис для работы с одной моделью"""

    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    @abstractmethod
    def model(self) -> Type[T]:
        """Модель SQLAlchemy, с которой работает сервис"""
        ...

    async def get_by_id(self, id: int) -> Optional[T]:
        """Возвращает объект по ID"""
        return await self.session.get(self.model, id)

    async def get_all(self) -> List[T]:
        """Возвращает все объекты"""
        result = await self.session.execute(select(self.model).options())
        return result.scalars().all()

    async def get_by_filter(self, **filters) -> List[T]:
        """Возвращает объекты по фильтрам (равенство)"""
        stmt = select(self.model)
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add(self, obj: T) -> None:
        """Добавляет объект в сессию"""
        self.session.add(obj)

    async def add_all(self, objects: List[T]) -> None:
        """Добавляет несколько объектов в сессию"""
        self.session.add_all(objects)

    async def delete(self, obj: T) -> None:
        """Удаляет объект"""
        await self.session.delete(obj)

    @staticmethod
    async def update_fields(obj: T, **kwargs) -> T:
        """Обновляет указанные поля объекта"""
        for key, value in kwargs.items():
            setattr(obj, key, value)
        return obj

    async def create_or_update(self, id_obj: int, **kwargs) -> T:
        """Создает или обновляет объект по id"""
        stmt = select(self.model).where(self.model.id == id_obj)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()

        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
        else:
            obj = self.model(id=id_obj, **kwargs)
            self.session.add(obj)

        return obj

    async def create(self, **kwargs) -> T:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        return obj
