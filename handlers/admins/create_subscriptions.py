import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot
from entity.StateModels import SubscriptionState
from entity.database import subscriptions
from pkg.states import AdminStates
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "create_subscriptions")
async def start_create_subscriptions(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await state.set_state(AdminStates.description_subscriptions)
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Введите описание подписки")
    await state.update_data(subscription=SubscriptionState(message_id=message.message.message_id))


@router.message(AdminStates.description_subscriptions)
async def description_subscriptions(message: Message, state: FSMContext):
    id = message.from_user.id
    await message.delete()
    data = await state.get_data()
    subscription: SubscriptionState = data.get("subscription")
    subscription.description = message.text
    await bot.edit_message_text(chat_id=id,
                                message_id=subscription.message_id,
                                text="Введите количество запросов в подписке")
    await state.set_state(AdminStates.count_request_subscriptions)
    await state.update_data(subscription=subscription)


@router.message(AdminStates.count_request_subscriptions)
async def count_request_subscriptions(message: Message, state: FSMContext):
    id = message.from_user.id
    await message.delete()
    data = await state.get_data()
    subscription: SubscriptionState = data.get("subscription")
    subscription.count_request = int(message.text)
    await bot.edit_message_text(chat_id=id,
                                message_id=subscription.message_id,
                                text="Введите количество месяцев в подписке")
    await state.set_state(AdminStates.count_month_subscriptions)
    await state.update_data(subscription=subscription)


@router.message(AdminStates.count_month_subscriptions)
async def count_month_subscriptions(message: Message, state: FSMContext):
    id = message.from_user.id
    await message.delete()
    data = await state.get_data()
    subscription: SubscriptionState = data.get("subscription")
    subscription.count_month = int(message.text)
    await bot.edit_message_text(chat_id=id,
                                message_id=subscription.message_id,
                                text="Введите количество недель в подписке")
    await state.set_state(AdminStates.count_week_subscriptions)
    await state.update_data(subscription=subscription)


@router.message(AdminStates.count_week_subscriptions)
async def count_week_subscriptions(message: Message, state: FSMContext):
    id = message.from_user.id
    await message.delete()
    data = await state.get_data()
    subscription: SubscriptionState = data.get("subscription")
    subscription.count_week = int(message.text)
    await bot.edit_message_text(chat_id=id,
                                message_id=subscription.message_id,
                                text="Введите количество дней в подписке")
    await state.set_state(AdminStates.count_day_subscriptions)
    await state.update_data(subscription=subscription)


@router.message(AdminStates.count_day_subscriptions)
async def count_day_subscriptions(message: Message, state: FSMContext):
    id = message.from_user.id
    await message.delete()
    data = await state.get_data()
    subscription: SubscriptionState = data.get("subscription")
    subscription.count_day = int(message.text)
    await bot.edit_message_text(chat_id=id,
                                message_id=subscription.message_id,
                                text="Введите стоимость подписки")
    await state.set_state(AdminStates.amount_subscriptions)
    await state.update_data(subscription=subscription)


@router.message(AdminStates.amount_subscriptions)
async def count_day_subscriptions(message: Message, state: FSMContext):
    id = message.from_user.id
    await message.delete()
    data = await state.get_data()
    subscription: SubscriptionState = data.get("subscription")
    subscription.amount = float(message.text)
    subscription_db = await subscriptions.create_subscription(subscription)
    if subscription_db:
        await bot.edit_message_text(chat_id=id,
                                    message_id=subscription.message_id,
                                    text="Подписка создана\nВыберите действие",
                                    reply_markup=Keyboards.subscriptions_kb)
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=subscription.message_id,
                                    text="Подписка не создана\nВыберите действие",
                                    reply_markup=Keyboards.subscriptions_kb)
    await state.clear()


create_subscriptions_rt = router
