import datetime

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User, Document

from data.config import offset, FORMAT_FILES, count_free_request
from entity.database import users
from handlers.users.payment import no_sbp


class IsAdmin(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        ...


class ThereSubscription(Filter):
    async def __call__(self, message: Message, event_from_user: User, state: FSMContext) -> bool:
        user = await users.get(message.from_user.id)
        current_date = datetime.datetime.now(datetime.timezone(offset))
        if user.end_subscription is None and user.count_request == count_free_request:
            await state.clear()
            user.end_subscription = datetime.datetime.now(datetime.timezone(offset))
            await users.update(user)
            await no_sbp(message)
            return False
        if user.end_subscription is None:
            return True
        elif user.end_subscription.timestamp() < current_date.timestamp():
            return False
        return True


class IsPdf(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        format_file = message.document.file_name.split('.')[-1]
        if format_file in FORMAT_FILES:
            return True
        return False
