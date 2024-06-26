from .users import users_routers
from .admins import admins_routers
routers = (*users_routers, *admins_routers)


