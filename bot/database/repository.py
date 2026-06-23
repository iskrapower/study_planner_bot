from sqlalchemy import select

from bot.database.database import async_session
from bot.database.models import User
from bot.database.models import Subject


async def get_or_create_user(
    telegram_id: int,
    username: str | None
):

    async with async_session() as session:

        result = await session.execute(
            select(User)
            .where(User.telegram_id == telegram_id)
        )

        user = result.scalar_one_or_none()


        if user is None:

            user = User(
                telegram_id=telegram_id,
                username=username
            )

            session.add(user)

            await session.commit()

            await session.refresh(user)


        return user
    

async def create_subject(
    user_id: int,
    name: str,
    exam_date: str,
    daily_hours: int
):

    async with async_session() as session:

        subject = Subject(
            user_id=user_id,
            name=name,
            exam_date=exam_date,
            daily_hours=daily_hours
        )

        session.add(subject)

        await session.commit()

        await session.refresh(subject)

        return subject