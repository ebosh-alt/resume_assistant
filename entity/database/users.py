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
    id_subscription = Column(Integer)
    start_subscription = Column(DateTime)
    thread_id = Column(BigInteger)
    created_at = Column(DateTime)

    def dict(self):
        return {"id": self.id,
                "username": self.username,
                "id_subscription": self.id_subscription,
                "start_subscription": self.start_subscription,
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

    async def in_(self, id: int) -> User | bool:
        result = await self.get(id)
        if type(result) is User:
            return result
        return False
