import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import bot
from entity.database import users
from service.GetMessage import get_mes
from service.OpenAI import ChatGPT
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("help"))
@router.callback_query(F.data == "help")
async def helping(message: Message | CallbackQuery):
    id = message.from_user.id
    user = await users.get(id)
    if user.thread_id is None:
        response, thread_id = await ChatGPT.get_answer(user_id=id,
                                                       content="Расскажи что ты умеешь")
        user.thread_id = thread_id
    else:

        response, thread_id = await ChatGPT.get_answer(user_id=id,
                                                       thread_id=user.thread_id,
                                                       content="Расскажи что ты умеешь")
    await user.update(user)
    await bot.send_message(chat_id=id,
                           text=response,
                           reply_markup=Keyboards.load_documents_kb)


help_rt = router
