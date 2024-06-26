import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from data.config import bot
from service.GetMessage import get_mes
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "Q&A")
async def q_a(message: Message | CallbackQuery):
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("q_a"),
                                reply_markup=Keyboards.back_menu_kb)


q_a_rt = router
