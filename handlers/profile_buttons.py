from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from keyboards.inline import get_profile_menu, get_training_menu, get_courses_keyboard, get_main_menu
from database.json_db import JSONDatabase
from config import USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH

router = Router()
db = JSONDatabase(USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH)


@router.callback_query(F.data == "show_profile")
async def show_profile_callback(callback: CallbackQuery):
    """Показать профиль по inline-кнопке"""
    user = db.load_user(callback.from_user.id)

    if not user:
        await callback.answer("Пользователь не найден", show_alert=True)
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

    try:
        # Пытаемся отредактировать текущее сообщение
        await callback.message.edit_text(
            profile_text,
            parse_mode="Markdown",
            reply_markup=get_profile_menu()
        )
    except TelegramBadRequest:
        # Если не удалось отредактировать, отправляем новое сообщение
        await callback.message.answer(
            profile_text,
            parse_mode="Markdown",
            reply_markup=get_profile_menu()
        )

    await callback.answer()


@router.callback_query(F.data == "course_speech")
async def speech_course(callback: CallbackQuery):
    """Переход к речевой тренировке"""
    try:
        # Пытаемся отредактировать текущее сообщение
        await callback.message.edit_text(
            "🗣️ *Тренировка речи*\n\n"
            "Выберите действие:",
            parse_mode="Markdown",
            reply_markup=get_training_menu()
        )
    except:
        # Если не удалось отредактировать, отправляем новое сообщение
        await callback.message.answer(
            "🗣️ *Тренировка речи*\n\n"
            "Выберите действие:",
            parse_mode="Markdown",
            reply_markup=get_training_menu()
        )

    await callback.answer()


@router.callback_query(F.data == "my_courses")
async def my_courses(callback: CallbackQuery):
    """Показать мои курсы"""
    try:
        # Пытаемся отредактировать текущее сообщение
        await callback.message.edit_text(
            "📚 *Мои курсы*\n\n"
            "Выберите курс для тренировки:",
            parse_mode="Markdown",
            reply_markup=get_courses_keyboard()
        )
    except:
        # Если не удалось отредактировать, отправляем новое сообщение
        await callback.message.answer(
            "📚 *Мои курсы*\n\n"
            "Выберите курс для тренировки:",
            parse_mode="Markdown",
            reply_markup=get_courses_keyboard()
        )

    await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """Возврат в главное меню"""
    try:
        # Пытаемся отредактировать текущее сообщение
        await callback.message.edit_text(
            "🏠 *Главное меню*\n\n"
            "Выберите действие:",
            parse_mode="Markdown",
            reply_markup=get_main_menu()
        )
    except:
        # Если не удалось отредактировать, отправляем новое сообщение
        await callback.message.answer(
            "🏠 *Главное меню*\n\n"
            "Выберите действие:",
            parse_mode="Markdown",
            reply_markup=get_main_menu()
        )

    await callback.answer()