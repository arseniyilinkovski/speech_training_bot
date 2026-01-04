from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    """Главное меню с профилем"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎤 Начать тренировку", callback_data="course_speech"),
            ],
            [
                InlineKeyboardButton(text="📊 Мой прогресс", callback_data="my_progress"),
                InlineKeyboardButton(text="👤 Профиль", callback_data="show_profile"),
            ],
            [
                InlineKeyboardButton(text="🔔 Настройки уведомлений", callback_data="notification_settings"),
                InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help"),
            ]
        ]
    )
    return keyboard

def get_profile_menu():
    """Меню профиля"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎤 Тренировка речи", callback_data="course_speech"),
                InlineKeyboardButton(text="📊 Статистика", callback_data="my_progress"),
            ],
            [
                InlineKeyboardButton(text="🔔 Уведомления", callback_data="notification_settings"),
                InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_menu"),
            ]
        ]
    )
    return keyboard

def get_training_menu():
    """Меню тренировок"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎤 Речевая тренировка", callback_data="start_training"),
            ],
            [
                InlineKeyboardButton(text="📚 Мои курсы", callback_data="my_courses"),
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="show_profile"),
            ]
        ]
    )
    return keyboard

# Остальные функции остаются без изменений...
def get_courses_keyboard():
    """Выбор курсов"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🗣️ Тренировка речи", callback_data="course_speech"),
            ],
            [
                InlineKeyboardButton(text="➕ Добавить курс (скоро)", callback_data="add_course"),
            ]
        ]
    )
    return keyboard

def get_warmup_confirmation():
    """Подтверждение разминки"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Размялся", callback_data="warmup_done"),
                InlineKeyboardButton(text="⏭️ Пропустить разминку", callback_data="skip_warmup"),
            ]
        ]
    )
    return keyboard

def get_exercise_types():
    """Выбор типа упражнения"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎯 Случайное упражнение", callback_data="exercise_random"),
            ],
            [
                InlineKeyboardButton(text="🗣️ Скороговорка", callback_data="exercise_tongue_twister"),
            ],
            [
                InlineKeyboardButton(text="📖 Чтение вслух", callback_data="exercise_reading"),
            ],
            [
                InlineKeyboardButton(text="🎨 Описание предмета", callback_data="exercise_description"),
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="show_profile"),
            ]
        ]
    )
    return keyboard

def get_notification_skip_keyboard():
    """Клавиатура для пропуска настроек уведомлений"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⏭️ Пропустить настройку", callback_data="skip_notifications"),
            ]
        ]
    )
    return keyboard

def get_delete_message_keyboard(message_id: int):
    """Клавиатура для удаления сообщения"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑️ Удалить это сообщение",
                    callback_data=f"delete_{message_id}"
                )
            ]
        ]
    )
    return keyboard