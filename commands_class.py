from twitchio.ext import commands
from db import db_handler_command, db_handler
from db.models import TwitchCommands


@commands.cog()
class Command():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='commandadd')
    def add_command(self, ctx, name, response):
        if not await db_handler_command.command_exists(ctx.channel.name, name):
            data = [TwitchCommands(channel_name=ctx.channel.name,
                                   name=name,
                                   response=response)]

            await db_handler.insert(data)
            await ctx.send(f'{name} has been added!')
        else:
            await ctx.send(f'{name} already exists!')

    @commands.command(name='commanddelete')
    def delete_command(self, ctx, command_name):
        try:
            await db_handler_command.delete_command(ctx.channel.name, command_name)
            ctx.send(f'{command_name} has been successfully deleted!')
        except:
            await ctx.send(f'Could not delete {command_name}. Maybe it does not exist?')

    @commands.command(name='viewcommands')
    def get_commands(self, ctx):
        commands = await db_handler_command.get_commands(ctx.channel.name)
        if commands:
            await ctx.send(commands)
        else:
            await ctx.send('There are no commands.')

