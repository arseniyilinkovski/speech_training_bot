from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_main_menu
from database.json_db import JSONDatabase
from config import USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH

router = Router()
db = JSONDatabase(USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH)


@router.callback_query(F.data == "my_progress")
async def show_progress(callback: CallbackQuery):
    user = db.load_user(callback.from_user.id)

    if not user:
        await callback.answer("Пользователь не найден", show_alert=True)
        return

    progress_text = (
        f"📊 *Ваш прогресс*\n\n"
        f"👤 {user.first_name} {user.last_name}\n"
        f"🔥 Серия дней: {user.streak_days}\n"
        f"💰 Всего опыта: {user.total_experience} XP\n\n"
        f"*По курсам:*\n"
    )

    for course, exp in user.course_experience.items():
        level = exp // 100 + 1
        progress = exp % 100
        progress_text += f"• {course.capitalize()}: Уровень {level} ({progress}/100 XP)\n"

    progress_text += f"\n✅ Сегодня выполнено: {'Да' if user.completed_today else 'Нет'}"

    try:
        # Пытаемся отредактировать текущее сообщение
        await callback.message.edit_text(
            progress_text,
            parse_mode="Markdown",
            reply_markup=get_main_menu()
        )
    except:
        # Если не удалось отредактировать, отправляем новое сообщение
        await callback.message.answer(
            progress_text,
            parse_mode="Markdown",
            reply_markup=get_main_menu()
        )

    await callback.answer()