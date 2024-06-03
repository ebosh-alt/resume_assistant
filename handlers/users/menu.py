import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import bot
from entity.database import users, User
from service.GetMessage import get_mes

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start(message: Message | CallbackQuery):
    id = message.from_user.id
    user = await users.get(id)
    if user is None:
        user = User(id=id, username=f"@{message.from_user.username}")
        await users.new(user)
    await bot.send_message(
        chat_id=id,
        text=get_mes("menu")
    )

menu_rt = router
