from discord.ext import commands
import discord

guild_id = 1193857532813381653

class Utility(commands.Cog):
    """The Utility Cog ig."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Tells the ping of the bot.")
    async def ping(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! I got a ping of {latency}ms.")

async def setup(bot):
    await bot.add_cog(Utility(bot))
