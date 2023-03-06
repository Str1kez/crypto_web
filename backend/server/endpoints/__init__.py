from server.endpoints.auth import api as auth_router
from server.endpoints.data_encryption import api as encryption_router
from server.endpoints.key_exchange import api as key_router


routes = [
    auth_router,
    key_router,
    encryption_router,
]

__all__ = [
    "routes",
]
