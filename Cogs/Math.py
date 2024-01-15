import discord
from discord.ext import bridge, commands
import datetime

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(name="add", description="To add 2 numbers together")
    async def add(self, ctx, num1, num2):
        try:
            num1 = int(num1)
            num2 = int(num2)
            answer = num1 + num2
            embed = discord.Embed(title="Math!", description=f"The answer is {answer}", color=0x1fe2f3, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
            embed.set_thumbnail(url=self.bot.user.avatar)
            await ctx.respond(embed=embed)
        except ValueError:
            await ctx.respond("Please enter valid numbers.")

    @bridge.bridge_command(name="subtract", description="To subtract 2 numbers")
    async def subtract(self, ctx, num1, num2):
        try:
            num1 = int(num1)
            num2 = int(num2)
            answer = num1 - num2
            embed = discord.Embed(title="Math!", description=f"The answer is {answer}", color=0x1fe2f3, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
            embed.set_thumbnail(url=self.bot.user.avatar)
            await ctx.respond(embed=embed)
        except ValueError:
            await ctx.respond("Please enter valid numbers.")

    @bridge.bridge_command(name="multiply", description="To multiply 2 numbers")
    async def multiply(self, ctx, num1, num2):
        try:
            num1 = int(num1)
            num2 = int(num2)
            answer = num1 * num2
            embed = discord.Embed(title="Math!", description=f"The answer is {answer}", color=0x1fe2f3, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
            embed.set_thumbnail(url=self.bot.user.avatar)
            await ctx.respond(embed=embed)
        except ValueError:
            await ctx.respond("Please enter valid numbers.")

    @bridge.bridge_command(name="divide", description="To divide 2 numbers")
    async def divide(self, ctx, num1, num2):
        try:
            num1 = int(num1)
            num2 = int(num2)
            answer = num1 / num2
            embed = discord.Embed(title="Math!", description=f"The answer is {answer}", color=0x1fe2f3, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"@{self.bot.user}", icon_url=self.bot.user.avatar)
            embed.set_thumbnail(url=self.bot.user.avatar)
            await ctx.respond(embed=embed)
        except ValueError:
            await ctx.respond("Please enter valid numbers.")

def setup(bot):
    bot.add_cog(Math(bot))
