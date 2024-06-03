import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery

from data.config import bot, YKASSA_API_KEY
from entity.database import users, User, subscriptions
from service.GetMessage import get_mes
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.data == "pay_subscribe")
async def load_documents(message: Message | CallbackQuery):
    id = message.from_user.id
    prices = await subscriptions.get_labeled_price()
    # await bot.edit_message_text(chat_id=id,
    #                             message_id=message.message.message_id,
    #                             text=get_mes("pay_subscribe"),
    #                             reply_markup=await Keyboards.pay_subscribe())
    await message.delete()
    await bot.send_invoice(chat_id=id,
                           title="Покупка",
                           description="подписки",
                           provider_token=YKASSA_API_KEY,
                           currency="rub",
                           need_email=False,
                           need_phone_number=False,
                           need_shipping_address=False,
                           is_flexible=False,
                           prices=prices,
                           start_parameter="start_parameter",
                           payload="payload")


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    logging.info("Processing pre-checkout query")
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    logging.info(message.successful_payment)
    id = message.from_user.id
    user = users.get(id)


load_documents_rt = router
