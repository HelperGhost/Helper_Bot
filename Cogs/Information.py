import discord
from discord.ext import bridge, commands
import datetime

# Now time
now = datetime.datetime.now(datetime.timezone.utc)

class User_Info(commands.Cog):
    def __init__(self, Helper):
        self.helper = Helper

    @bridge.bridge_command(name="userinfo", description="tells the information about the user")
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        # discord joined data
        account_created_at = member.created_at
        account_time = int(account_created_at.timestamp())

        # discord joined data
        server_joined_at = member.joined_at
        server_time = int(server_joined_at.timestamp())

        roles = sorted(member.roles, key=lambda role: role.position, reverse=True)
        role = ", ".join(f"{role.mention}" for role in roles if role.name != '@everyone')

        embed = discord.Embed(
        title="",
        description="",
        color= member.color,  # You can customize the color here
        timestamp = datetime.datetime.utcnow()
        )

        embed.set_author(name=f"@{member.name}", icon_url=f"{member.avatar}")
        embed.set_thumbnail(url=f"{member.avatar}")

        embed.add_field(name="**User Info:**", value=f"ID: {member.id}\nName: {member.mention}", inline=False)
        embed.add_field(name="**Discord Joined:**", value=f"<t:{account_time}:D> (<t:{account_time}:R>)", inline=False)
        embed.add_field(name="**Server Joined:**", value=f"<t:{server_time}:D> (<t:{server_time}:R>)", inline=False)
        embed.add_field(name="**User's Roles:**", value=f"{role}", inline=False)

        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="avatar", description="shows avatar of a member")
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed = discord.Embed(
            title="",
            description="",
            color= member.color,  # You can customize the color here
            timestamp = datetime.datetime.utcnow()
        )

        embed.set_author(name=f"@{member.name}", icon_url=f"{member.avatar}")
        embed.set_image(url=f"{member.avatar}")

        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="user_roles", description="provides the roles of the user")
    async def user_roles(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        roles = sorted(member.roles, key=lambda role: role.position, reverse=True)
        role = ", ".join(f"{role.mention}" for role in roles if role.name != '@everyone')

        embed = discord.Embed(
            title = "",
            description = "",
            color = member.color,
            timestamp = datetime.datetime.utcnow()
        )

        embed.set_author(name=f"@{member.name}", icon_url=f"{member.avatar}")
        embed.add_field(name="**Roles:**", value=f"{role}")

        await ctx.respond(embed=embed)

class Server_info(commands.Cog):
    def __init__(self, Helper):
        self.helper: commands.Bot = Helper

    @bridge.bridge_command(name="serverinfo", description="tells the information about the server")
    async def serverinfo(self, ctx):

        server_created_at = ctx.guild.created_at

        roles = sorted(ctx.guild.roles, key=lambda role: role.position, reverse=True)
        role = ", ".join(f"{ctx.guild.roles}" for role in roles if role.name != '@everyone')

        embed = discord.Embed(
            title = "Under Development!",
            description = "",
            color = ctx.guild.owner.color,
            timestamp = datetime.datetime.utcnow()
        )

        embed.set_author(name=f'{ctx.guild.name}', icon_url=f'{ctx.guild.icon}')
        embed.set_thumbnail(url=f'{ctx.guild.icon}')

        embed.add_field(name="**Owner:**", value=f'{ctx.guild.owner.mention}')
        embed.add_field(name="**Members:**", value=len(ctx.guild.members))
        embed.add_field(name="**Roles:**", value=len(ctx.guild.roles))
        embed.add_field(name="**Categories:**", value=len(ctx.guild.categories))
        embed.add_field(name="**Channels:**", value=len(ctx.guild.channels))
        embed.add_field(name="**Text Channels:**", value=len(ctx.guild.text_channels))
        embed.add_field(name="**Voice Channels:**", value=len(ctx.guild.voice_channels))

        await ctx.respond(embed=embed)

    @bridge.bridge_command(name="servericon", description="provides the server icon")
    async def servericon(self, ctx):

        embed = discord.Embed(
            title = "",
            description = "",
            color = ctx.guild.owner.color,
            timestamp = datetime.datetime.utcnow()
        )

        embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
        embed.set_image(url=f"{ctx.guild.icon}")

        await ctx.respond(embed=embed)

def setup(Helper):
    Helper.add_cog(User_Info(Helper))
    Helper.add_cog(Server_info(Helper))
