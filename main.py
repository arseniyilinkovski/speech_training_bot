import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers.registration import router as registration_router
from handlers.exercices import router as exercises_router
from handlers.profile_reply import router as profile_reply_router
from handlers.profile import router as profile_router
from handlers.start import router as start_router
from handlers.cleanup import router as cleanup_router
from handlers.profile_buttons import router as profile_buttons_router  # НОВЫЙ РОУТЕР
from utils.notifications import NotificationScheduler
from utils.message_manager import message_manager

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация всех роутеров
    dp.include_router(registration_router)
    dp.include_router(exercises_router)
    dp.include_router(profile_reply_router)
    dp.include_router(profile_router)
    dp.include_router(start_router)
    dp.include_router(cleanup_router)
    dp.include_router(profile_buttons_router)  # ДОБАВЛЯЕМ

    # Middleware для управления сообщениями
    @dp.update.middleware()
    async def message_cleanup_middleware(handler, event, data):
        result = await handler(event, data)

        if hasattr(event, 'from_user'):
            user_id = event.from_user.id
            await message_manager.cleanup_user(user_id, keep_last=3, bot=bot)  # Увеличиваем до 3 сообщений

        return result

    # Запуск планировщика уведомлений
    scheduler = NotificationScheduler(bot)
    asyncio.create_task(scheduler.start())

    try:
        print("🤖 Бот запущен! Нажмите Ctrl+C для остановки.")
        await dp.start_polling(bot)
    finally:
        scheduler.stop()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())