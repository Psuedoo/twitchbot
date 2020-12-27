import wikipedia
import random
import requests
from http import HTTPStatus
from twitchio.ext import commands
from cogs.utils import checks
from db import db_handler_admin


@commands.cog()
class Basic():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="randomnumber")
    async def randnumber(self, ctx):
        await ctx.send(f"Your random number is {random.randint(1, 1000)}.")

    @commands.command(name="roll")
    async def roll(self, ctx, sides: int=None):
        if sides:
            await ctx.send(f"You rolled a {random.randint(1, sides)}.")
        else:
            await ctx.send(f"You rolled a {random.randint(1, 6)}.")

    @commands.command(name="randchoice", aliases=["rc",])
    async def randchoice(self, ctx, *choices):
        if choices:
            await ctx.send(f"/me has chosen {random.choice(choices)}.")
        else:
            await ctx.send("I don't understand or you didn't specify any options.")


    @commands.command(name="coolest")
    async def coolest(self, ctx):
        await ctx.send(f"The coolest has to be {random.choice(ctx.channel.chatters).name}")

    @commands.command(name="wiki")
    async def wiki(self, ctx, *topic):
    
        if topic:
            try:
                full_summary = wikipedia.summary(topic)[0:450]
            except wikipedia.exceptions.DisambiguationError as e:
                await ctx.send(f"Be more specific, {ctx.author.name}.")
                print(e)

            summary = full_summary[0:full_summary.rindex(".") + 1]
            await ctx.send(f"Wiki Says: {summary}")

   
    @commands.command(name="randwiki", aliases=["rw",])
    async def randomwiki(self, ctx):
        full_summary = wikipedia.summary(wikipedia.random())
        full_summary = full_summary[0:450]
        summary = full_summary[0:full_summary.rindex(".") + 1]
        await ctx.send(f"{summary}")


    @commands.command(name="hello", aliases=["h",])
    async def hello_command(self, ctx, name):
        if name:
            await ctx.send(f"Hello, {name}!")
        else:
            await ctx.send(f"Hello, {ctx.author.name}!")


    @commands.command(name="shot")
    async def shot(self, ctx, name):
        if name:
            await ctx.send(f"Cheers, {name}!")
        else:
            await ctx.send(f"Cheers, {ctx.author.name}!")


    @commands.command(name="discord")
    async def discord(self, ctx):
        discord_invite_link = await db_handler_admin.get_discord_link(ctx.channel.name)
        if discord_invite_link:
            message = await db_handler_admin.get_discord_invite_message(ctx.channel.name)
            if not message:
                message = "Feel free to join the discord here:"
            await ctx.send(f"{message} {discord_invite_link}")
        else:
            await ctx.send("There is no discord linked to this channel. Set the discord invite link with !setdiscordlink")

    # Convert commands like this to channel commands in config
    @commands.check(checks.is_psuedoos_channel)
    @commands.command(name="github", aliases=["project", "git",])
    async def github(self, ctx):
        await ctx.send("Twitch bot: https://github.com/Psuedoo/twitchbot"
                       " Discord bot: https://github.com/Psuedoo/discordbot")



    @commands.command(name="docs", aliases=["whatshouldpsuedoobedoinginsteadofaskingchat",])
    async def docs(self, ctx):
        await ctx.send("Read the docs.")


    @commands.command(name="google")
    async def google(self, ctx, *query):

        if query:
            new_query = "+".join(query)
            await ctx.send(f"https://www.google.com/search?q={new_query}")
        else:
            await ctx.send("Please supply a query.")


    @commands.command(name="affirmation")
    async def affirmation(self, ctx):
        response = requests.get("https://www.affirmations.dev/")
        await ctx.send(f"{response.json()['affirmation']}.")


    @commands.command(name="cat")
    async def cat(self, ctx, status_code: str=None):
        if status_code:
            await ctx.send(f"https://http.cat/{status_code}")
        else:
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
        poses_dict = {"pose1": "https://i.imgur.com/OODPxwv.jpg",
                "pose2": "https://i.imgur.com/ByTd3iA.jpg",
                "pose3": "https://i.imgur.com/OH2B4L9.jpg",
                "pose4": "https://i.imgur.com/JDSohOV.jpg",
                "pose5": "https://i.imgur.com/ZUrSSUM.jpg",
                "pose6": "https://i.imgur.com/iKoXx6u.jpg",
                "pose7": "https://i.imgur.com/la9Tqar.jpg",
                "pose8": "https://i.imgur.com/lmYnk7s.jpg",
                "pose9": "https://i.imgur.com/DyCVUp5.jpg",
                "pose10": "https://i.imgur.com/QOQAPY0.jpg",}
        pose = random.choice(list(poses_dict.items()))
        await ctx.send(f"{pose[0]}: {pose[1]}")

    @commands.command(name="whothoughtofwebrtc", aliases=["wtowrtc",])
    async def webrtc(self, ctx):
        await ctx.send("Why ofcourse, it was @stupac62..")




