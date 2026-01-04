import json
import os
from typing import Dict, List, Any, Optional
from models.user import User


class JSONDatabase:
    def __init__(self, users_path: str, exercises_path: str, texts_path: str):
        self.users_path = users_path
        self.exercises_path = exercises_path
        self.texts_path = texts_path
        self._ensure_directories()
        self._init_files()

    def _ensure_directories(self):
        """Создает директории если их нет"""
        os.makedirs(os.path.dirname(self.users_path), exist_ok=True)

    def _init_files(self):
        """Инициализирует JSON файлы если их нет"""
        for path in [self.users_path, self.exercises_path, self.texts_path]:
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump({}, f)

    # Методы для работы с пользователями
    def save_user(self, user: User):
        users = self.load_users()
        users[str(user.user_id)] = user.to_dict()
        self._save_data(self.users_path, users)

    def load_user(self, user_id: int) -> Optional[User]:
        users = self.load_users()
        user_data = users.get(str(user_id))
        if user_data:
            return User.from_dict(user_data)
        return None

    def load_users(self) -> Dict:
        with open(self.users_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_all_users(self) -> List[User]:
        users_data = self.load_users()
        return [User.from_dict(data) for data in users_data.values()]

    # Методы для упражнений и текстов
    def load_exercises(self) -> Dict:
        with open(self.exercises_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_texts(self) -> Dict:
        with open(self.texts_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self, path: str, data: Dict):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)