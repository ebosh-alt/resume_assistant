import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import bot
from service.GetMessage import get_mes
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("help"))
@router.callback_query(F.data == "help")
async def helping(message: Message | CallbackQuery):
    id = message.from_user.id
    if type(message) is Message:
        await bot.send_message(chat_id=id,
                               text=get_mes("help"),
                               reply_markup=Keyboards.back_menu_kb)
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message.message.message_id,
                                    text=get_mes("help"),
                                    reply_markup=Keyboards.back_menu_kb)


help_rt = router
