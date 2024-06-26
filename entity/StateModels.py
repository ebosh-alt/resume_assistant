from pydantic import BaseModel


class SubscriptionState(BaseModel):
    description: str = None
    count_request: int = None
    count_month: int = None
    count_week: int = None
    count_day: int = None
    amount: float = None
    message_id: int = None
