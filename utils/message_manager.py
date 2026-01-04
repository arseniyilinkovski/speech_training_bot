from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from typing import List, Optional
import asyncio


class MessageManager:
    def __init__(self):
        self.user_messages = {}  # user_id: [message_ids]

    async def add_message(self, user_id: int, message: Message):
        """Добавить сообщение для отслеживания"""
        if user_id not in self.user_messages:
            self.user_messages[user_id] = []
        self.user_messages[user_id].append(message.message_id)

    async def add_callback_message(self, user_id: int, callback: CallbackQuery):
        """Добавить сообщение из callback"""
        if user_id not in self.user_messages:
            self.user_messages[user_id] = []
        self.user_messages[user_id].append(callback.message.message_id)

    async def cleanup_user(self, user_id: int, keep_last: int = 1, bot=None):
        """Очистить старые сообщения пользователя"""
        if user_id in self.user_messages and bot:
            messages = self.user_messages[user_id]
            # Оставляем только последние keep_last сообщений
            if len(messages) > keep_last:
                to_delete = messages[:-keep_last]
                for msg_id in to_delete:
                    try:
                        await bot.delete_message(chat_id=user_id, message_id=msg_id)
                    except:
                        pass
                # Обновляем список
                self.user_messages[user_id] = messages[-keep_last:]

    async def delete_all_user_messages(self, user_id: int, bot=None):
        """Удалить все сообщения пользователя"""
        if user_id in self.user_messages and bot:
            for msg_id in self.user_messages[user_id]:
                try:
                    await bot.delete_message(chat_id=user_id, message_id=msg_id)
                except:
                    pass
            self.user_messages[user_id] = []


message_manager = MessageManager()


async def delete_message_by_name(name: str, state: FSMContext, message:Message):
    data = await state.get_data()
    msg_id = data.get(name)

    if msg_id:
        try:
            await message.bot.delete_message(
                chat_id=message.from_user.id,
                message_id=msg_id
            )
        except:
            pass
