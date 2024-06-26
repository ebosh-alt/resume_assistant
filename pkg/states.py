from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    communication = State()
    communication1 = State()
    communication2 = State()
    communication3 = State()
    communication4 = State()
    communication5 = State()


class AdminStates(StatesGroup):
    delete_subscriptions = State()
    description_subscriptions = State()
    count_request_subscriptions = State()
    count_month_subscriptions = State()
    count_week_subscriptions = State()
    count_day_subscriptions = State()
    amount_subscriptions = State()


class ManageStates(StatesGroup):
    ...
