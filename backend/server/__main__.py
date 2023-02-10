from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from server.config import DefaultSettings
from server.endpoints import routes


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


app = FastAPI()
add_cors(app)
bind_routes(app)


if __name__ == "__main__":
    run("server.__main__:app", host="127.0.0.1", port=8001, reload=True, reload_dirs=["server"])
