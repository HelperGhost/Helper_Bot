from discord.ext import commands
import discord

class UserInfo(commands.Cog):
    """The UserInfo Cog."""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "😎"

    @commands.hybrid_command(name="userinfo", description="To get the user's information")
    async def userinfo(self, ctx: commands.Context, user: discord.Member = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(
            title="User Information",
            description=f"Here is some information about {user.mention}",
            color=user.color
        )

        account_created_at = user.created_at
        created_at = int(account_created_at.timestamp())

        account_joined_at = user.joined_at
        joined_at = int(account_joined_at.timestamp())

        roles = sorted(user.roles, key=lambda role: role.position, reverse=True)
        role = ', '.join(f"{role.mention}" for role in roles if role!= ctx.guild.default_role)
        
        embed.add_field(name="User Info", value=f"ID: {user.id}\nName: {user.mention}", inline=False)
        embed.add_field(name="Created at", value=f"<t:{created_at}:D> (<t:{created_at}:R>)", inline=False)
        embed.add_field(name="Joined at", value=f"<t:{joined_at}:D> (<t:{joined_at}:R>)", inline=False)
        embed.add_field(name="Roles", value=role, inline=False)
        embed.set_author(name=f"@{ctx.user.name}", icon_url=ctx.user.avatar)
        embed.set_thumbnail(url=user.avatar)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="roles", description="To get the roles of the user")
    async def roles(self, ctx: commands.Context, user: discord.Member = None):
        if user == None:
            user = ctx.author

        embed = discord.Embed(
            title="Roles",
            description=f"Here is the list of roles of {user.mention}",
            color=user.color
        )

        roles = sorted(user.roles, key=lambda role: role.position, reverse=True)
        role = ", ".join(f"{role.mention}" for role in roles if role!= ctx.guild.default_role)

        embed.add_field(name="Roles", value=role, inline=False)
        embed.set_author(name=f"@{ctx.user.name}", icon_url=ctx.user.avatar)
        embed.set_thumbnail(url=user.avatar)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="avatar", description="To get the avatar of the user")
    async def avatar(self, ctx: commands.Context, user: discord.Member = None):
        if user == None:
            user = ctx.author

        embed = discord.Embed(
            title="Avatar",
            description=f"Here is the avatar of {user.mention}",
            color=user.color
        )

        embed.set_image(url=user.avatar)
        embed.set_author(name=f"@{ctx.user.name}", icon_url=ctx.user.avatar)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
