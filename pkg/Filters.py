import logging

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User, CallbackQuery

from data.config import FORMAT_FILES, BASE_PATH_PDF, bot, allowed_file_len
from entity.database import users
from handlers.users.exceptions import now_allowed_len_file, not_valid_file_format
from handlers.users.payment import no_subscription
from service import Files

logger = logging.getLogger(__name__)


class ThereSubscription(Filter):
    async def __call__(self, message: Message | CallbackQuery, event_from_user: User, state: FSMContext) -> bool:
        user = await users.get(message.from_user.id)
        status = await users.check_subscription(user)
        match status:
            case "Subscription time is over":
                await state.clear()
                return await no_subscription(message, "Subscription time is over")
            case "The number of requests exceeded":
                await state.clear()
                return await no_subscription(message, "The number of requests exceeded")
            case "The free subscription has expired":
                await state.clear()
                return await no_subscription(message, "The free subscription has expired")
            case "Subscription ended":
                return False
            case "Free subscription":
                return True
            case "There is a subscription":
                return True
            case _:
                raise ValueError(f"Not type of subscription: {status}")


class AcceptableFileFormat(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        format_file = message.document.file_name.split('.')[-1]
        if format_file in FORMAT_FILES:
            return True
        return await not_valid_file_format(message)


class AllowedLenFile(Filter):
    async def __call__(self, message: Message, event_from_user: User) -> bool:
        path_file = f"{BASE_PATH_PDF}{event_from_user.id}_{message.document.file_name}"
        format_file = message.document.file_name.split('.')[-1]
        await bot.download(
            message.document,
            destination=path_file)
        logger.info("Downloaded file")
        if format_file == "doc":
            Files.convert_doc_to_docx(path_file)
            path_file = path_file.replace(".doc", ".docx")
        len_file = Files.len(path_file=path_file)
        logger.info(f"len {path_file}: {len_file}")
        if len_file <= allowed_file_len:
            return True
        return await now_allowed_len_file(message)