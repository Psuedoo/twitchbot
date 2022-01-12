import requests
from twitchio.ext import commands

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='discord')
    async def discord(self, ctx):
        await ctx.send('https://discord.gg/UcFgW6A')

    @commands.command(name='giveaway')
    async def giveaway(self, ctx):
        response = f'http://www.rafflecopter.com/rafl/display/512f00b00/?'
        await ctx.send(response)

    @commands.command(name="followage")
    async def followage(self, ctx):
        response = requests.get(
            f"https://2g.be/twitch/following.php?user=$({ctx.author.name})&channel=$({ctx.channel.name})&format=mwdhms")
        await ctx.send(response.text)

def prepare(bot):
    bot.add_cog(Basic(bot))