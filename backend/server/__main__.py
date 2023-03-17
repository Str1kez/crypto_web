from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from server.config import DefaultSettings
from server.db.cache import Cache
from server.endpoints import routes
from server.tools import euler_function, get_prime, get_private_key, get_public_key


def bind_routes(app: FastAPI):
    path_prefix = DefaultSettings().PATH_PREFIX
    for router in routes:
        app.include_router(router, prefix=path_prefix)


def add_cors(app: FastAPI):
    origins = [
        "*",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@asynccontextmanager
async def generate_rsa_keys(_: FastAPI):
    settings = DefaultSettings()
    p = get_prime(settings.KEY_BIT_LEN)
    q = get_prime(settings.KEY_BIT_LEN)
    while p == q:
        q = get_prime(settings.KEY_BIT_LEN)
    public_rsa_key = get_public_key(euler_function(p, q))
    private_rsa_key = get_private_key(euler_function(p, q), public_rsa_key)
    await Cache().set("n", p * q)
    await Cache().set("public_rsa", public_rsa_key)
    await Cache().set("private_rsa", private_rsa_key)
    yield


app = FastAPI(lifespan=generate_rsa_keys)
add_cors(app)
bind_routes(app)


if __name__ == "__main__":
    run("server.__main__:app", host="127.0.0.1", port=8001, reload=True, reload_dirs=["server"])
