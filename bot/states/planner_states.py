from aiogram.fsm.state import State, StatesGroup


class PlannerStates(StatesGroup):

    subject = State()
    exam_date = State()
    daily_hours = State()