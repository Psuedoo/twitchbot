import os
import random
import wikipedia
import pdb
import traceback
from twitchio.ext import commands
from cogs.utils import checks

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            irc_token=os.environ["TMI_TOKEN"],
            client_id=os.environ["CLIENT_ID"],
            nick=os.environ["BOT_NICK"],
            prefix=os.environ["BOT_PREFIX"],
            initial_channels=os.environ["CHANNEL"].split(";"),
        )

        
        initial_extensions = ["cogs.admin", "cogs.basic"]
        
        for extension in initial_extensions:
            try:
                self.load_module(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}.")
                traceback.print_exc()

    def check_args(self, prefix, message):
        message = message.lstrip(prefix)
        if message:
            return True
        else:
            return False

    def get_args(self, prefix, message):
        check = self.check_args(prefix, message)
        if check:
            return message.lstrip(f"{prefix} ")
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

        await ctx.send(f"Go check out https://www.twitch.tv/{streamer_name} . They are a great streamer!")


    @commands.command(name="discord")
    async def discord(self, ctx):
        if ctx.channel.name == "psuedoo":
            await ctx.send("Join the Discord to stay connected after stream! https://discord.gg/UcFgW6A")
        elif ctx.channel.name == "lettrebag":
            await ctx.send("Hey, did you know there is a Discord server that you can chat with all of your new friends? You can also see plenty of pet pictures! Join here: https://discord.gg/SpD5ZDt")
        

bot = Bot()
bot.run()
