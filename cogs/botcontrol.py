from discord.ext import commands
import discord

class BotControl(commands.Cog):
    """The BotControl Cog ig."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title="Error!",
                description=f"{error}.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="Invalid Command!",
                description=f"The command does not exist. Use `help` to see a list of commands.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Missing Permissions!",
                description="You do not have the required permissions to use this command.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Command On Cooldown!",
                description="This command in on cooldown.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Bad Argument!",
                description="Please provide a valid argument.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Error!",
                description="This command is only available to the owner of the bot.",
                color=0x1fe2f3
            )
            await ctx.send(embed=embed)
            return
        if isinstance(error, discord.Forbidden):
            embed = discord.Embed(
                title="Error!",
                description="I do not have permissions to do this.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return
        if isinstance(error, discord.HTTPException):
            embed = discord.Embed(
                title="Error!",
                description="Something went wrong, please try again later.",
                color=0xff0000
            )
            await ctx.send(embed=embed)
            return

async def setup(bot):
    await bot.add_cog(BotControl(bot))
