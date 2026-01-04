from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from models.user import User
from database.json_db import JSONDatabase
from config import USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH
from keyboards.reply import get_profile_reply_keyboard
from keyboards.inline import get_notification_skip_keyboard, get_main_menu
from datetime import datetime
import re

router = Router()
db = JSONDatabase(USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH)


class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_notifications = State()


def validate_time_format(time_str: str) -> bool:
    """Проверяет формат времени HH:MM"""
    pattern = r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$'
    return bool(re.match(pattern, time_str.strip()))


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    # Удаляем команду /start
    await message.delete()

    user = db.load_user(message.from_user.id)

    if user:
        # Просто отправляем новое сообщение
        await message.answer(
            f"👋 С возвращением, {user.first_name}!\n"
            f"Ваша серия: {user.streak_days} дней 🔥\n"
            f"Опыт: {user.total_experience} XP",
            reply_markup=get_profile_reply_keyboard()
        )
        await state.clear()
    else:
        # Сохраняем приветственное сообщение в state
        welcome_msg = await message.answer(
            "🎤 Добро пожаловать в бот для тренировки речи!\n\n"
            "Этот бот поможет вам:\n"
            "• Улучшить дикцию\n"
            "• Развить уверенность в речи\n"
            "• Сделать речь более выразительной\n\n"
            "Для начала нужно пройти регистрацию:\n"
            "Введите ваше имя и фамилию через пробел"
        )

        # Сохраняем ID приветственного сообщения в state
        await state.update_data(welcome_message_id=welcome_msg.message_id)
        await state.set_state(RegistrationStates.waiting_for_name)


@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    # Удаляем сообщение пользователя с именем
    await message.delete()

    # Получаем ID приветственного сообщения из state
    data = await state.get_data()
    welcome_message_id = data.get('welcome_message_id')

    # Удаляем приветственное сообщение бота
    if welcome_message_id:
        try:
            await message.bot.delete_message(
                chat_id=message.from_user.id,
                message_id=welcome_message_id
            )
        except:
            pass

    parts = message.text.strip().split()
    if len(parts) >= 2:
        first_name, last_name = parts[0], ' '.join(parts[1:])

        await state.update_data(first_name=first_name, last_name=last_name)

        # Отправляем новое сообщение с настройкой уведомлений
        notification_msg = await message.answer(
            f"✅ Отлично, {first_name} {last_name}!\n\n"
            f"Теперь настроим уведомления.\n"
            f"По умолчанию напоминания будут приходить в:\n"
            f"• 09:00 утра\n• 13:00 дня\n• 19:00 вечера\n\n"
            f"Хотите изменить время? Отправьте новое время в формате ЧЧ:ММ, "
            f"например '10:30' (можно несколько через запятую).",
            reply_markup=get_notification_skip_keyboard()
        )

        # Сохраняем ID сообщения о настройке уведомлений
        await state.update_data(notification_msg_id=notification_msg.message_id)
        await state.set_state(RegistrationStates.waiting_for_notifications)
    else:
        # Отправляем новое сообщение с ошибкой
        await message.answer(
            "Пожалуйста, введите имя и фамилию через пробел:"
        )


@router.message(RegistrationStates.waiting_for_notifications)
async def process_notifications(message: Message, state: FSMContext):
    # Удаляем сообщение пользователя с временем
    await message.delete()

    # Получаем данные из state
    data = await state.get_data()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    notification_msg_id = data.get('notification_msg_id')

    # Удаляем сообщение с инструкцией о настройке уведомлений
    if notification_msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.from_user.id,
                message_id=notification_msg_id
            )
        except:
            pass

    user = User(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=first_name,
        last_name=last_name,
        registered_at=datetime.now().isoformat(),
        last_active=datetime.now().isoformat()
    )

    if message.text:
        times = [t.strip() for t in message.text.split(',')]
        valid_times = []

        for time_str in times:
            if validate_time_format(time_str):
                valid_times.append(time_str)

        if valid_times:
            user.notification_times = valid_times
            db.save_user(user)
            # Отправляем новое сообщение с подтверждением
            await message.answer(
                f"✅ Настройки сохранены!\n"
                f"Уведомления будут приходить в: {', '.join(valid_times)}\n\n"
                "Теперь вы готовы начать тренировку речи! 🎤",
                reply_markup=get_main_menu()
            )
        else:
            # Отправляем новое сообщение с ошибкой
            await message.answer(
                "❌ Неверный формат времени. Используйте формат ЧЧ:ММ, например '10:30'.\n"
                "Попробуйте еще раз или нажмите 'Пропустить настройку' на клавиатуре выше."
            )
            return
    else:
        db.save_user(user)
        # Отправляем новое сообщение с подтверждением
        await message.answer(
            "✅ Регистрация завершена!\n"
            "Уведомления настроены по умолчанию.\n"
            "Вы можете изменить их в настройках позже.\n\n"
            "Теперь вы готовы начать тренировку речи! 🎤",
            reply_markup=get_main_menu()
        )

    await state.clear()


@router.callback_query(F.data == "skip_notifications")
async def skip_notifications(callback: CallbackQuery, state: FSMContext):
    # Удаляем сообщение с кнопками
    await callback.message.delete()

    # Получаем данные из state
    user_data = await state.get_data()
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')

    user = User(
        user_id=callback.from_user.id,
        username=callback.from_user.username or "",
        first_name=first_name,
        last_name=last_name,
        registered_at=datetime.now().isoformat(),
        last_active=datetime.now().isoformat()
    )

    db.save_user(user)

    # Отправляем новое сообщение
    await callback.message.answer(
        "✅ Регистрация завершена!\n"
        "Уведомления настроены по умолчанию.\n"
        "Вы можете изменить их в настройках позже.\n\n"
        "Теперь вы готовы начать тренировку речи! 🎤",
        reply_markup=get_main_menu()
    )

    await state.clear()
    await callback.answer()