from discord.ext import commands
import discord

class Server(commands.Cog):
    """The description for Server goes here."""

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Server(bot))
