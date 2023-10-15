import discord
from discord.ext import commands
import datetime

# Now time
now = datetime.datetime.now(datetime.timezone.utc)

class User_Info(commands.Cog):
    def __init__(self, Helper):
        self.helper: commands.Bot = Helper

    @commands.slash_command(name="userinfo", description="tells the information about the user")
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        # discord joined data
        account_created_at = member.created_at
        account_age = now - account_created_at
        discord_join_date = member.created_at.strftime("%A, %B %d, %Y %H:%M UTC")

        # discord joined data
        server_joined_at = member.joined_at
        server_age = now - server_joined_at
        server_join_date = member.created_at.strftime("%A, %B %d, %Y %H:%M UTC ")

        roles = sorted(member.roles, key=lambda role: role.position, reverse=True)
        role = ", ".join(f"{role.mention}" for role in roles if role.name != '@everyone')

        embed = discord.Embed(
        title="",
        description="",
        color= member.color  # You can customize the color here
        )
        embed.set_author(name=f"@{member.name}", icon_url=f"{member.avatar}")
        embed.set_thumbnail(url=f"{member.avatar}")

        embed.add_field(name="**User Info**", value=f"ID: {member.id}\nName: @{member.name}", inline=False)
        embed.add_field(name="**Discord Joined**", value=f"{discord_join_date} ({account_age.days} days)", inline=False)
        embed.add_field(name="**Server Joined**", value=f"{server_join_date} ({server_age.days} days)", inline=False)
        embed.add_field(name="**User's Roles**", value=f"{role}", inline=False)

        await ctx.respond(embed=embed)

def setup(Helper):
    Helper.add_cog(User_Info(Helper))
