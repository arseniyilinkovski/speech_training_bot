import asyncio
from datetime import datetime, time
from aiogram import Bot
from database.json_db import JSONDatabase
from config import USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH


class NotificationScheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.db = JSONDatabase(USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH)
        self.is_running = True

    async def start(self):
        """Запуск планировщика уведомлений"""
        while self.is_running:
            now = datetime.now()
            current_time = now.strftime("%H:%M")

            users = self.db.get_all_users()
            for user in users:
                if user.notifications_enabled and current_time in user.notification_times:
                    await self.send_notification(user)

            # Проверяем каждую минуту
            await asyncio.sleep(60)

    async def send_notification(self, user):
        """Отправка уведомления пользователю"""
        try:
            message = (
                f"🔔 Напоминание о тренировке!\n\n"
                f"Не забудьте выполнить упражнение сегодня, "
                f"чтобы продлить серию {user.streak_days} дней! 🔥\n\n"
                f"Нажмите /start для начала тренировки"
            )
            await self.bot.send_message(user.user_id, message)
        except Exception as e:
            print(f"Ошибка отправки уведомления пользователю {user.user_id}: {e}")

    def stop(self):
        """Остановка планировщика"""
        self.is_running = False