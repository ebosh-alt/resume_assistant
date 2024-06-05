import datetime
import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice

from data.config import bot, YKASSA_API_KEY, offset
from entity.database import users, subscriptions, Subscription
from service.GetMessage import get_mes
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "load_documents")
async def no_sbp(msg: CallbackQuery):
    id = msg.from_user.id
    await msg.answer(text="У Вас нет действующей подписки", disable_notification=False)
    await bot.edit_message_text(chat_id=id,
                                message_id=msg.message.message_id,
                                text=get_mes("subscriptions", subscriptions=await subscriptions.get_all()),
                                reply_markup=await Keyboards.payment_kb())


@router.callback_query(F.data.contains("subscriptions_"))
async def choice_amount(msg: CallbackQuery):
    id = msg.from_user.id
    id_sbp = int(msg.data.replace("subscriptions_", ""))
    sbp: Subscription = await subscriptions.get(id_sbp)
    await msg.message.delete()
    prices = [LabeledPrice(label=sbp.description, amount=sbp.amount * 100)]
    await bot.send_message(chat_id=id,
                           text="Тестовая карты: 1111 1111 1111 1026\nТестовая дата: 12/22\nТестовый CVC 000")
    await bot.send_invoice(chat_id=id,
                           title="Оплата подписки",
                           description=sbp.description,
                           provider_token=YKASSA_API_KEY,
                           currency="rub",
                           need_email=False,
                           need_phone_number=False,
                           need_shipping_address=False,
                           is_flexible=False,
                           prices=prices,
                           start_parameter="start_parameter",
                           payload=f"{sbp.id}")


def transform_date(day, month, year):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    return f'{day} {months[int(month) - 1]} {year} года'


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    logging.info("Processing pre-checkout query")
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    logging.info(message.successful_payment)
    id = message.from_user.id
    id_sbp = int(message.successful_payment.invoice_payload)
    sbp = await subscriptions.get(id_sbp)
    user = await users.get(id)
    days = sbp.count_day + sbp.count_month * 30 + sbp.count_week * 7
    user.end_subscription = datetime.datetime.now(datetime.timezone(offset)) + datetime.timedelta(days=days)
    await users.update(user)
    date = user.end_subscription.date()
    await bot.send_message(chat_id=id,
                           text=get_mes("view_subscribe", date=transform_date(date.day, date.month, date.year)),
                           reply_markup=Keyboards.load_documents_kb)


payment_rt = router
