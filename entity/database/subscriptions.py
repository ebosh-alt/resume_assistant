import logging
from sqlalchemy import Column, String, BigInteger, Integer, DateTime
from .base import Base, BaseDB

logger = logging.getLogger(__name__)


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(BigInteger, primary_key=True)
    description = Column(String(255), nullable=False)
    count_request = Column(Integer, nullable=False)
    count_month = Column(Integer, nullable=False)
    count_week = Column(Integer, nullable=False)
    count_day = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def dict(self):
        return {"id": self.id,
                "description": self.description,
                "count_request": self.count_request,
                "count_month": self.count_month,
                "count_week": self.count_week,
                "count_day": self.count_day,
                "created_at": self.created_at
                }


class Subscriptions(BaseDB):
    async def new(self, subscription: Subscription):
        await self._add_obj(subscription)

    async def get(self, id: int) -> Subscription | None:
        result = await self._get_object(Subscription, id)
        return result

    async def update(self, subscription: Subscription) -> None:
        await self._update_obj(instance=subscription, obj=Subscription)

    async def delete(self, subscription: Subscription) -> None:
        await self._delete_obj(instance=subscription)

    async def in_(self, id: int) -> Subscription | bool:
        result = await self.get(id)
        if type(result) is Subscription:
            return result
        return False
