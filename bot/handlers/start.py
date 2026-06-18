from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):

    username = message.from_user.username

    await message.answer(
        f"""
            Hello, {username}!

            I'm the AI ​​Research Planner Bot.

            I've helped you:
            - create a preparation plan;
            - manage your time;
            - write down a task.

            Commands:

            /plan — create a plan
            /help — help
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