import asyncio
import logging
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime

from data.config import offset
from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    id_subscription = Column(Integer, default=None)
    end_subscription = Column(DateTime, default=None)
    thread_id = Column(String, default=None)
    created_at = Column(DateTime)

    def dict(self):
        return {"id": self.id,
                "username": self.username,
                "id_subscription": self.id_subscription,
                "end_subscription": self.end_subscription,
                "thread_id": self.thread_id,
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

    def __in__(self, id: int):
        result = asyncio.run(self.in_(id))
        return result

    async def __aexit__(self, exc_type, exc, tb):
        print ("Выход из асинхронного контекста")

    async def in_(self, id: int) -> User | bool:
        result = await self.get(id)
        if type(result) is User:
            return result
        return False
