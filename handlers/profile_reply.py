from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from database.json_db import JSONDatabase
from config import USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH
from keyboards.inline import get_main_menu
from keyboards.reply import get_profile_reply_keyboard

router = Router()
db = JSONDatabase(USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH)


@router.message(F.text.lower() == "📊 мой профиль")
@router.message(F.text.lower() == "мой профиль")
@router.message(Command("profile"))
async def show_profile(message: Message):
    """Показать профиль пользователя с inline-кнопками"""
    user = db.load_user(message.from_user.id)

    if not user:
        await message.answer(
            "Вы еще не зарегистрированы. Используйте /start",
            reply_markup=get_profile_reply_keyboard()
        )
        return

    # Рассчитываем уровень и прогресс
    speech_exp = user.course_experience.get("speech", 0)
    level = speech_exp // 100 + 1
    progress = speech_exp % 100
    progress_bar = "▓" * int(progress / 10) + "░" * (10 - int(progress / 10))

    profile_text = (
        f"👤 *Ваш профиль*\n\n"
        f"*Имя:* {user.first_name} {user.last_name}\n"
        f"*Серия дней:* {user.streak_days} 🔥\n"
        f"*Общий опыт:* {user.total_experience} XP\n\n"
        f"*Курс «Речь»:*\n"
        f"Уровень {level} ({progress}/100 XP)\n"
        f"{progress_bar}\n\n"
        f"*Сегодня выполнено:* {'✅ Да' if user.completed_today else '❌ Нет'}\n"
        f"*Зарегистрирован:* {user.registered_at[:10]}"
    )

    # Отправляем профиль с inline-меню
    await message.answer(
        profile_text,
        parse_mode="Markdown",
        reply_markup=get_main_menu()
    )