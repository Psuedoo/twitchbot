from twitchio.ext import commands
from cogs.utils import checks

@commands.cog()
class Admin():
    def __init__(self, bot):
        self.bot = bot

    def _admin_unload(self):
        pass

    def _prepare(self, bot):
        pass

    def breakdown(self):
        pass


    @commands.command(name="unload")
    @commands.check(checks.is_psuedo)
    async def unload(self, ctx, module):
        try:
            self.bot.unload_module(module)
        except Exception as e:
            await ctx.send(f"Could not unload '{module}'. Check console for details.")
        else:
            await ctx.send("Not sure what's going on anymore...")

    @commands.command(name="load")
    @commands.check(checks.is_psuedo)
    async def load(self, ctx, module):
        try:
            self.bot.load_module(module)
        except Exception as e:
            await ctx.send(f"Could not load '{module}'. Check console for details.")
        else:
            await ctx.send(f"'{module}' loaded.")


    @commands.command(name="reload")
    @commands.check(checks.is_psuedo)
    async def _reload(self, ctx, *, module):
        try:
            self.bot.unload_module(module)
            self.bot.load_module(module)

        except Exception as e:
            await ctx.send(f"Could not reload '{module}'. Check console for details.")
        else:
            await ctx.send(f"'{module}' reloaded.")

    def prepare(bot):
        bot.add_cog(Admin(bot))

    def breakdown(bot):
        pass
