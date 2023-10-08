import discord
from discord.ext import commands
import datetime
import asyncio

muted_role_name = "Muted"

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # This is the command to ban people in the server
    @commands.slash_command(name="ban", description="to ban any member in the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        try:
            await member.ban()
            await ctx.respond(f'<@{member.id}> has been banned. Reason: {reason}.')
        except discord.Forbidden:
            await ctx.respond("I don't have permission to ban members.") # Bot will respond this if it does not have the permissions
        except discord.HTTPException:
            await ctx.respond("An error occured while processing the ban command.") # Bot will respond this if there is an error while connecting to discord

    # Timeout command now works
    @commands.slash_command(name="timeout", description="to timeout a member in the server")
    @commands.has_permissions(kick_members=True)
    async def timeout(self, ctx, member: discord.Member, time: int = 10, *, reason: str ="No reason provided"):
        duration = datetime.datetime.utcnow() + datetime.timedelta(minutes=time)
        await member.timeout(duration, reason=reason)
        await ctx.respond(f'{member.mention} has been timed out. reason: {reason}.')

    @commands.slash_command(name="mute", description="to mute a member in discord server")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, time: int = 10, reason: str ="No reason provided"):
        muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)
        duration = time * 60
        try:
            if not muted_role:
                muted_role = ctx.guild.create_role(name=muted_role_name)

            await member.add_roles(muted_role, reason=reason)
            await ctx.respond(f'{member.mention} has been muted for {time} minutes. Reason: {reason}.')

            await asyncio.sleep(duration)

            await member.remove_roles(muted_role)
            await ctx.respond(f'{member.mention} has been unmuted after {time} minutes.')
        except discord.Forbidden:
            await ctx.respond("I don't have permission to mute members.") # Bot will respond this if it does not have the permissions
        except discord.HTTPException:
            await ctx.respond("An error occured while processing the mute command.") # Bot will respond this if there is an error while connecting to discord

    @commands.slash_command(name="unmute", description="to unmute a member in discord server.")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        muted_role = discord.utils.get(ctx.guild.roles, name=muted_role_name)
        try:
            if not muted_role:
                await ctx.respond("The Muted role doesn't exist.")
                return

            if muted_role not in member.roles:
                ctx.respond(f'{member.name} is not muted.')
                return

            await member.remove_roles(muted_role)
            await ctx.respond(f'{member.mention} has been unmuted. Reason: {reason}.')
        except discord.Forbidden:
            await ctx.respond("I don't have permission to unmute members.") # Bot will respond this if it does not have the permissions
        except discord.HTTPException:
            await ctx.respond("An error occured while processing the unmute command.") # Bot will respond this if there is an error while connecting to discord

    @commands.slash_command(name="kick", description="to kick a member in the discord server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        try:
            await member.kick(reason=reason)
            await ctx.respond(f'<@{member.id}> has been kicked from the server. Reason: {reason}.')
        except discord.Forbidden:
            await ctx.respond("I don't have permission to kick members.") # Bot will respond this if it does not have the permissions
        except discord.HTTPException:
            await ctx.respond("An error occured while processing the kick command.") # Bot will respond this if there is an error while connecting to discord

def setup(bot):
    bot.add_cog(Moderation(bot))
