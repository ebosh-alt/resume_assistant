import datetime

from aiogram.filters import Filter
from aiogram.types import Message, User, Document

from data.config import offset, FORMAT_FILES
from entity.database import users


class IsAdmin(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        ...


class ThereSubscription(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        user = await users.get(message.from_user.id)
        current_date = datetime.datetime.now(datetime.timezone(offset))
        if user.end_subscription is None:
            return False
        elif user.end_subscription.timestamp() < current_date.timestamp():
            return False
        return True


class IsPdf(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        format_file = message.document.file_name.split('.')[-1]
        if format_file in FORMAT_FILES:
            return True
        return False
