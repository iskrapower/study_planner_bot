from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database.repository import create_subject
from database.repository import get_or_create_user

from bot.states.planner_states import PlannerStates


router = Router()


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


    await message.answer(
        f"""
            Study plan saved!

            Subject:
            {subject.name}

            Exam date:
            {subject.exam_date}

            Daily hours:
            {subject.daily_hours}

            Next step: I will generate your AI study plan.
        """
    )


    await state.clear()