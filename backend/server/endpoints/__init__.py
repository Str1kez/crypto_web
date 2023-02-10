from server.endpoints.auth import api as auth_router


routes = [
    auth_router,
]

__all__ = [
    "routes",
]
