import os
import requests
import logging
from dotenv import load_dotenv
from twitchio.ext import commands

# For when cogs are implemented
initial_extensions = [
    "cogs.basic",
    "cogs.mod",
#     "cogs.admin",
#     "cogs.sound",
]

# Use for local building with .env file rather than Docker env vars
if os.path.exists("./.env"):
    load_dotenv()

# Basic logging for now, will change to db
logging.basicConfig(
    level=logging.INFO,
    filename='chat.log',
    filemode='a',
    # format='%(name)s - %(levelname)s - %(message)s'
    )

class Bot(commands.Bot):
    def __init__(self):
        self.channels = ["psuedoo"]
        self.prefix = os.getenv("BOT_PREFIX", None)
        super().__init__(
            token=os.getenv("TOKEN", None),
            nick=os.getenv("BOT_NICK", None),
            prefix=self.prefix,  # TODO: Figure out how to change prefix from channel to channel
            initial_channels=self.channels,
        )

        # Loading the exenstions
        for extension in initial_extensions:
            try:
                self.load_module(extension)
            except Exception as e:
                print(f"Failed to load extension {extension}.", e)


    async def event_ready(self):
        print(f"Ready | {self.nick}")

    async def event_message(self, message):
        log = (
            f'time={message.timestamp},'
            f'channel={message.channel.name},'
            f'author={message.author.name},'
            f'message={message.content}'
        )
            
        logging.info(log)

        await self.handle_commands(message)

    @commands.command(name="test")
    async def test(self, ctx):
        response = f'Hello {ctx.author.name}!'
        logging.info(f'Psuedoobot={response}')
        await ctx.send(response)


if __name__ == '__main__':
    bot = Bot()
    bot.run()
