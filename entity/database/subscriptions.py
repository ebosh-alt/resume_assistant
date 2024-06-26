import datetime
import logging

from aiogram.types import LabeledPrice
from sqlalchemy import Column, String, Integer, DateTime

from data.config import offset
from .base import Base, BaseDB
from ..StateModels import SubscriptionState

logger = logging.getLogger(__name__)


class Subscription(Base):
    """
    Attributes:
        id integer
        description string
        count_request integer
        count_month integer
        count_week integer
        count_day integer
        amount float
        created_at datetime
    """
    __tablename__ = "subscriptions"

    id = Column(Integer, autoincrement="auto", primary_key=True)
    description = Column(String(255), nullable=False)
    count_request = Column(Integer, nullable=False)
    count_month = Column(Integer, nullable=False)
    count_week = Column(Integer, nullable=False)
    count_day = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def dict(self):
        return {"id": self.id,
                "description": self.description,
                "count_request": self.count_request,
                "count_month": self.count_month,
                "count_week": self.count_week,
                "count_day": self.count_day,
                "amount": self.amount,
                "created_at": self.created_at
                }


class Subscriptions(BaseDB):
    async def new(self, subscription: Subscription):
        subscription.created_at = datetime.datetime.now(datetime.timezone(offset))
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

    async def get_all(self):
        result = await self._get_objects(Subscription)
        return result

    async def get_all_sorted(self):
        filters = {"order_by": Subscription.amount}
        result = await self._get_objects(Subscription, filters)
        return result

    async def get_labeled_price(self) -> list[LabeledPrice]:
        all_subscriptions: list[Subscription] = await self._get_objects(Subscription)
        prices: list[LabeledPrice] = []
        for subscription in all_subscriptions:
            amount = subscription.amount * 100
            prices.append(LabeledPrice(label=subscription.description, amount=amount))
        return prices

    async def get_all_amount(self):
        result = await self._get_attributes(Subscription, "amount")
        return result

    async def create_subscription(self, subscription_state: SubscriptionState):
        subscription = Subscription(description=subscription_state.description,
                                    count_request=subscription_state.count_request,
                                    count_month=subscription_state.count_month,
                                    count_week=subscription_state.count_week,
                                    count_day=subscription_state.count_day,
                                    amount=subscription_state.amount)
        await self.new(subscription)
        return subscription
