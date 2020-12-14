import os
import requests
from twitchio.ext import commands
from cogs.utils import checks
from db import db_handler, db_handler_admin, db_handler_command

initial_extensions = [
    "cogs.admin",
    "cogs.basic",
    "cogs.sound",
    "cogs.commands",
]


class Bot(commands.Bot):
    def __init__(self):
        self.channels = os.environ["CHANNEL"].split(";")
        super().__init__(
            irc_token=os.environ["TMI_TOKEN"],
            client_id=os.environ["CLIENT_ID"],
            nick=os.environ["BOT_NICK"],
            prefix=os.environ["BOT_PREFIX"],  # TODO: Figure out how to change prefix from channel to channel
            initial_channels=os.environ["CHANNEL"].split(";"),
        )

        for extension in initial_extensions:
            try:
                self.load_module(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}.", e)

    async def event_ready(self):
        print(f"Ready | {self.nick}")
        await db_handler.initialize_channels(self.channels)

    # TODO: Make this prettier for my eyes
    # TODO: Add prefix to the bot and get it instead of '?'
    async def event_message(self, message):
        prefix = self.prefixes[0]
        if message.content.startswith(prefix):
            command = message.content[1:]
            response = await db_handler_command.get_command(message.channel.name, command)
            if response:
                await message.channel.send(response)
            else:
                await self.handle_commands(message)

        inner_msg = f"{message.channel}'s channel"
        line_count = (30 - len(inner_msg)) // 2
        header = '-' * line_count + inner_msg + '-' * line_count
        footer = '-' * ((line_count * 2) + len(inner_msg))

        # Dedent removes leading whitespace

        print(f"""
            {header}
            Time:\t\t{message.timestamp}
            Author:\t\t{message.author.name}
            Message:\t{message.content}
            {footer}
        """)

    # Commands use a decorator...
    @commands.command(name="test")
    async def my_command(self, ctx):
        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command(name="shoutout", aliases=["so", ])
    @commands.check(checks.is_mod)
    async def shoutout(self, ctx):
        *_, streamer_name = ctx.message.content.rsplit(" ")
        streamer_name = streamer_name.lstrip("@")
        streamer_url = f"https://www.twitch.tv/{streamer_name}"
        await ctx.send(f"{await db_handler_admin.get_shoutout_message(ctx.channel.name)} {streamer_url}")

    @commands.command(name="followage")
    async def followage(self, ctx):
        response = requests.get(
            f"https://2g.be/twitch/following.php?user=$({ctx.author.name})&channel=$({ctx.channel.name})&format=mwdhms")
        await ctx.send(response.text)


if __name__ == '__main__':
    bot = Bot()
    bot.run()
