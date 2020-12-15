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


async def set_discord_link(name, link):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_set_discord_link, name, link)


def local_set_discord_link(session, name, link):
    row = session.query(Twitch).filter(Twitch.name == name).one_or_none()
    row.guild_invite_link = link
    session.commit()


async def get_discord_link(name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_discord_link, name)


def local_get_discord_link(session, name):
    row = session.query(Twitch).filter(Twitch.name == name).one_or_none()
    return row.guild_invite_link


async def set_discord_id(name, id):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_set_discord_id, name, id)


def local_set_discord_id(session, name, id):
    row = session.query(Twitch).filter(Twitch.name == name).one_or_none()
    row.guild_id = id
    session.commit()


async def get_discord_id(name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_discord_id, name)


def local_get_discord_id(session, name):
    row = session.query(Twitch).filter(Twitch.name == name).one_or_none()
    return row.guild_id


async def set_discord_invite_message(name, message):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_set_discord_invite_message, name, message)


def local_set_discord_invite_message(session, name, message):
    row = session.query(Twitch).filter(Twitch.name == name).one_or_none()
    row.guild_invite_message = message
    session.commit()


async def get_discord_invite_message(name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_discord_invite_message, name)


def local_get_discord_invite_message(session, name):
    row = session.query(Twitch).filter(Twitch.name == name).one_or_none()
    return row.guild_invite_message


# TODO: Do this
def local_get_prefix(session, channel_name):
    pass