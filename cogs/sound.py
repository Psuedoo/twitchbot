import os
import asyncio
from twitchio.ext import commands
from cogs.utils import checks
from tinydb import TinyDB, Query
from config import Config

@commands.cog()
class Sound():
    def __init__(self, bot):
        self.bot = bot

    async def tcp_echo_client(self, message):
        reader, writer = await asyncio.open_connection('localhost', 3000)

        print(f"Send: {message!r}")
        writer.write(message.encode())

        data = await reader.read(100)
        print(f"Received: {data.decode()!r}")

        writer.close()
        print('Closed')

    async def event_raw_data(self, data):
        user_name = None
        bit_amount = None
        channel_name = None
        channel = None
        message = None
        is_subscriber = False
        tags = data.split(";")

        for tag in tags:
            if tag.startswith("user-type=") and "PRIVMSG" in tag:
                channel_name = tag[tag.find('#')+1:]
                channel_name = channel_name[:channel_name.find(":")-1]
                message = tag[tag.rfind(":")+1:]

            if tag.startswith("display-name="):
                user_name = tag[tag.find("=")+1:]

            if tag.startswith("bits="):
                bit_amount = tag[tag.find("=")+1:]

            if tag.startswith("subscriber="):
                if tag[tag.find("=")+1:] == "1":
                    is_subscriber = True
    
        try:
            if channel_name:
                config = Config(channel_name) 
                db = TinyDB(config.sounds)
        except:
            pass

        try:
            channel = self.bot.get_channel(channel_name)
        except:
            # Channel doesn't exist
            pass
       
        if channel:
            if bit_amount:
                if int(bit_amount) == 1:
                    await channel.send(f"Thank you {user_name}, for the bit!")
                elif int(bit_amount) > 1:
                    await channel.send(f"Thank you {user_name}, for {bit_amount} bits!")
                    cheer_sound = [sound.get('command_name') for sound in db if sound.get('command_name') == 'cheer'][0]
                await self.tcp_echo_client(f'sound_name={cheer_sound};'
                        f'channel_name={channel_name};'
                        f'discord_id={config.discord_id}')
            elif is_subscriber and not message.startswith("!") or not channel_name:
                try:
                    sub_sound = [sound.get('command_name') for sound in db if sound.get('command_name') == 'sub'][0]
                    await self.tcp_echo_client(f'sound_name={sub_sound};'
                        f'channel_name={channel_name};'
                        f'discord_id={config.discord_id}')
    
                except:
                    pass

    @commands.command(name="play")
    async def play(self, ctx, *sound):
        config = Config(ctx.channel.name)
        full_sound = " ".join(sound)
        await self.tcp_echo_client(f"sound_name={full_sound};"
                f"channel_name={ctx.channel.name};"
                f"discord_id={config.discord_id}")

    @commands.command(name="viewsounds")
    async def view_sounds(self, ctx):
        config = Config(ctx.channel.name)
        self.db = TinyDB(config.sounds)
        sounds = [sound.get('command_name') for sound in self.db]
        await ctx.send(sounds)
