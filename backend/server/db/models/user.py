from sqlalchemy import VARCHAR, Column
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.sql import func

from server.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "user"

    _id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        name="id",
    )
    username = Column(
        VARCHAR(30),
        nullable=False,
        unique=True,
        index=True,
    )
    password = Column(
        TEXT,
        nullable=False,
    )
