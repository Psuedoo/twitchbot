from db.models import *
from db import db_handler


async def set_shoutout_message(name, message):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_set_shoutout_message, name, message)


def local_set_shoutout_message(session, name, message):
    row = session.query(Twitch).filter(Twitch.name == name).one_or_none()
    row.shoutout_message = message
    session.commit()


async def get_shoutout_message(name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_shoutout_message, name)


def local_get_shoutout_message(session, name):
    row = session.query(Twitch).filter(Twitch.name == name).one_or_none()
    return row.shoutout_message

# TODO: Do this
def local_get_prefix(session, channel_name):
    pass