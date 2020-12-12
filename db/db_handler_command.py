from db.models import *
from db import db_handler


async def command_exists(channel_name, command_name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_command_exists, channel_name, command_name)


def local_command_exists(session, channel_name, command_name):
    row = session.query(TwitchCommands) \
        .filter(TwitchCommands.channel_name == channel_name, TwitchCommands.name == command_name).one_or_none()
    if row:
        return True
    return False


async def delete_command(channel_name, command_name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_delete_command, channel_name, command_name)


def local_delete_command(session, channel_name, command_name):
    if local_command_exists(session, channel_name, command_name):
        row = session.query(TwitchCommands) \
            .filter(TwitchCommands.channel_name == channel_name, TwitchCommands.name == command_name)

        session.delete(row)
        session.commit()


async def get_commands(channel_name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_commands, channel_name)


def local_get_commands(session, channel_name):
    row = session.query(TwitchCommands).filter(TwitchCommands.channel_name == channel_name)
    if row:
        command_names = [command.name for command in row]
        return command_names


async def get_command(channel_name, command_name):
    async with await db_handler.connection() as c:
        return await c.run_sync(local_get_command, channel_name, command_name)


def local_get_command(session, channel_name, command_name):
    row = session.query(TwitchCommands)\
        .filter(TwitchCommands.channel_name == channel_name, TwitchCommands.name == command_name).one_or_none()
    return row