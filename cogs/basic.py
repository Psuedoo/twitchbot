import wikipedia
import random
import requests
import re
from http import HTTPStatus
from twitchio.ext import commands
from cogs.utils import checks
from tinydb import TinyDB, Query
from db import db_handler_admin, db_handler_quotes


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

    @commands.command(name="addquote", aliases=["aq",])
    @commands.check(checks.is_mod)
    async def addquote(self, ctx, user_author, user_quote):
        db = TinyDB(f'quotes/quotes_{ctx.channel.name}.json')

        if user_author and user_quote:
            try:
                await db_handler_quotes.add_quote(ctx.channel.name, user_author, user_quote)
                await ctx.send("Quote added successfully!")
            except:
                await ctx.send("Failed to add quote.")
        else:
            await ctx.send("Please supply author and quote. Surround both with quotation marks!")

    
    def get_quote(self, ctx, user_author=None, user_quote=None):
        db = TinyDB(f'quotes/quotes_{ctx.channel.name}.json')
        Quote = Query()
     
        # Check if there are args
        if user_author or user_quote:
            
            
            # Check if author is specified
            if user_author:
                results = Quote.author.search(user_author, re.IGNORECASE) 
                # Checks if author is in db
                if db.contains(results): 
                    quotes = db.search(results)
                        
                    actual_author = (db.search(results)[0])['author']

                    # Checks if keyword is specified
                    if user_quote:
                        
                        # Finding quote...
                        for quote in quotes:
                            if re.search(user_quote, quote["quote"], flags=re.IGNORECASE):
                                actual_quote = quote
                        
                        # Author and quote was found successfully 
                        if actual_author and actual_quote:
                            return actual_quote 

                        # Author was found successfully but quote was not
                        elif actual_author and not actual_quote:
                            return f"Keyword did not return any quotes from {user_author}"
                       
                       # It would be hard to reach this. But neither return anything..
                        else:
                            return "You shouldn't be seeing this... but neither returned anything..."

                    # Author is specified and in the db, but keyword is not specified. Return random quote from author
                    elif user_author and not user_quote:
                        
                        return random.choice(quotes)


                # Author has been specified but isn't in the db; Maybe 'user_author' is actually 'user_quote'??
                else:
                    all_quotes = db.all()
                    possible_quotes = []
                
                    actual_author = None
                    actual_quote = None

                    # Finding quote...
                    for quote in all_quotes:
                        if re.search(user_author, quote["quote"], flags=re.IGNORECASE):
                            actual_quote = 1 
                            actual_author = 1 
                            possible_quotes.append(quote)
                    
                    if actual_author and actual_quote:
                        return random.choice(possible_quotes)
                    else:
                        return f"{user_author} is not in the db. Maybe it's not in proper case?"

                
                
            # Author not secified, but keyword is
            elif not user_author and user_quote:
                all_quotes = db.all()
                possible_quotes = []

                # Finding quote...
                for quote in all_quotes:
                    if re.search(user_quote, quote["quote"], flags=re.IGNORECASE):
                        actual_quote = quote["quote"]
                        actual_author = quote["author"]
                        possible_quotes.append(quote)
                      
                
                # If there are any results from the keyword
                if len(possible_quotes) > 0:
                    return random.choice(possible_quotes)

                # There weren't any results from the keyword
                else:
                    return f"No quotes were found containing, {user_quote}. Could be your casing."
                        
            # Maybe author and keyword isn't specified but still put ';' for some reason??
            else:
                return "To get a random quote, just run !quote or !q."
                

        # No args; Return random quote
        else:
            return random.choice(db.all()) 
            #await ctx.send(f"{quote['author']} said: ' {quote['quote']} '")

    # TODO: Finish this for DB migration.. UGH
    # !q ; quote
    @commands.command(name="quote", aliases=["q",])
    async def quote(self, ctx, user_author=None, user_quote=None):

        if user_author:
            user_author = user_author.lower()
        elif user_quote:
            user_quote = user_quote.lower()
        
        quote = self.get_quote(ctx, user_author, user_quote)

        if type(quote) is str:
            await ctx.send(quote)
        elif type(quote['author']) == str and type(quote['quote']) == str:
            await ctx.send(f"ID: {quote.doc_id}; {quote['author']} said: '{quote['quote']} '")
        else:
            await ctx.send(quote)
            await ctx.send("I dunno, you've reached the quote else...")

    @commands.check(checks.is_mod)
    @commands.command(name="deletequote", aliases=["dq",])
    async def deletequote(self, ctx, quote_id):

        if quote_id.isalnum():
            quote_id = int(quote_id)
            has_deleted = await db_handler_quotes.delete_quote(ctx.channel.name, quote_id)
            if has_deleted:
                await ctx.send('Deleted quote!')
            else:
                await ctx.send('Could not delete quote')


