from aiogram.types import Message

from data.config import bot, allowed_file_len, FORMAT_FILES
from service.GetMessage import get_mes


async def now_allowed_len_file(message: Message):
    id = message.from_user.id
    await bot.send_message(chat_id=id,
                           text=get_mes("file_too_large", len_file=allowed_file_len))


async def not_valid_file_format(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=get_mes("not_valid_file_format", format_files=", ".join(FORMAT_FILES)))
