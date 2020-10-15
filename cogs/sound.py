import os 
import asyncio
from twitchio.ext import commands
from cogs.utils import checks
from tinydb import TinyDB, Query

@commands.cog()
class Sound():
    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB(os.path.expanduser('~/coding/sounds/sounds.json'))


    async def tcp_echo_client(self, message):
        reader, writer = await asyncio.open_connection('localhost', 3000)

        print(f"Send: {message!r}")
        writer.write(message.encode())

        data = await reader.read(100)
        print(f"Recieved: {data.decode()!r}")

        writer.close()

    async def event_raw_data(self, data):
        tags = data.split(";")
        user_name = None
        bit_amount = None
        channel_name = None
        for tag in tags:
            if tag.startswith("user-type="):
                channel_name = tag[tag.find("#")+1:tag.rfind(":")-1]
            if tag.startswith("display-name="):
                user_name = tag[tag.find("=")+1:]
            if tag.startswith("bits="):
                bit_amount = tag[tag.find("=")+1:]
        try: 
            channel = self.bot.get_channel(channel_name)
        except:
            pass
        else:
            if bit_amount:
                if int(bit_amount) == 1:
                    await channel.send(f"Thank you {user_name}, for the bit!")
                elif int(bit_amount) > 1:
                    await channel.send(f"Thank you {user_name}, for {bit_amount} bits!")
                await self.tcp_echo_client("cheer")


    @commands.command(name="play")
    async def play(self, ctx, *sound):
        full_sound = " ".join(sound)
        await self.tcp_echo_client(full_sound)

    @commands.command(name="viewsounds")
    async def view_sounds(self, ctx):
        sounds = [sound.get('command_name') for sound in self.db]
        await ctx.send(sounds)
            

