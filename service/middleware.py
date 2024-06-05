import logging
from aiogram.types import Message, CallbackQuery, Document
from typing import Any, Awaitable, Callable, Dict
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class Logging:
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> None:

        # if event.message.document:
        #     name = "@" + event.message.from_user.username if event.message.from_user.username \
        #         else event.message.from_user.first_name
        #     logging.info(f'{[name, event.message.from_user.id]} - document - {event.message.document}')
        if type(event.message) is Message:
            name = "@" + event.message.from_user.username if event.message.from_user.username \
                else event.message.from_user.first_name
            logging.info(f'{[name, event.message.from_user.id]} - message - {event.message.text}')

        else:
            try:
                name = "@" + event.callback_query.from_user.username if event.callback_query.from_user.username \
                    else event.callback_query.from_user.first_name
                logging.info(
                    f'{[name, event.callback_query.from_user.id]} - callback_query - {event.callback_query.data}')
            except Exception as e:
                logging.error(e)
        result = await handler(event, data)
        return result
