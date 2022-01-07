from twitchio.ext import commands


class Mod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.is_mod


    @commands.command(name="shoutout", aliases=["so", ])
    async def shoutout(self, ctx):
        *_, streamer_name = ctx.message.content.rsplit(" ")
        streamer_name = streamer_name.lstrip("@")
        streamer_url = f"https://www.twitch.tv/{streamer_name}"
        await ctx.send(f"Go follow: {streamer_url}")

def prepare(bot):
    bot.add_cog(Mod(bot))