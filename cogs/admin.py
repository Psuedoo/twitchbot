import traceback
from config import Config
from tinydb import TinyDB, Query
from twitchio.ext import commands
from cogs.utils import checks
from twitchio import webhook

@commands.cog()
class Admin():
    def __init__(self, bot):
        self.bot = bot
        self.breakdown = None

    @commands.command(name="unload")
    @commands.check(checks.is_mod)
    async def unload(self, ctx, *, module):
        try:
            module = f"cogs.{module}"
            self.bot.unload_module(module)
        except AttributeError as e:
            if "breakdown" in e:
                pass
            else:
                print(e)
        except Exception as e:
            pass
            # await ctx.send(f"Could not unload '{module}'. Check console for details.")
            # print(traceback.format_exc())
        else:
            await ctx.send(f"'{module}' unloaded.")

    @commands.command(name="load")
    @commands.check(checks.is_mod)
    async def load(self, ctx, *, module):
        try:
            module = f"cogs.{module}"
            self.bot.load_module(module)
            print(traceback.format_exc())
        except Exception as e:
            await ctx.send(f"Could not load '{module}'. Check console for details.")
        else:
            await ctx.send(f"'{module}' loaded.")


    @commands.command(name="reload")
    @commands.check(checks.is_psuedo)
    async def _reload(self, ctx, *, module):
        try:
            module = f"cogs.{module}"
            self.bot.unload_module(module)
            self.bot.load_module(module)
        except Exception as e:
            await ctx.send(f"Could not reload '{module}'. Check console for details.")
            print(traceback.format_exc()) 
        else:
            await ctx.send(f"'{module}' reloaded.")

    @commands.command(name="setshoutoutmessage")
    @commands.check(checks.is_mod)
    async def set_shoutout_message(self, ctx, *message):
        shoutout_message = " ".join(message)
        config = Config(ctx.channel.name)
        config.shoutout_message = shoutout_message
        config.update_config()
        await ctx.send("Successfully updated shoutout message!")

    @commands.command(name="setdiscordid")
    @commands.check(checks.is_mod)
    async def set_discord_id(self, ctx, discord_id):
        config = Config(ctx.channel.name)
        config.discord_id = discord_id
        config.update_config()
        await ctx.send("Successfully updated discord id!")

    @commands.command(name="setdiscordlink")
    @commands.check(checks.is_mod)
    async def set_discord_link(self, ctx, link):
        config = Config(ctx.channel.name)
        config.discord_invite_link = link
        config.update_config()
        await ctx.send("Successfully updated discord invite link!")

    @commands.command(name="setdiscordmessage")
    @commands.check(checks.is_mod)
    async def set_discord_message(self, ctx, *message):
        discord_message = " ".join(message)
        config = Config(ctx.channel.name)
        config.discord_message = discord_message
        config.update_config()
        await ctx.send("Successfully updated discord message!")


# TODO: Add info command creation support

# !addcommand "stupac62" "KEYBOARDS"
# !stupac62 -> KEYBOARDS
