from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline import get_main_menu
from utils.message_manager import message_manager

router = Router()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer(
        "🏠 Главное меню",
        reply_markup=get_main_menu()
    )