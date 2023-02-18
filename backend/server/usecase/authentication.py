from sqlalchemy import Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import select

from server.db.connection.session import get_session
from server.db.models.user import User
from server.exceptions.user import InvalidCredentials, UserNotFound
from server.schemas.signin import SignInRequest
from server.tools.hash import get_hash


async def __get_db_credentials(credentials: SignInRequest) -> Row[tuple[str, int]]:
    try:
        async with get_session() as session:
            query = select(User.password, User.time_label).where(User.username == credentials.username)
            data = await session.execute(query)
            return data.one()
    except NoResultFound:
        raise UserNotFound


async def auth_by_code(credentials: SignInRequest):
    password_hash, timestamp = await __get_db_credentials(credentials)
    timestamp_hash = get_hash(str(timestamp))
    auth_hash = get_hash(password_hash + timestamp_hash)
    if credentials.password_hash != auth_hash:
        raise InvalidCredentials
