from db.models import *
from db import db_handler


async def get_sounds(name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_sounds, name)


def local_get_sounds(session, name):
    channel = session.query(Twitch).filter(Twitch.name == name).one_or_none()
    if channel.guild_id:
        sounds = session.query(SoundsAssociation).filter(SoundsAssociation.guild_id == channel.guild_id)
        return [sound.name for sound in sounds]
    else:
        return
