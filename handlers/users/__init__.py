from .help import help_rt
from .load_documents import load_documents_rt
from .menu import menu_rt
from .payment import payment_rt
from .Q_A import q_a_rt
from .remains import remains_rt
from .subscriptions import subscriptions_rt

users_routers = (menu_rt, help_rt, load_documents_rt, payment_rt, q_a_rt, remains_rt, subscriptions_rt)
