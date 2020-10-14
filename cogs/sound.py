import asyncio
from twitchio.ext import commands
from cogs.utils import checks


@commands.cog()
class Sound():
    def __init__(self, bot):
        self.bot = bot

    async def tcp_echo_client(self, message):
        reader, writer = await asyncio.open_connection('localhost', 3000)

        print(f"Send: {message!r}")
        writer.write(message.encode())

        data = await reader.read(100)
        print(f"Recieved: {data.decode()!r}")

        writer.close()

    @commands.command(name="play")
    async def play(self, ctx, *sound):
        full_sound = " ".join(sound)
        await self.tcp_echo_client(full_sound)

