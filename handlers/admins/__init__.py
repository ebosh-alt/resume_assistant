from .menu import admin_rt
from .subscriptions import subscriptions_rt
from .create_subscriptions import create_subscriptions_rt
from .delete_subscriptions import delete_subscriptions_rt
from .watch_subscriptions import watch_subscriptions_rt

admins_routers = (admin_rt, subscriptions_rt, create_subscriptions_rt, delete_subscriptions_rt, watch_subscriptions_rt)
