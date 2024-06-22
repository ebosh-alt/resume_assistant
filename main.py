import asyncio
import logging

from contextlib import suppress
from multiprocessing import Process

from data.config import dp, bot
from entity.database import subscriptions, Subscription
from entity.database.base import create_async_database
from handlers import routers
from service import middleware, Files

logger = logging.getLogger(__name__)


async def main() -> None:
    await create_async_database()
    for router in routers:
        dp.include_router(router)
    dp.update.middleware(middleware.Logging())
    if len(await subscriptions.get_all()) == 0:
        await subscriptions.new(Subscription(
            description="Подписка на 2 месяц, доступно 60 запросов в месяц",
            count_request=60,
            count_month=2,
            count_week=0,
            count_day=0,
            amount=200
        ))
    # bg_proc = Process(target=Files.delete_files)
    # bg_proc.start()
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
