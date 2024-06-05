from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    communication = State()


class AdminStates(StatesGroup):
    ...


class ManageStates(StatesGroup):
    ...
