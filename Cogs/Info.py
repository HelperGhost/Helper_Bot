import discord
from discord.ext import bridge, commands
import datetime

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name="help", description="To get the help menu")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Help Menu!",
            description="",
            color=0x1fe2f3,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Commands", value="To get the help for commands visit https://helperghost.github.io", inline=False)
        embed.add_field(name="Support", value="To get support for the bot visit https://dsc.gg/binarybitlab", inline=False)
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="info", description="To get the bot's information")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Information!",
            description="Here is some information about the bot:",
            color=0x1fe2f3,
            timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="Name", value=self.bot.user.mention, inline=False)
        embed.add_field(name="ID", value=self.bot.user.id, inline=False)
        embed.add_field(name="Owner", value="<@875208986603958344>", inline=False)
        embed.add_field(name="Source Code", value="https://github.com/HelperGhost/Helper_Bot", inline=False)
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="ping", description="To get the bot's ping")
    async def ping(self, ctx):
        embed = discord.Embed(
            title="Pong 🏓!",
            description=f"I got a ping of {round(self.bot.latency * 1000)}ms.",
            color=0x1fe2f3,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="invite", description="To get the bot's invite link")
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Invite me to your server!",
            description=f"Here is the link: https://discord.com/api/oauth2/authorize?client_id=1155466619116601406&permissions=8&scope=bot",
            color=0x1fe2f3,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="support", description="To get the bot's support server link")
    async def support(self, ctx):
        embed = discord.Embed(
            title="Join the support server!",
            description=f"Here is the link: https://dsc.gg/binarybitlab",
            color=0x1fe2f3,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
