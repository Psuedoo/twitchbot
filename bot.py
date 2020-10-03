import os
import random
import wikipedia
import asyncio
import requests
from aiohttp import web
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
                print(e)


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

    @commands.command(name="followage")
    async def followage(self, ctx):
        response = requests.get(f"https://2g.be/twitch/following.php?user=$({ctx.author.name})&channel=$({ctx.channel.name})&format=mwdhms")
        await ctx.send(response.text)


if __name__ == '__main__':
    bot = Bot()
    bot.run()
