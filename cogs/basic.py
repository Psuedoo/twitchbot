import subprocess
import wikipedia
import random
from twitchio.ext import commands
from twitchio import dataclasses
from cogs.utils import checks
from tinydb import TinyDB, Query


@commands.cog()
class Basic():
    def __init__(self, bot):
        self.bot = bot


    def check_args(self, prefix, message):
            message = message.lstrip(prefix)
            if message:
                return True
            else:
                return False


    def get_args(self, prefix, message):
        check = self.check_args(prefix, message)
        if check:
            return message.lstrip(f"{prefix} ")
        else:
            return None

    @commands.command(name="randomnumber")
    async def randnumber(self, ctx):
        await ctx.send(f"Your random number is {random.randint(1, 1000)}.")


    @commands.command(name="roll")
    async def roll(self, ctx):
        await ctx.send(f"You rolled a {random.randint(1, 6)}.")


    @commands.command(name="tp")
    async def tp(self, ctx):
        if self.check_args("tp" , ctx.message.clean_content):
            args = self.get_args("tp", ctx.message.clean_content)
            await ctx.send(args)
        else:
            await ctx.send("You didn't have any arguments.")


    @commands.command(name="randchoice", aliases=["rc",])
    async def randchoice(self, ctx):
        if self.check_args("randchoice", ctx.message.clean_content):
            args = self.get_args("randchoice", ctx.message.clean_content)
            choice = random.choice(args.split(" "))
            await ctx.send(f"/me has chosen {choice}")
        else:
            await ctx.send("I don't understand or you didn't specify any options.")


    @commands.command(name="coolest")
    async def coolest(self, ctx):
        await ctx.send(f"The coolest has to be {random.choice(ctx.channel.chatters).name}")


    # TODO : Fix this command, broken with ASMR and Abra
    @commands.command(name="wiki")
    async def wiki(self, ctx):
        if self.check_args("wiki", ctx.message.clean_content):
           
            args = ctx.message.clean_content.lstrip("wiki")
            try: 
                full_summary = wikipedia.summary(args)[0:450]
            except wikipedia.exceptions.DisambiguationError as a:
                await ctx.send(f"Be more specific, {ctx.author.name}.")    
            
            
            summary = full_summary[0:full_summary.rindex(".") + 1]
            await ctx.send(f"Wiki Says: {summary}")
        else:
            await ctx.send("I don't understand or you didn't supply arguments.")

   
    @commands.command(name="randwiki", aliases=["rw",])
    async def randomwiki(self, ctx):
        full_summary = wikipedia.summary(wikipedia.random())
        full_summary = full_summary[0:450]
        summary = full_summary[0:full_summary.rindex(".") + 1]
        await ctx.send(f"{summary}")


    @commands.command(name="hello")
    async def hello_command(self, ctx):
        await ctx.send(f"Hello {ctx.author.name}!")


    @commands.command(name="songsuggest")
    async def songsuggest(self, ctx):
        db = TinyDB("songs.json")
        
        if self.check_args("songsuggest", ctx.message.clean_content):
            url = get_args("songsuggest", ctx.message.clean_content) 
            args = ['youtube-dl', '-x', url]
            Popen("", args)

        else:
            await ctx.send("You did something wrong, {ctx.author.name}.")

    @commands.command(name="shot")
    async def shot(self, ctx):
        await ctx.send(f"Cheers, {ctx.author.name}!")
