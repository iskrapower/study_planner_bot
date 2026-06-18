from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.planner_states import PlannerStates


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


    await message.answer(
        f"""
            Your study plan settings:

            Subject:
            {data['subject']}

            Exam date:
            {data['exam_date']}

            Daily hours:
            {data['daily_hours']}

            I will generate your plan soon.
        """
    )


    await state.clear()