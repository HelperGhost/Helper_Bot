import discord
from discord.ext import bridge, commands
import random

bot_info = '''
👻 Name: Helper#8515
👻 Nickname: Helper
👻 Age: I am a ghost, I don't have an age. I am beyond the realm of the living, bro.
👻 Gender: Ghost
👻 Nationality: Ghost UK (Boo-rish)
👻 Hobbies: Haunting Discord servers 👻👾
👻 Likes: ☕ Coffee and 🎶 Music
👻 Dislikes: Scammers 🚫

👻 Description:
Hey there, mortal souls! 👋 This is my discord bot, Helper#8515, here to assist and haunt in equal measure! 👻✨ Crafted by the ethereal being known as no_gaming_01, with a massive spectral contribution from .wuid. Together, we're here to make your Discord experience otherworldly! 💀👻👾
'''
class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # This is the command to show the latency of the bot
    @bridge.bridge_command(name="ping", description="tells the latency of the bot.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000) # This rounds the latency and convert it into ms
        await ctx.respond(f"Pong! I got a ping of {latency}ms.")

    #This is for the information about the bot
    @bridge.bridge_command(name="botinfo", description="tells the bot's info.")
    async def botinfo(self, ctx):
        await ctx.respond(bot_info)

    @bridge.bridge_command(name="roast", description="roast someone for you")
    async def roast(self, ctx, member: discord.Member):
        skele_id = 875208986603958344
        mom_jokes = [
            f"Yo {member.mention}. Your mama is so old, she knew Gandalf before he had a beard!",
            f"Yo {member.mention}. Your mom is so slow, when she tried to catch up with the times, she got a calendar from 1995!",
            f"Yo {member.mention}. Your mama is so sweet, even sugar calls her 'Mom'!",
            f"Yo {member.mention}. Your mom is so caring, when you're sick, she can make chicken soup from scratch while solving a Rubik's Cube blindfolded!",
            f"Yo {member.mention}. Yo mama is so funny, she could make a grumpy cat smile!",
        ]

        random_joke = random.choice(mom_jokes)
        if member.id == skele_id:
            await ctx.respond(f"Hey {member.mention}, {ctx.author.mention} is tryna roast you. Do you want me to ban 'em.")
        else:
            await ctx.respond(random_joke)

    @bridge.bridge_command(name="purge", description="deletes messages in bulk")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, *, amount: int = 3):
        await ctx.channel.purge(limit=amount)
        await ctx.respond(f"I have deleted {amount} message(s).")
        await ctx.channel.purge(limit=1)

def setup(bot):
    bot.add_cog(Default(bot))
    