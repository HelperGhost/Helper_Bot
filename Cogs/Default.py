import discord
from discord.ext import commands

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
        self.bot: commands.bot = bot

    # This is the command to show the latency of the bot
    @commands.slash_command(name="ping", description="tells the latency of the bot.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000) # This rounds the latency and convert it into ms
        await ctx.respond(f"Pong! I got a ping of {latency}ms.")

    #This is for the information about the bot
    @commands.slash_command(name="botinfo", description="tells the bot's info.")
    async def botinfo(self, ctx):
        await ctx.respond(bot_info)

def setup(bot):
    bot.add_cog(Default(bot))