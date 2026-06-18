from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command("plan"))
async def plan_handler(message: Message):

    await message.answer(
        """
            Let's create a preparation plan.

            Write the subject.

            For example:

            Python
            Mathematics
            IELTS
        """
    )