from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from server.db.connection.session import get_session
from server.db.models.user import User
from server.exceptions import UserExists
from server.schemas.signup import SignUpRequest
from server.tools.hash import password_hash


async def register_user(credentials: SignUpRequest):
    credentials.password = password_hash(credentials.password)
    try:
        async with get_session() as session:
            await session.execute(insert(User), [credentials.__dict__])
            await session.commit()
    except IntegrityError:
        raise UserExists
