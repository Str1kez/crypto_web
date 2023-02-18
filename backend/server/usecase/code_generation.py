from datetime import datetime as dt

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.sql import update

from server.db.connection.session import get_session
from server.db.models.user import User
from server.exceptions.user import UserNotFound


async def get_code(username: str):
    """
    update "user"
    set time_label = extract(epoch from now())::integer
    where username = 'hasbulla'
    returning time_label;
    """
    try:
        async with get_session() as session:
            time_label = int(dt.now().timestamp())
            query = (
                update(User).where(User.username == username).values(time_label=time_label).returning(User.time_label)
            )
            db_time_label = await session.execute(query)
            await session.commit()
            return db_time_label.one()[0]
    except (IntegrityError, NoResultFound):
        raise UserNotFound
