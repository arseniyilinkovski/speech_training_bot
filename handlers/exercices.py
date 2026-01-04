from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Voice
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random
from exercices.description import DescriptionExercise
from exercices.reading import ReadingExercise
from exercices.tongue_twister import TongueTwisterExercise
from keyboards.inline import get_warmup_confirmation, get_exercise_types, get_main_menu, get_delete_message_keyboard
from database.json_db import JSONDatabase
from config import USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH
from utils.message_manager import message_manager

router = Router()
db = JSONDatabase(USERS_JSON_PATH, EXERCISES_JSON_PATH, TEXTS_JSON_PATH)


class ExerciseStates(StatesGroup):
    waiting_for_warmup = State()
    waiting_for_exercise = State()
    waiting_for_voice = State()


@router.callback_query(F.data == "start_training")
async def start_training(callback: CallbackQuery, state: FSMContext):
    await message_manager.add_callback_message(callback.from_user.id, callback)

    user = db.load_user(callback.from_user.id)

    if not user:
        await callback.answer("Пожалуйста, сначала пройдите регистрацию", show_alert=True)
        return

    if user.completed_today:
        await callback.message.edit_text(
            f"✅ Сегодня вы уже выполнили упражнение!\n\n"
            f"Ваша серия: {user.streak_days} дней 🔥\n"
            f"Вы можете потренироваться еще для получения опыта.",
            reply_markup=get_exercise_types()
        )
        await state.set_state(ExerciseStates.waiting_for_exercise)
    else:
        await callback.message.edit_text(
            "💪 *Разминка перед тренировкой*\n\n"
            "1. Языком посчитайте все зубы по кругу\n"
            "2. Продавите языком щеки изнутри\n"
            "3. Сделайте круговые движения языком\n\n"
            "Повторите 3 раза и нажмите '✅ Размялся'",
            reply_markup=get_warmup_confirmation()
        )
        await state.set_state(ExerciseStates.waiting_for_warmup)


@router.callback_query(F.data == "warmup_done")
async def warmup_done(callback: CallbackQuery, state: FSMContext):
    await message_manager.add_callback_message(callback.from_user.id, callback)

    await callback.message.edit_text(
        "🎯 Выберите тип упражнения:",
        reply_markup=get_exercise_types()
    )
    await state.set_state(ExerciseStates.waiting_for_exercise)




@router.callback_query(F.data.startswith("exercise_"))
async def select_exercise(callback: CallbackQuery, state: FSMContext):
    await message_manager.add_callback_message(callback.from_user.id, callback)

    exercise_type = callback.data.replace("exercise_", "")

    if exercise_type == "random":
        exercise_type = random.choice(["tongue_twister", "reading", "description"])

    if exercise_type == "tongue_twister":
        exercise = TongueTwisterExercise()
    elif exercise_type == "reading":
        exercise = ReadingExercise()
    elif exercise_type == "description":
        exercise = DescriptionExercise()
    else:
        return

    result = await exercise.execute()

    # Создаем клавиатуру с кнопкой "Назад в тренировку"
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Назад к выбору упражнений", callback_data="start_training"),
            ]
        ]
    )

    await callback.message.edit_text(
        result["text"],
        parse_mode="Markdown",
        reply_markup=back_keyboard  # Заменяем на новую клавиатуру
    )

    await state.update_data(
        current_exercise=exercise,
        exercise_data=result["data"]
    )
    await state.set_state(ExerciseStates.waiting_for_voice)


@router.message(F.voice)
async def process_voice(message: Message, state: FSMContext):
    await message_manager.add_message(message.from_user.id, message)

    data = await state.get_data()
    exercise = data.get("current_exercise")

    if not exercise:
        await message.answer("Пожалуйста, сначала выберите упражнение")
        return

    if await exercise.validate(message.voice):
        user = db.load_user(message.from_user.id)

        streak_updated = user.check_streak_update()

        experience_gained = exercise.experience
        user.total_experience += experience_gained
        user.course_experience["speech"] += experience_gained

        db.save_user(user)

        if streak_updated:
            response = (
                f"✅ Отлично! Упражнение выполнено!\n\n"
                f"🎁 +{experience_gained} XP\n"
                f"🔥 Серия: {user.streak_days} дней\n"
                f"💰 Всего опыта: {user.total_experience} XP\n\n"
                f"Так держать! Вы продлеваете свою серию!"
            )
        else:
            response = (
                f"✅ Хорошая работа!\n\n"
                f"🎁 +{experience_gained} XP\n"
                f"🔥 Серия продолжается: {user.streak_days} дней\n"
                f"💰 Всего опыта: {user.total_experience} XP"
            )

        response_msg = await message.answer(
            response,
            reply_markup=get_main_menu()
        )
        await message_manager.add_message(message.from_user.id, response_msg)
        await state.clear()
    else:
        error_msg = await message.answer(
            "❌ Голосовое сообщение слишком короткое/длинное. "
            "Пожалуйста, попробуйте еще раз, следуя инструкциям.",
            reply_markup=get_delete_message_keyboard(message.message_id)
        )
        await message_manager.add_message(message.from_user.id, error_msg)