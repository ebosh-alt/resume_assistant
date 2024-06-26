import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import bot
from entity.database import subscriptions
from pkg.states import AdminStates
from service.keyboards import Keyboards

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "delete_subscriptions")
async def delete_subscriptions(message: CallbackQuery, state: FSMContext):
    id = message.from_user.id
    await bot.edit_message_text(chat_id=id,
                                message_id=message.message.message_id,
                                text="Введите id подписки")
    await state.set_state(AdminStates.delete_subscriptions)
    await state.update_data(message_id=message.message.message_id)


@router.message(AdminStates.delete_subscriptions)
async def get_id_by_delete_subscriptions(message: Message, state: FSMContext):
    id = message.from_user.id
    await message.delete()
    id_subscriptions = int(message.text)
    data = await state.get_data()
    message_id = data.get("message_id")
    if subscription := await subscriptions.in_(id_subscriptions):
        await subscriptions.delete(subscription)
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text="Подиска удалена!\nВыберите действие",
                                    reply_markup=Keyboards.subscriptions_kb)
        await state.clear()
    else:
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text="Подиска не найдена!\nВыберите действие",
                                    reply_markup=Keyboards.subscriptions_kb)


delete_subscriptions_rt = router
