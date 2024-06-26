import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from data.config import bot
from entity.database import subscriptions
from service.GetMessage import get_mes, get_text
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "tariff")
async def remains(message: CallbackQuery):
    id = message.from_user.id
    text = get_text(get_mes("subscriptions", subscriptions=await subscriptions.get_all_sorted()))
    reply_markup = await Keyboards.payment_kb()

    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=text,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.MARKDOWN_V2)


subscriptions_rt = router
