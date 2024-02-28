from discord.ext import commands
import discord
from typing import Optional
from datetime import datetime

class Utility(commands.Cog):
    """The Utility Cog ig."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="help", description="Shows the help menu.")
    async def help(self, ctx: commands.Context, command: Optional[str]=None):
        await ctx.send("This command is still underdevelopment.")

    @commands.hybrid_command(name="info", description="Shows the bot's info.")
    async def info(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Info",
            description="Helper Bot is all in one bot.",
            color=0x1fe2f3,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Name", value=self.bot.user.mention, inline=False)
        embed.add_field(name="ID", value=self.bot.user.id, inline=False)
        embed.add_field(name="Owner", value="@no_gaming_01", inline=False)
        embed.add_field(name="Source Code", value="https://github.com/HelperGhost/Helper_Bot", inline=False)
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="ping", description="Tells the ping of the bot.")
    async def ping(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Pong 🏓!",
            description=f"I got a ping of {round(self.bot.latency * 1000)}ms.",
            color=0x1fe2f3,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="invite", description="Gives the invite link of the bot.")
    async def invite(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Invite me to your server!",
            description=f"Here is the link: https://discord.com/api/oauth2/authorize?client_id=1155466619116601406&permissions=8&scope=bot",
            color=0x1fe2f3,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="support", description="Gives the support server invite link.")
    async def support(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Join the support server!",
            description=f"Here is the link: https://dsc.gg/binarybitlab",
            color=0x1fe2f3,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
