from db.models import *
from db import db_handler


async def get_sounds(name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_sounds, name)


def local_get_sounds(session, channel_name):
    sounds = session.query(SoundsAssociation).filter(SoundsAssociation.channel_name == channel_name)
    return [sound.command for sound in sounds]


async def get_sound_guild_id(sound_name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_sound_guild_id, sound_name)


def local_get_sound_guild_id(session, sound_name):
    sound = session.query(SoundsAssociation).filter(SoundsAssociation.command == sound_name).one_or_none()
    return sound.guild_id


async def get_sound(sound_name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_sound_guild_id, sound_name)


def local_get_sound(session, sound_name):
    sound = session.query(SoundsAssociation).filter(SoundsAssociation.command == sound_name).one_or_none()
    return sound
