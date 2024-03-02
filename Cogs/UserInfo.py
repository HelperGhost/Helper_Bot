from venv import create
import discord
from discord.ext import bridge, commands
import datetime
import os
import dotenv

dotenv.load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(guild_ids=[guild_id], name="userinfo", description="To get the user's information")
    async def userinfo(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(
            title="User Information",
            description=f"Here is some information about {user.mention}",
            color=user.color,
            timestamp=datetime.datetime.utcnow()
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
        await ctx.respond(embed=embed)

    @bridge.bridge_command(guild_ids=[guild_id], name="roles", description="To get the roles of the user")
    async def roles(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        embed = discord.Embed(
            title="Roles",
            description=f"Here is the list of roles of {user.mention}",
            color=user.color,
            timestamp=datetime.datetime.utcnow()
        )

        roles = sorted(user.roles, key=lambda role: role.position, reverse=True)
        role = ", ".join(f"{role.mention}" for role in roles if role!= ctx.guild.default_role)

        embed.add_field(name="Roles", value=role, inline=False)
        embed.set_author(name=f"@{ctx.user.name}", icon_url=ctx.user.avatar)
        embed.set_thumbnail(url=user.avatar)

        await ctx.respond(embed=embed)

    @bridge.bridge_command(guild_ids=[guild_id], name="avatar", description="To get the avatar of the user")
    async def avatar(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        embed = discord.Embed(
            title="Avatar",
            description=f"Here is the avatar of {user.mention}",
            color=user.color,
            timestamp=datetime.datetime.utcnow()
        )

        embed.set_image(url=user.avatar)
        embed.set_author(name=f"@{ctx.user.name}", icon_url=ctx.user.avatar)

        await ctx.respond(embed=embed)

    @commands.user_command(guild_ids=[guild_id], name="userid", description="To get the user's ID")
    async def userid(self, ctx, user: discord.Member):
        embed = discord.Embed(
            title="User ID",
            description=f"Id of {user.mention} is `{user.id}`",
            color=user.color,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=f"@{ctx.user.name}", icon_url=ctx.user.avatar)
        embed.set_thumbnail(url=user.avatar)

        await ctx.respond(embed=embed)

    @commands.user_command(guild_ids=[guild_id], name="userage", description="To get the user's age")
    async def userage(self, ctx, user: discord.Member):

        account_created_at = user.created_at
        created_at = int(account_created_at.timestamp())

        embed = discord.Embed(
            title="User Age",
            description=f"Age of {user.mention} is <t:{created_at}:D> (<t:{created_at}:R>)",
            color=user.color,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=f"@{ctx.user.name}", icon_url=ctx.user.avatar)
        embed.set_thumbnail(url=user.avatar)

        await ctx.respond(embed=embed)

    @commands.user_command(guild_ids=[guild_id], name="userjoined", description="To get the user's joined date")
    async def userjoined(self, ctx, user: discord.Member):

        account_joined_at = user.joined_at
        joined_at = int(account_joined_at.timestamp())

        embed = discord.Embed(
            title="User Joined",
            description=f"Joined at <t:{joined_at}:D> (<t:{joined_at}:R>)",
            color=user.color,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_author(name=f"@{ctx.user.name}", icon_url=ctx.user.avatar)
        embed.set_thumbnail(url=user.avatar)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))
