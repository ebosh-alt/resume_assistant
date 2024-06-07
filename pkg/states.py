from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    communication = State()
    communication1 = State()
    communication2 = State()
    communication3 = State()
    communication4 = State()
    communication5 = State()


class AdminStates(StatesGroup):
    ...


class ManageStates(StatesGroup):
    ...
