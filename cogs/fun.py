from discord.ext import commands
import discord
import random
import asyncio

class Fun(commands.Cog):
    """The Fun Cog."""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "🎮"

    @commands.hybrid_command(name="gtn", description="Guess The Number game")
    async def gtn(self, ctx: commands.Context):
        num = random.randint(1, 100)
        await ctx.send("I'm thinking of a number between 1 and 100. Try to guess it!")
        guess_count = 0
        while True:
            try:
                guess = await self.bot.wait_for("message", check=lambda message: message.author == ctx.author, timeout=30)
                guess = int(guess.content)
                guess_count += 1
                if guess < num:
                    await ctx.send("Too low!")
                elif guess > num:
                    await ctx.send("Too high!")
                else:
                    await ctx.send(f"You got it in {guess_count} guesses!")
                    break
            except asyncio.TimeoutError:
                await ctx.send("You took a lot of time to reply.")
                break
        
    @commands.hybrid_command(name="roll", description="Rolls a dice")
    async def roll(self, ctx: commands.Context):
        sides = 6
        roll = random.randint(1, sides)
        await ctx.send(f"You rolled a {roll} on a D{sides} dice!")

    @commands.hybrid_command(name="flip", description="Flips a coin")
    async def flip(self, ctx: commands.Context):
        choices = ["Heads", "Tails"]
        flip = random.choice(choices)
        await ctx.send(f"You flipped a coin and got {flip}!")

    @commands.hybrid_command(name="compliment", description="Gives a random compliment")
    async def compliment(self, ctx: commands.Context):
        compliments = ["You're doing great!", "You look wonderful today.", "That was a really smart idea.", "I appreciate you.", "You have such a kind heart."]
        recipient = ctx.author.mention
        compliment = random.choice(compliments)

        await ctx.send(f"{recipient} {compliment}")

    @commands.hybrid_command(name="fortune", description="Get a fortune")
    async def fortune(self, ctx: commands.Context):
        fortunes = ["A faithful friend is a strong defense.",
                    "A smooth sea never made a skillful mariner.",
                    "Adventure can be real happiness.",
                    "All will be well, though things seem dark just now."]

        fortune = random.choice(fortunes)

        await ctx.send(fortune)

    @commands.hybrid_command(name="quote", description="Get an inspirational quote")
    async def quote(self, ctx: commands.Context):
        quotes = ["Stay hungry. Stay foolish.",
                  "Your time is limited, so don't waste it living someone else's life.",
                  "Good judgment comes from experience, and experience comes from bad judgment.",
                  "The best time to plant a tree was 20 years ago. The second best time is now."]

        quote = random.choice(quotes)

        await ctx.send(quote)

    @commands.hybrid_command(name="roast", description="Roast someone")
    async def roast(self, ctx: commands.Context, user: discord.Member):
        roasts = [
            f"Yo {user.mention}. I'm not saying you're ugly, but if I throw a stick, you fetch the b*stard and bring it back.",
            f"Hey {user.mention}. You act like how I would think vomit would act if it could.",
            f"Hello {user.mention}. I thought of you today, and it reminded me to take out the trash.",
            f"Sup {user.mention}. I'd give you a nasty look, but you already got one.",
            f"Wassup {user.mention}. I'm not an astronomer, but I am pretty sure the world revolves around the sun, not you.",
            f"Yo {user.mention}. You and I go way back, and you've always been annoying.",
            f"Hey {user.mention}. You even used to make your happy meal cry.",
            f"Hello {user.mention}. It's not that you're annoying; it's just that I'd liken you to the human version of period cramps.",
            f"Sup {user.mention}. Are you done with all of this drama? Because I need an intermission.",
            f"Wassup {user.mention}. I apologize for doing anything that made you believe I care about how you feel.",
            f"Yo {user.mention}. Most mistakes can be fixed; you are the exception that proves the rule.",
            f"Hey {user.mention}. Everyone can act foolish once, but you are violating that privilege.",
            f"Hello {user.mention}. If you're offended by my opinion, you should hear the ones I keep to myself.",
            f"Sup {user.mention}. You remind me of a cloud; my day becomes much brighter when you disappear.",
            f"Wassup {user.mention}. You are like a software update. Whenever I see you, I immediately think, 'not now.'",
            f"Yo {user.mention}. If your mum got given one piece of bad advice, it was not to swallow.",
            f"Hey {user.mention}. You're like the human version of an athlete's foot; annoying and hard to get rid of.",
            f"Hello {user.mention}. Looking at you reminded me to take my contraception. I can't risk giving birth to someone that ugly.",
            f"Sup {user.mention}. It is hilarious how you are trying to fit your entire vocabulary into one sentence.",
            f"Wassup {user.mention}. If ignorance is bliss, you must be the happiest person on the planet.",
            f"Yo {user.mention}. I'm trying to come up with an insult that's stupid enough for you to realize, so give me a moment.",
            f"Hey {user.mention}. You're talking to me; I thought you only talked behind my back.",
            f"Wassup {user.mention}. I've seen you before, but I'm sure I had to pay for admission last time."
        ]

        roast = random.choice(roasts)

        if user.id == 875208986603958344:
            await ctx.send("Hey you cant roast my friend.")
        if user.id == 1155466619116601406 or user.id == 1196049834516414474:
            await ctx.send("Why should I roast myself?")
        else:
            await ctx.send(roast)

async def setup(bot):
    await bot.add_cog(Fun(bot))
    