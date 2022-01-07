from twitchio.ext import commands
from cogs.utils import checks

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='discord')
    async def discord(self, ctx):
        await ctx.send('https://discord.gg/UcFgW6A')

    @commands.command(name='giveaway')
    async def giveaway(self, ctx):
        response = f'http://www.rafflecopter.com/rafl/display/512f00b00/?'
        logging.info(f'Psuedoobot={response}')
        await ctx.send(response)

    @commands.command(name="followage")
    async def followage(self, ctx):
        response = requests.get(
            f"https://2g.be/twitch/following.php?user=$({ctx.author.name})&channel=$({ctx.channel.name})&format=mwdhms")
        await ctx.send(response.text)

    # @commands.command(name="shoutout", aliases=["so", ])
    # @checks.is_mod
    # async def shoutout(self, ctx):
    #     *_, streamer_name = ctx.message.content.rsplit(" ")
    #     streamer_name = streamer_name.lstrip("@")
    #     streamer_url = f"https://www.twitch.tv/{streamer_name}"
    #     await ctx.send(f"Go follow: {streamer_url}")

def prepare(bot):
    bot.add_cog(Basic(bot))