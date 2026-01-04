import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID", "")

# Пути к файлам данных
USERS_JSON_PATH = "data/users.json"
EXERCISES_JSON_PATH = "data/exercises.json"
TEXTS_JSON_PATH = "data/texts.json"

# Настройки упражнений
EXERCISE_TYPES = {
    "tongue_twister": "Скороговорка",
    "reading": "Чтение вслух",
    "description": "Описание предмета"
}

# Время для напоминаний (по умолчанию)
DEFAULT_NOTIFICATION_TIMES = ["09:00", "13:00", "19:00"]