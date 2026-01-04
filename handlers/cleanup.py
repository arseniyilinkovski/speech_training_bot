from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

from keyboards.reply import get_profile_reply_keyboard
from utils.message_manager import message_manager

router = Router()

@router.callback_query(F.data.startswith("delete_"))
async def delete_message(callback: CallbackQuery):
    try:
        message_id = int(callback.data.split("_")[1])
        await callback.message.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=message_id
        )
        await callback.answer("Сообщение удалено")
    except Exception as e:
        await callback.answer("Не удалось удалить сообщение")
        print(f"Ошибка удаления: {e}")

@router.message(Command("clear"))
async def clear_chat(message: Message):
    """Очистить все сообщения бота"""
    await message_manager.delete_all_user_messages(message.from_user.id, bot=message.bot)
    await message.answer("✅ Все сообщения очищены", reply_markup=get_profile_reply_keyboard())