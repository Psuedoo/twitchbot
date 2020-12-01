import asyncio
from twitchio.ext import commands
from db import db_handler, db_handler_sound


@commands.cog()
class Sound():
    def __init__(self, bot):
        self.bot = bot

    async def tcp_echo_client(self, message):
        reader, writer = await asyncio.open_connection('localhost', 4000)

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
                channel_name = tag[tag.find('#') + 1:]
                channel_name = channel_name[:channel_name.find(":") - 1]
                message = tag[tag.rfind(":") + 1:]

            if tag.startswith("display-name="):
                user_name = tag[tag.find("=") + 1:]

            if tag.startswith("bits="):
                bit_amount = tag[tag.find("=") + 1:]

            if tag.startswith("subscriber="):
                if tag[tag.find("=") + 1:] == "1":
                    is_subscriber = True

        try:
            channel = self.bot.get_channel(channel_name)
        except:
            print('Channel doesnt exist')
            pass

        if channel:
            if bit_amount:
                if int(bit_amount) == 1:
                    await channel.send(f"Thank you {user_name}, for the bit!")
                elif int(bit_amount) > 1:
                    await channel.send(f"Thank you {user_name}, for {bit_amount} bits!")
                    if int(bit_amount) > 100:
                        cheer_sound = await db_handler_sound.get_sound('cheer')
                        if cheer_sound:
                            await self.tcp_echo_client(f'sound_name={cheer_sound.name};'
                                                       f'channel_name={channel_name};'
                                                       f'discord_id={cheer_sound.guild_id}')
            elif is_subscriber and not message.startswith("!") or not channel_name:
                try:
                    sub_sound = await db_handler_sound.get_sound('sub')
                    if sub_sound:
                        await self.tcp_echo_client(f'sound_name={sub_sound.name};'
                                                   f'channel_name={channel_name};'
                                                   f'discord_id={sub_sound.guild_id}')

                except:
                    pass

    @commands.command(name="play")
    async def play(self, ctx, sound):
        await self.tcp_echo_client(f"sound_name={sound};"
                                   f"channel_name={ctx.channel.name};"
                                   f"discord_id={await db_handler_sound.get_sound_guild_id(sound)}")

    @commands.command(name="viewsounds")
    async def view_sounds(self, ctx):
        sounds = await db_handler_sound.get_sounds(ctx.channel.name)
        if sounds and len(sounds) > 0:
            await ctx.send(sounds)
        else:
            await ctx.send('There are no sounds')
