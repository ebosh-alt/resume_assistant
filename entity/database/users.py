import datetime
import logging

from sqlalchemy import Column, String, BigInteger, Integer, DateTime

from data.config import offset, count_free_request
from .subscriptions import Subscriptions
from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    id_subscription = Column(Integer, default=None)
    end_subscription = Column(DateTime, default=None)
    thread_id = Column(String, default=None)
    count_request = Column(Integer, default=0)
    created_at = Column(DateTime)

    def dict(self):
        return {"id": self.id,
                "username": self.username,
                "id_subscription": self.id_subscription,
                "end_subscription": self.end_subscription,
                "thread_id": self.thread_id,
                "count_request": self.count_request,
                "created_at": self.created_at
                }


class Users(BaseDB):
    async def new(self, user: User):
        user.created_at = datetime.datetime.now(datetime.timezone(offset))
        await self._add_obj(user)

    async def get(self, id: int) -> User | None:
        result = await self._get_object(User, id)
        return result

    async def update(self, user: User) -> None:
        await self._update_obj(instance=user, obj=User)

    async def delete(self, user: User) -> None:
        await self._delete_obj(instance=user)

    async def in_(self, id: int) -> User | bool:
        result = await self.get(id)
        if type(result) is User:
            return result
        return False

    async def check_subscription(self, user: User):
        current_date = datetime.datetime.now(datetime.timezone(offset))

        if user.end_subscription is None and user.count_request == count_free_request:
            user.end_subscription = datetime.datetime.now(datetime.timezone(offset))
            await self.update(user)
            return "The free subscription has expired"
        if user.end_subscription is None:
            return "Free subscription"
        elif user.end_subscription.timestamp() < current_date.timestamp():
            return "Subscription time is over"
        elif user.id_subscription is not None:
            subscription = await Subscriptions().get(user.id_subscription)
            if user.count_request == subscription.count_request:
                return "The number of requests exceeded"
        return "There is a subscription"
