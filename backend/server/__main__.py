from fastapi import FastAPI
from uvicorn import run

from server.config import DefaultSettings
from server.endpoints import routes


def bind_routes(app: FastAPI):
    path_prefix = DefaultSettings().PATH_PREFIX
    for router in routes:
        app.include_router(router, prefix=path_prefix)


app = FastAPI()
bind_routes(app)


if __name__ == "__main__":
    run("server.__main__:app", host="127.0.0.1", port=8001, reload=True, reload_dirs=["server"])
