from discord.ext import commands
import discord
from discord.ui import View, Select
from typing import Optional
from datetime import datetime

class HelpSelect(Select):
    BLACKLISTED_COG = ["BotControl"]

    def __init__(self, bot: commands.Bot):
        super().__init__(
            placeholder="Select a category.",
            options=self.generate_options(bot)
        )
        
        self.bot = bot

    def generate_options(self, bot: commands.Bot):
        options = []
        for name, cog in bot.cogs.items():
            if name in self.BLACKLISTED_COG:
                continue

            emoji = cog.emoji if hasattr(cog, "emoji") else None

            option = discord.SelectOption(
                label=name,
                description=cog.__doc__,
                value=name,
                emoji=emoji
            )
            options.append(option)
        return options
    
    async def callback(self, interaction: discord.Interaction):
        cog_name = self.values[0]
        cog = self.bot.get_cog(cog_name)

        embed = discord.Embed(
            title=f"{cog.qualified_name}",
            description=cog.__doc__,
            color=0x1fe2f3
        )
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=f"Requested by @{interaction.user.name}.", icon_url=interaction.user.avatar)

        commands = self.get_commands(cog)

        for cmd in commands:
            embed.add_field(name=cmd.name, value=cmd.description, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    def get_commands(self, cog: commands.Cog):
        commands = []
        for cmd in cog.walk_commands():
            if cmd.hidden:
                continue
            commands.append(cmd)
        for cmd in cog.walk_app_commands():
            if cmd.hidden:
                continue
            commands.append(cmd)
        return commands

class Utility(commands.Cog):
    """The Utility Cog."""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "⚙"

    @commands.hybrid_command(name="help", description="Shows the help menu.")
    async def help(self, ctx: commands.Context, command: Optional[str]=None):
        embed = discord.Embed(
            title="Help",
            description="The help menu of Helper Bot.",
            color=0x1fe2f3
        )
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=f"Requested by @{ctx.author.name}.", icon_url=ctx.author.avatar)
        view = View().add_item(HelpSelect(self.bot))
        await ctx.send(embed=embed, view=view)

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
