from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.database.repository import create_subject
from bot.database.repository import get_or_create_user
from bot.services.ai_service import generate_study_plan

from bot.states.planner_states import PlannerStates


router = Router()


async def send_split_message(message: Message, text: str, max_length: int = 4000):
    if len(text) <= max_length:
        await message.answer(text)
        return

    while text:
        if len(text) <= max_length:
            await message.answer(text)
            break
        
        chunk_end = text.rfind('\n', 0, max_length)
        if chunk_end == -1:
            chunk_end = text.rfind(' ', 0, max_length)
        if chunk_end == -1:
            chunk_end = max_length

        chunk = text[:chunk_end]
        await message.answer(chunk)
        text = text[chunk_end:].lstrip()


@router.message(Command("plan"))
async def plan_handler(
        message: Message,
        state: FSMContext
):

    await state.set_state(
        PlannerStates.subject
    )

    await message.answer(
        "What subject do you want to study?"
    )


@router.message(PlannerStates.subject)
async def subject_handler(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        subject=message.text
    )

    await state.set_state(
        PlannerStates.exam_date
    )

    await message.answer(
        "When is your exam date?"
    )


@router.message(PlannerStates.exam_date)
async def exam_date_handler(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        exam_date=message.text
    )

    await state.set_state(
        PlannerStates.daily_hours
    )

    await message.answer(
        "How many hours can you study per day?"
    )


@router.message(PlannerStates.daily_hours)
async def hours_handler(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        daily_hours=message.text
    )


    data = await state.get_data()

    status_message = await message.answer("🤖 Generating your AI study plan, please wait...")


    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )


    subject = await create_subject(
        user_id=user.id,
        name=data["subject"],
        exam_date=data["exam_date"],
        daily_hours=int(data["daily_hours"])
    )

    plan = await generate_study_plan(
        subject=data["subject"],
        exam_date=data["exam_date"],
        daily_hours=int(data["daily_hours"])
    )


    await status_message.delete()

    full_response = f"📚 Your AI study plan:\n\n{plan}"

    await send_split_message(message=message, text=full_response)


    await state.clear()