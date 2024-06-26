import datetime
import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.config import bot, count_free_request
from entity.database import users, subscriptions
from service.GetMessage import get_mes, transform_date
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "remains")
async def remains(message: CallbackQuery):
    id = message.from_user.id
    user = await users.get(id)
    if user.id_subscription:
        subscription = await subscriptions.get(user.id_subscription)
        count_request = subscription.count_request - user.count_request
        date = user.end_subscription.date()
        date_end = transform_date(date.day, date.month, date.year)
    else:
        count_request = count_free_request - user.count_request
        date = datetime.datetime.now()
        date_end = transform_date(date.day, date.month, date.year)

    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text=get_mes("remains", date_end=date_end, count_request=count_request),
                                reply_markup=Keyboards.back_menu_kb)


remains_rt = router
