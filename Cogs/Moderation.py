import discord
from discord.ext import bridge, commands
import datetime
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @bridge.bridge_command(name="ban", description="To ban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(title="User Banned", description=f"{member} was banned. Reason: {reason}.", color=0x00ff00)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
            embed.set_footer(text=f"User ID: {member.id}")
            await ctx.respond(embed=embed)
        except discord.Forbidden:
            await ctx.respond("I do not have permissions to ban members")
        except discord.HTTPException:
            await ctx.respond("Banning failed, please try again later")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You do not have permissions to ban members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.respond("Please mention a valid member of this server to ban.")
        else:
            await ctx.respond(f"An error occurred while banning: {error}")
        
    @bridge.bridge_command(name="kick", description="To kick a user from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(title="User Kicked", description=f"{member} was kicked. Reason: {reason}.", color=0xff0000)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
            embed.set_footer(text=f"User ID: {member.id}")
            await ctx.respond(embed=embed)
        except discord.Forbidden:
            await ctx.respond("I do not have permissions to kick members")
        except discord.HTTPException:
            await ctx.respond("Kicking failed, please try again later")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You do not have permissions to kick members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.respond("Please mention a valid member of this server to kick.")
        else:
            await ctx.respond(f"An error occurred while kicking: {error}")
    
    @bridge.bridge_command(name="mute", description="To mute a user in the server")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, time: int = 10, *, reason="No reason provided"):
        try:
            duration = datetime.datetime.utcnow() + datetime.timedelta(minutes=time)
            await member.timeout(duration, reason=reason)
            embed = discord.Embed(title="User Muted", description=f"{member} was muted for {time} minutes. Reason: {reason}.", color=0xffff00)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
            embed.set_footer(text=f"User ID: {member.id}")
            await ctx.respond(embed=embed)
        except discord.Forbidden:
            await ctx.respond("I do not have permissions to mute members")
        except discord.HTTPException:
            await ctx.respond("Muting failed, please try again later")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You do not have permissions to mute members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.respond("Please mention a valid member of this server to mute or provide a valid duration in minutes.")
        elif isinstance(error, ValueError):
            await ctx.respond("Please provide a valid number for duration in minutes.")
        else:
            await ctx.respond(f"An error occurred while muting: {error}")

    @bridge.bridge_command(name="unban", description="To unban a user from the server")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason="No reason provided"):
        try:
            await ctx.guild.unban(discord.Object(id=user.id), reason=reason)
            embed = discord.Embed(title="User Unbanned", description=f"Unbanned {user.name}. Reason: {reason}.", color=0x00ff00)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
            embed.set_footer(text=f"User ID: {user.id}")
            await ctx.respond(embed=embed)
        except discord.Forbidden:
            await ctx.respond("I do not have permissions to unban members")
        except discord.HTTPException:
            await ctx.respond("Unbanning failed, please try again later")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You do not have permissions to unban members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.respond("Please provide a valid member ID to unban.")
        elif isinstance(error, discord.NotFound):
            await ctx.respond("The member ID provided is invalid or not banned from this server.")
        else:
            await ctx.respond(f"An error occurred while unbanning: {error}")

    @bridge.bridge_command(name = "unmute", description = "To unmute a muted user in the server")
    @commands.has_permissions(kick_members = True)
    async def unmute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.remove_timeout()
            embed = discord.Embed(title="User Unmuted", description=f"{member} was unmuted. Reason: {reason}.", color=0x00ff00)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
            embed.set_footer(text=f"User ID: {member.id}")
            await ctx.respond(embed=embed)
        except discord.Forbidden:
            await ctx.respond("I do not have permissions to unmute members")
        except discord.HTTPException:
            await ctx.respond("Unmuting failed, please try again later")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You do not have permissions to unmute members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.respond("Please mention a valid member of this server to unmute.")
        elif isinstance(error, discord.NotFound):
            await ctx.respond("The member provided is not muted in this server.")
        else:
            await ctx.respond(f"An error occurred while unmuting: {error}")

    @bridge.bridge_command(name="purge", description="To purge messages from a channel")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        await ctx.respond(f"Purging {limit} messages...")
        await ctx.channel.purge(limit=limit)
        await asyncio.sleep(3)
        await ctx.send(f"{limit} messages purged")
        await ctx.channel.purge(limit=1)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You do not have permissions to purge messages.")
        elif isinstance(error, commands.BadArgument):
            await ctx.respond("Please provide a valid number for the message limit.")
        else:
            await ctx.respond(f"An error occurred while purging: {error}")

def setup(bot):
    bot.add_cog(Moderation(bot))
