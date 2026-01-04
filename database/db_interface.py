from abc import ABC, abstractmethod
from typing import Optional, List
from models.user import User


class DatabaseInterface(ABC):
    @abstractmethod
    def save_user(self, user: User):
        pass

    @abstractmethod
    def load_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass