from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_profile_reply_keyboard():
    """Reply-клавиатура с кнопкой профиля"""
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="📊 Мой профиль"))

    return builder.as_markup(resize_keyboard=True)


def get_remove_keyboard():
    """Убрать клавиатуру"""
    return ReplyKeyboardMarkup(remove_keyboard=True)