import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import bot
from entity.database import users, User
from service.GetMessage import get_mes
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.data == "load_documents")
async def load_documents(message: Message | CallbackQuery):
    id = message.from_user.id
    user = await users.get(id)
    if user.id_subscription is None:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=get_mes("no_subscription"),
                                    reply_markup=Keyboards.go_payment_kb)

    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=get_mes("load_documents"))


load_documents_rt = router
