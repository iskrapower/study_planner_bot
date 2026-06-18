from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)


class Base(DeclarativeBase):
    pass



class User(Base):

    __tablename__ = "users"


    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    telegram_id: Mapped[int]

    username: Mapped[str | None]


    subjects = relationship(
        "Subject",
        back_populates="user"
    )



class Subject(Base):

    __tablename__ = "subjects"


    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str]

    exam_date: Mapped[str]

    daily_hours: Mapped[int]


    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )


    user = relationship(
        "User",
        back_populates="subjects"
    )