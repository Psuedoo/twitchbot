import os
import random
import wikipedia
import pdb
import traceback
import socketio
import asyncio
from twitchio.ext import commands
from cogs.utils import checks

initial_extensions = [
        "cogs.admin",
        "cogs.basic",
        ]


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            irc_token=os.environ["TMI_TOKEN"],
            client_id=os.environ["CLIENT_ID"],
            nick=os.environ["BOT_NICK"],
            prefix=os.environ["BOT_PREFIX"],
            initial_channels=os.environ["CHANNEL"].split(";"),
        )

        
        for extension in initial_extensions:
            try:
                self.load_module(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}.")
                traceback.print_exc()

    def clean_message(self, ctx):
        command_name = None
        message = ctx.message.clean_content
        
        if ctx.command.aliases:
            for alias in ctx.command.aliases:
                if message.startswith(alias):
                    print(alias)
                    command_name = alias
                    break
        if message.startswith(ctx.command.name):
            command_name = ctx.command.name

        message = message.replace(command_name, '')
        return message



    def check_args(self, ctx):
            message = self.clean_message(ctx)
            if message:
                return True
            else:
                return False


    def get_args(self, ctx):
        check = self.check_args(ctx)
        if check:
            args = self.clean_message(ctx)
            return args
        else:
            return None



    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f"Ready | {self.nick}")


    async def event_message(self, message):
        print(f"{message._channel}'s channel:\n{message._author.name}:\t{message.content}\t{message.timestamp}")
        await self.handle_commands(message)


    # Commands use a decorator...
    @commands.command(name="test")
    async def my_command(self, ctx):
        await ctx.send(f"Hello {ctx.author.name}!")


    @commands.command(name="shoutout", aliases=["so",])
    @commands.check(checks.is_mod)
    async def shoutout(self, ctx):
        *_, streamer_name = ctx.message.content.rsplit(" ")
        
        streamer_name = streamer_name.lstrip("@")

        await ctx.send(f"Go check out https://www.twitch.tv/{streamer_name} They are an awesome person!")


    @commands.command(name="send")
    async def send(self, ctx):
        # sio.emit('my event', {'data': 'message'})
        await ctx.send("Sent.")

    async def run_bot(bot):
        await bot.run()


if __name__ == '__main__':
    bot = Bot()
    
    bot.run()

