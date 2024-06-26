import logging

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from data.config import contact_us
from entity.database import subscriptions, Subscription

logger = logging.getLogger(__name__)


class Builder:
    @staticmethod
    def create_keyboard(name_buttons: list | dict, *sizes: int) -> types.InlineKeyboardMarkup:
        keyboard = InlineKeyboardBuilder()
        if type(name_buttons) is list:
            for name_button in name_buttons:
                keyboard.button(
                    text=name_button, callback_data=name_button
                )
        elif type(name_buttons) is dict:
            for name_button in name_buttons:
                if "http" in name_buttons[name_button] or "@" in name_buttons[name_button]:
                    keyboard.button(
                        text=name_button, url=name_buttons[name_button]
                    )
                else:
                    keyboard.button(
                        text=name_button, callback_data=name_buttons[name_button]
                    )

        if len(sizes) == 0:
            sizes = (1,)
        keyboard.adjust(*sizes)
        return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)

    @staticmethod
    def create_reply_keyboard(name_buttons: list, one_time_keyboard: bool = False, request_contact: bool = False,
                              *sizes) -> types.ReplyKeyboardMarkup:
        keyboard = ReplyKeyboardBuilder()
        for name_button in name_buttons:
            if name_button is not tuple:
                keyboard.button(
                    text=name_button,
                    request_contact=request_contact
                )
            else:
                keyboard.button(
                    text=name_button,
                    request_contact=request_contact

                )
        if len(sizes) == 0:
            sizes = (1,)
        keyboard.adjust(*sizes)
        return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)


class Keyboards:
    menu_kb = Builder.create_keyboard({
        "Загрузить документы": "load_documents",
        "Мой остаток": "remains",
        "Тарифы": "tariff",
        "Связь с нами": contact_us,
        "Возможности бота": "help",
        "Q&A": "Q&A",
    })
    load_documents_kb = Builder.create_keyboard({"Загрузить документы": "load_documents"})
    go_payment_kb = Builder.create_keyboard({"Купить подписку": "pay_subscribe"})
    back_menu_kb = Builder.create_keyboard({"Меню": "menu"})
    menu_admin = Builder.create_keyboard({
        "Тарифы": "admin_subscriptions"
    })

    back_to_subscriptions_kb = Builder.create_keyboard({
        "Назад": "admin_subscriptions"
    })
    subscriptions_kb = Builder.create_keyboard({
        "Просмотреть текущие": "watch_subscriptions",
        "Создать тариф": "create_subscriptions",
        "Удалить тариф": "delete_subscriptions",
        "Назад": "menu_admin",
    })

    @staticmethod
    async def payment_kb():
        all_subscriptions: list[Subscription] = await subscriptions.get_all_sorted()
        buttons = {}
        for subscription in all_subscriptions:
            buttons[f"Купить за {subscription.amount}р"] = f"subscriptions_{subscription.id}"
        buttons["Меню"] = "menu"
        return Builder.create_keyboard(buttons)
