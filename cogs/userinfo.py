from discord.ext import commands
import discord

class UserInfo(commands.Cog):
    """The UserInfo Cog."""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = "😎"

    @commands.hybrid_command(name="userinfo", description="Gets the member information.")
    async def userinfo(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            member = ctx.author

        embed = discord.Embed(
            title="User Information",
            description=f"Here is some information about {member.mention}",
            color=0x1fe2f3
        )

        account_created_at = member.created_at
        created_at = int(account_created_at.timestamp())

        account_joined_at = member.joined_at
        joined_at = int(account_joined_at.timestamp())

        roles = sorted(member.roles, key=lambda role: role.position, reverse=True)
        role = ', '.join(f"{role.mention}" for role in roles if role!= ctx.guild.default_role)
        
        if not role:
            role = "No Roles."
        
        embed.add_field(name="User Info", value=f"ID: {member.id}\nName: {member.mention}", inline=False)
        embed.add_field(name="Created at", value=f"<t:{created_at}:D> (<t:{created_at}:R>)", inline=False)
        embed.add_field(name="Joined at", value=f"<t:{joined_at}:D> (<t:{joined_at}:R>)", inline=False)
        embed.add_field(name="Roles", value=role, inline=False)
        embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
        embed.set_thumbnail(url=member.avatar)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="roles", description="Gets the roles of member.")
    async def roles(self, ctx: commands.Context, member: discord.Member = None):
        if member == None:
            member = ctx.author

        embed = discord.Embed(
            title="Roles",
            description=f"Here is the list of roles of {member.mention}",
            color=0x1fe2f3
        )

        roles = sorted(member.roles, key=lambda role: role.position, reverse=True)
        role = ", ".join(f"{role.mention}" for role in roles if role!= ctx.guild.default_role)

        if not role:
            role = "No Roles."

        embed.add_field(name="Roles", value=role, inline=False)
        embed.set_author(name=f"@{member.name}", icon_url=member.avatar)
        embed.set_thumbnail(url=member.avatar)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="avatar", description="Gets the avatar of member.")
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        if not member:
            member = ctx.author

        embed = discord.Embed(
            title="Avatar",
            description=f"Here is the avatar of {member.mention}",
            color=0x1fe2f3
        )

        embed.set_image(url=member.avatar)
        embed.set_author(name=f"@{member.name}", icon_url=member.avatar)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UserInfo(bot))
