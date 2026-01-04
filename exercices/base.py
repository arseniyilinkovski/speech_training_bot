from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseExercise(ABC):
    """Базовый класс для упражнений"""

    def __init__(self, name: str, description: str, experience: int):
        self.name = name
        self.description = description
        self.experience = experience

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Выполнение упражнения"""
        pass

    @abstractmethod
    async def validate(self, user_input: Any) -> bool:
        """Валидация ответа пользователя"""
        pass