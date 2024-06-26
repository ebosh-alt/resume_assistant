import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from data.config import bot
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "admin_subscriptions")
async def start(message: Message | CallbackQuery):
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Выберите действие",
                                reply_markup=Keyboards.subscriptions_kb)


subscriptions_rt = router
