import subprocess
import wikipedia
import random
import requests
import json
from http import HTTPStatus
from twitchio.ext import commands
from twitchio import dataclasses
from cogs.utils import checks
from tinydb import TinyDB, Query


@commands.cog()
class Basic():
    def __init__(self, bot):
        self.bot = bot

    def clean_message(self, ctx):
        command_name = None
        message = ctx.message.clean_content
        
        if ctx.command.aliases:
            for alias in ctx.command.aliases:
                if message.startswith(alias):
                    print(alias)
                    command_name = alias
                    break
        if message.startswith(ctx.command.name):
            command_name = ctx.command.name

        message = message.replace(command_name, '')
        return message



    def check_args(self, ctx):
            message = self.clean_message(ctx)
            if message:
                return True
            else:
                return False


    def get_args(self, ctx):
        check = self.check_args(ctx)
        if check:
            args = self.clean_message(ctx)
            return args
        else:
            return None

    @commands.command(name="randomnumber")
    async def randnumber(self, ctx):
        await ctx.send(f"Your random number is {random.randint(1, 1000)}.")


    @commands.command(name="roll")
    async def roll(self, ctx):
        if self.check_args(ctx):
            args = self.get_args(ctx)
            try:
                number = int(args)
                roll_number = random.randint(1, number)
                await ctx.send(f"You rolled a {roll_number}.")
            except TypeError:
                await ctx.send("Please supply a number.")
        else:
            await ctx.send(f"You rolled a {random.randint(1, 6)}.")


    # TODO: Fix bug when I do !rc eat sleep
    @commands.command(name="randchoice", aliases=["rc",])
    async def randchoice(self, ctx):
        if self.check_args(ctx):
            choice = random.choice(self.clean_message(ctx).split(" "))
            args = self.get_args(ctx)
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
        if self.check_args(ctx):
           
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


    @commands.command(name="hello", aliases=["h",])
    async def hello_command(self, ctx):
        await ctx.send(f"Hello {ctx.author.name}!")


    # TODO: Maybe just download songs to listen to later.. maybe add songs to a spotify playlist? 
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


    @commands.command(name="discord")
    async def discord(self, ctx):
        if ctx.channel.name == "psuedoo":
            await ctx.send("Join the Discord to stay connected after stream! https://discord.gg/UcFgW6A")
        elif ctx.channel.name == "lettrebag":
            await ctx.send("Hey, did you know there is a Discord server that you can chat with all of your new friends? You can also see plenty of pet pictures! Join here: https://discord.gg/SpD5ZDt")


    @commands.check(checks.is_psuedoos_channel)
    async def github(self, ctx):
        await ctx.send("The current project, probably: https://github.com/Psuedoo/twitchbot")


    @commands.command(name="docs", aliases=["whatshouldpsuedoobedoinginsteadofaskingchat",])
    async def docs(self, ctx):
        await ctx.send("Read the docs.")


    @commands.command(name="google")
    async def google(self, ctx):
        if self.check_args(ctx):
            
            args = self.clean_message(ctx)
            phrase = args.replace(" ", "+")
            
            if phrase.endswith("+"):
                phrase = phrase[:-1]
            if phrase.startswith("+"):
                phrase = phrase[1:]
            
            await ctx.send(f"https://www.google.com/search?q={phrase}")
        else:
            await ctx.send("Please supply a query to Google.")


    @commands.command(name="affirmation")
    async def affirmation(self, ctx):
        response = requests.get("https://www.affirmations.dev/")
        await ctx.send(f"{response.json()['affirmation']}.")


    @commands.command(name="cat")
    async def cat(self, ctx):
        statuses = list(HTTPStatus)
        status = random.choice(statuses)
        await ctx.send(f"https://http.cat/{status.value}")

    @commands.command(name="dog")
    async def dog(self, ctx):
        response = requests.get("https://api.thedogapi.com/v1/images/search")
        await ctx.send(f"{response.json()[0]['url']}")

    @commands.command(name="birb")
    async def birb(self, ctx):
        response = requests.get("https://some-random-api.ml/img/birb")
        await ctx.send(f"{response.json()['link']}")

    @commands.command(name="meme")
    async def meme(self, ctx):
        response = requests.get("https://some-random-api.ml/meme")
        await ctx.send(f"{response.json()['image']}")

    @commands.command(name="JoJo")
    @commands.check(checks.is_lettrebags_channel)
    async def jojo(self, ctx):
        poses_dict = {"pose1": "url",
                "pose2": "url",
                "pose3": "url"}
        pose = random.choice(list(poses_dict.items()))
        await ctx.send(f"{pose[0]}: {pose[1]}")

    @commands.command(name="whothoughtofwebrtc", aliases=["wtowrtc",])
    async def webrtc(self, ctx):
        await ctx.send("Why ofcourse, it was @stupac62..")

    @commands.command(name="addquote", aliases=["aq",])
    @commands.check(checks.is_mod)
    async def addquote(self, ctx):
        db = TinyDB(f'quotes_{ctx.channel.name}.json')
        if self.check_args(ctx):
            args = self.get_args(ctx)
            # Psuedoo "Just look at it"
            quote = args[args.find(';') + 2:]
            author = args[:args.find(';')].lstrip(" ")
            
            Quote = Query()
            # For some reason it isn't confirming that the quote already exists.. 
            contains = db.contains(Quote['quote'] == quote)

            if contains:
                await ctx.send("Quote already exists...")
            else:
                db.insert({'author': author, 'quote': quote})
                await ctx.send("Quote has been added successfully!")

        else:
            await ctx.send("Please supply some information, yo.")


    # TODO: Add view quote command; Add edit quote command
    # TODO: Add info command creation support
