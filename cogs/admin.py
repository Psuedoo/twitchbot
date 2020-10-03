import traceback
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

    @commands.command(name="title")
    @commands.check(checks.is_mod)
    async def title(self, ctx):
        if check_args("title", ctx.message.clean_content):
            args = get_args("title", ctx.message.clean_content)
        else:
            await ctx.send("Please supply a new title.")

# TODO: Add info command creation support

# !addcommand "stupac62" "KEYBOARDS"
# !stupac62 -> KEYBOARDS
