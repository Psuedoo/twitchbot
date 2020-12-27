import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from db.models import *


async def connection():
    engine = create_async_engine('postgresql://psuedo@192.168.0.179/discordbot_dev', echo=False)
    session = AsyncSession(bind=engine)
    return session


async def insert(data=[]):
    async with await connection() as c:
        c.add_all(data)
        await c.commit()


async def initialize_channels(channels=[]):
    async with await connection() as c:
        for channel in channels:
            if not await c.run_sync(local_channel_exists, channel):
                print(f'Adding {channel} to database')
                default_shoutout_message = 'Go checkout this awesome person! '
                data = [
                    Twitch(name=channel,
                           shoutout_message=default_shoutout_message,
                           guild_invite_link=None,
                           guild_invite_message=None,
                           guild_id=None)
                ]
                await insert(data)
            else:
                print(f'{channel} already exists in the database')


def local_channel_exists(session, channel_name):
    channels = session.query(Twitch).filter(Twitch.name == channel_name)
    if len(channels.all()) > 0:
        return True


