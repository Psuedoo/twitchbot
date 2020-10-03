import subprocess
import wikipedia
import random
import requests
import json
import re
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


    # TODO : Fix this command, broken with ASMR and Abra
    @commands.command(name="wiki")
    async def wiki(self, ctx, *topic):
    
        if topic:
            # " ".join(topic)

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
    async def shot(self, ctx, name):
        if name:
            await ctx.send(f"Cheers, {name}!")
        else:
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
    async def addquote(self, ctx, user_author, user_quote):
        db = TinyDB(f'quotes_{ctx.channel.name}.json')

        print(f"{user_author=}")
        print(f"{user_quote=}")

        if user_author and user_quote:
            Quote = Query()
            contains = db.contains(Quote['quote'] == user_quote)

            if contains:
                await ctx.send("Quote already exists...")
            else:
                try:
                    db.insert({'author': user_author, 'quote': user_quote})
                except:
                    await ctx.send("Failed to add quote.")
                else:
                    await ctx.send("Quote added successfully!")
        else:
            await ctx.send("Please supply author and quote. Surround both with quotation marks!")

    
    def get_quote(self, ctx, user_author=None, user_quote=None):
        db = TinyDB(f'quotes_{ctx.channel.name}.json')
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
    async def deletequote(self, ctx):
        db = TinyDB(f'quotes_{ctx.channel.name}.json')
        Quote = Query()

        if self.check_args(ctx):
            args = self.get_args(ctx).strip()
            if args.isalnum():
                quote_id = int(args)
                if db.contains(doc_id=quote_id):
                    quote = db.get(doc_id=quote_id)
                    await ctx.send(f"Trying to delete quote: {quote}....")
                    try:
                        db.remove(doc_ids=[quote_id,])
                    except KeyError as e:
                        await ctx.send("Could not delete quote.. {e}")
                    else:
                        await ctx.send("Quote has been deleted!")
                else:
                    await ctx.send(f"There is no quote in the DB with the ID {quote_id}")
            else:
                await ctx.send("You have to supply quote ID. Try using !quote command to get quote ID.")
        else:
            await ctx.send("You have to supply quote ID. Try using !quote command to get quote ID.")


    @commands.command(name="testing")
    async def testing(self, ctx, author, quote):
        await ctx.send(f"{author=}")
        await ctx.send(f"{quote=}")

# TODO: Add info command creation support
