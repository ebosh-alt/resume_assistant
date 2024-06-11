import asyncio
import logging

from contextlib import suppress

from data.config import dp, bot
from entity.database import subscriptions, Subscription
from entity.database.base import create_async_database
from handlers import routers
from service import middleware

logger = logging.getLogger(__name__)


async def main() -> None:
    await create_async_database()
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    await subscriptions.new(Subscription(
        description="Подписка на 1 месяц, доступно 30 запросов в месяц",
        count_request=1,
        count_month=1,
        count_week=0,
        count_day=0,
        amount=100
    ))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # filename="log.logging",
        format=u'%(filename)s:%(lineno)d #%(levelname)-3s [%(asctime)s] - %(message)s',
        filemode="w",
        encoding='utf-8')

    with suppress(KeyboardInterrupt):
        asyncio.run(main())
