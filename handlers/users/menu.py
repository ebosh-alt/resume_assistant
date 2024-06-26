import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import bot
from entity.database import users, User
from service.GetMessage import get_mes
from service.OpenAI import ChatGPT
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
@router.callback_query(F.data == "menu")
async def start(message: Message | CallbackQuery):
    id = message.from_user.id
    user = await users.get(id)
    if user is None:
        vector_store = ChatGPT.create_vector_store(id)
        thread = ChatGPT.create_thread()
        user = User(id=id,
                    username=f"@{message.from_user.username}",
                    vector_store_id=vector_store.id,
                    thread_id=thread.id)
        await users.new(user)
    if type(message) is Message:
        await bot.send_message(
            chat_id=id,
            text=get_mes("menu"),
            reply_markup=Keyboards.menu_kb,
        )
    else:
        await bot.edit_message_text(
            chat_id=id,
            message_id=message.message.message_id,
            text=get_mes("menu"),
            reply_markup=Keyboards.menu_kb,
        )


menu_rt = router
