from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database.repository import get_or_create_user


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):

    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username
    )

    await message.answer(
        f"""
            Welcome, {user.username}!

            I am your AI Study Planner.

            I can help you:
            - create study plans;
            - track tasks;
            - organize preparation.
        """
    )


@router.message(Command("help"))
async def help_handler(message: Message):

    await message.answer(
        """
            Available commands:

            /start — launch the bot
            /plan — create a training plan
            /help — list of commands
        """
    )